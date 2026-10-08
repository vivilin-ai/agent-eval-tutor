#!/usr/bin/env python3
"""Dependency-free, inspectable corpus builder and lexical retrieval."""
import argparse
import hashlib
import json
import math
import re
import shutil
import subprocess
import tempfile
import urllib.parse
import urllib.request
import urllib.error
from datetime import datetime, timezone
from html import unescape
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / 'references'
FAQ = 'https://hamel.dev/blog/posts/evals-faq/'
WECHAT = 'https://mp.weixin.qq.com/s?__biz=Mzg4NTczNzg2OA==&mid=2247511370&idx=1&sn=c9f4ff1d054cb229ac2f8c1462fcb05e'

class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.text = []; self.links = []; self.skip = 0
    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style', 'nav', 'footer'): self.skip += 1
        if not self.skip and tag == 'a':
            href = dict(attrs).get('href')
            if href: self.links.append(href)
        if not self.skip and tag in ('p','h1','h2','h3','li','br','div'): self.text.append('\n')
    def handle_endtag(self, tag):
        if tag in ('script','style','nav','footer') and self.skip: self.skip -= 1
    def handle_data(self, data):
        if not self.skip: self.text.append(data)

def canonical(url):
    p = urllib.parse.urlsplit(url)
    path = p.path
    if p.hostname == 'hamel.dev':
        path = re.sub(r'index\.html$', '', path)
        if not Path(path).suffix and not path.endswith('/'): path += '/'
    return urllib.parse.urlunsplit((p.scheme, p.netloc, path, p.query, ''))

def terms(text):
    out = re.findall(r'[a-z0-9]+', text.lower())
    for s in re.findall(r'[\u4e00-\u9fff]+', text):
        out += [s[i:i+2] for i in range(max(1, len(s)-1))]
    return out

def save(records):
    REF.mkdir(parents=True, exist_ok=True)
    (REF/'coverage.json').write_text(json.dumps({'updated_at':datetime.now(timezone.utc).isoformat(), 'scope':'FAQ direct substantive links; relevant Hamel evaluation articles one further hop; external links not recursively expanded. Unavailable pages are not evidence.', 'sources': records},ensure_ascii=False,indent=2)+'\n')
    catalog = ['# 来源目录', '', '自动抓取不代表逐页核验；方法建议必须阅读上下文。PDF 保留页码，图片/公式需检查原文件。', '']
    for source in records:
        if source['status'] == 'available':
            name = Path(source['file']).name
            catalog.append(f"- [{source['title']}]({source['url']}) — [{name}](documents/{name})")
            if source.get('source_format') == 'author_markdown':
                catalog.append('  作者官方源码：'+source['resolved_url'])
            if source.get('source_format') == 'user_provided_text':
                catalog.append('  用户提供正文；原始标题/作者/发布时间及图表未独立核验。')
    (REF/'catalog.md').write_text('\n'.join(catalog)+'\n')

def search(query, limit):
    coverage = json.loads((REF/'coverage.json').read_text())
    passages = []
    for source in coverage['sources']:
        if source['status'] != 'available': continue
        text = (ROOT/source['file']).read_text()
        paragraphs = re.split(r'\n\s*\n', text)
        for i, para in enumerate(paragraphs):
            context = '\n\n'.join(paragraphs[max(0,i-1):i+5])
            if para.strip(): passages.append((source,i+1,para,terms(para),context))
    q = set(terms(query)); n = len(passages)
    freq = {t:sum(t in p[3] for p in passages) for t in q}
    scored = []
    for source, i, para, ts, context in passages:
        score = sum(math.log(1+(n-freq[t]+.5)/(freq[t]+.5))*ts.count(t)/(ts.count(t)+1.2) for t in q if t in ts)
        if score:
            title_terms = set(terms(source['title']))
            score += .8 * sum(math.log(1+(n-freq[t]+.5)/(freq[t]+.5)) for t in q if t in title_terms)
        if score: scored.append({'title':source['title'],'url':source['url'],'file':source['file'],'paragraph':i,'score':round(score,3),'excerpt':para[:2400],'context':context[:6000],'source_format':source.get('source_format','html_article'),'evidence_scope':source.get('evidence_scope','read_context_before_use'),'limitations':source.get('limitations',[])})
    scored.sort(key=lambda x:x['score'],reverse=True)
    return {'query':query,'available_sources':sum(s['status']=='available' for s in coverage['sources']), 'missing_sources':sum(s['status'] in ('blocked','failed') for s in coverage['sources']), 'results':scored[:limit], 'warning':'Lexical candidates only; read source context before answering.'}

class ExcludedSource(ValueError):
    """Fetched page exists but is not a methods document."""


def read_pdf(data):
    if not data.startswith(b'%PDF-'):
        raise ValueError('response is not a PDF')
    if not shutil.which('pdftotext'):
        raise ValueError('PDF extraction requires pdftotext (Poppler)')
    with tempfile.TemporaryDirectory(prefix='agent-evals-pdf-') as directory:
        path = Path(directory)/'source.pdf'
        path.write_bytes(data)
        result = subprocess.run(['pdftotext','-layout',str(path),'-'],capture_output=True,timeout=60)
    if result.returncode:
        raise ValueError('PDF extraction failed: '+result.stderr.decode('utf-8',errors='replace')[:300])
    text = result.stdout.decode('utf-8',errors='replace')
    if len(re.sub(r'\s','',text)) < 200:
        raise ValueError('PDF has insufficient extractable text; OCR/manual import needed')
    pages = ['## PDF page '+str(i+1)+'\n\n'+page.strip() for i,page in enumerate(text.split('\f')) if page.strip()]
    title = ' '.join(text.strip().splitlines()[:2]).strip()[:180]
    return title, '\n\n'.join(pages)


def _fetch_document(url):
    current = url
    visited = set()
    for _ in range(5):
        if current in visited: raise ValueError('redirect loop')
        visited.add(current)
        req = urllib.request.Request(current,headers={'User-Agent':'AgentEvalTutor-KnowledgeBuilder/1.0'})
        with urllib.request.urlopen(req,timeout=25) as response:
            resolved = response.url
            content_type = response.headers.get('Content-Type','')
            charset = response.headers.get_content_charset() or 'utf-8'
            data = response.read(40_000_001)
        if len(data)>40_000_000: raise ValueError('page exceeds 40 MB size limit')
        host = urllib.parse.urlsplit(resolved).hostname
        path = urllib.parse.urlsplit(resolved).path
        if host == 'www.linkedin.com' and path.startswith('/in/'):
            raise ExcludedSource('personal profile; fetched but not an evaluation methods article')
        if host == 'arxiv.org' and path.startswith('/search'):
            raise ExcludedSource('search index; fetched but not a paper or methods document')
        if host == 'arxiv.org' and path.startswith('/abs/'):
            current = 'https://arxiv.org/pdf/'+path.rsplit('/',1)[-1]
            continue
        if 'pdf' in content_type or data.startswith(b'%PDF-'):
            title, body = read_pdf(data)
            if host == 'arxiv.org':
                abstract_url = 'https://arxiv.org/abs/'+path.rsplit('/',1)[-1]
                try:
                    with urllib.request.urlopen(abstract_url,timeout=25) as metadata_response:
                        metadata = metadata_response.read(1_000_000).decode('utf-8',errors='replace')
                    citation_title = re.search(r'<meta\s+name="citation_title"\s+content="([^"]+)"',metadata)
                    if citation_title: title = unescape(citation_title.group(1))
                except urllib.error.URLError:
                    pass  # Full PDF remains the evidence; metadata is optional.
            return {'title':title,'body':body,'links':[], 'resolved_url':resolved,
                    'source_format':'pdf_fulltext','sha256':hashlib.sha256(data).hexdigest(),
                    'extraction_note':'Poppler text extraction; page numbers retained. Images and equations may need original PDF verification.'}
        if 'html' not in content_type: raise ValueError('unsupported content type: '+content_type)
        html = data.decode(charset,errors='replace')
        # Follow only the constant fallback in Quarto's redirect stub; never execute JS.
        redirect = re.search(r'var\s+redirects\s*=\s*(\{[^;]+\})\s*;',html)
        if redirect and 'window.location.replace(redirect)' in html:
            mapping = json.loads(redirect.group(1)); target = mapping.get('')
            if not isinstance(target,str): raise ValueError('unsupported dynamic redirect')
            current = urllib.parse.urljoin(resolved,target)
            if urllib.parse.urlsplit(current).scheme != 'https': raise ValueError('redirect must use HTTPS')
            continue
        if host in ('youtu.be','www.youtube.com','m.youtube.com'):
            raise ValueError('video page is not evidence; an official caption transcript is required')
        page = Page()
        main = re.search(r'<main\b[^>]*>(.*?)</main>',html,re.S|re.I)
        article = re.search(r'<article\b[^>]*>(.*?)</article>',html,re.S|re.I)
        wechat = re.search(r'<div\b[^>]*id=["\']js_content["\'][^>]*>(.*)',html,re.S|re.I)
        page.feed(main.group(1) if main else article.group(1) if article else wechat.group(1) if wechat else html)
        body = re.sub(r'\n[ \t]*\n+', '\n\n',''.join(page.text)).strip()
        title_match = re.search(r'<title[^>]*>(.*?)</title>',html,re.S|re.I)
        title = unescape(re.sub('<.*?>','',title_match.group(1))).strip() if title_match else url
        if len(body)<200 or any(x in body for x in ('环境异常','访问过于频繁','验证后继续访问')) or re.search(r'captcha|access denied|just a moment',title,re.I):
            raise ValueError('empty or access challenge; not article evidence')
        return {'title':title,'body':body,'links':page.links,'resolved_url':resolved,
                'source_format':'html_article','sha256':hashlib.sha256(data).hexdigest()}
    raise ValueError('too many redirects')


# Publisher-owned alternative identified through the original URL's exact alias.
AUTHOR_ALTERNATIVES = {
    'https://mlops.systems/posts/2025-06-04-instrumenting-an-agentic-app-with-arize-phoenix-and-litellm.html':
    'https://raw.githubusercontent.com/strickvl/mlops-dot-systems/main/posts/2025-06-04-instrumenting-an-agentic-app-with-arize-phoenix-and-litellm.md'
}


def fetch_document(url):
    try:
        return _fetch_document(url)
    except urllib.error.URLError as original_error:
        alternative = AUTHOR_ALTERNATIVES.get(url)
        if not alternative: raise
        with urllib.request.urlopen(alternative,timeout=25) as response:
            data = response.read(8_000_001)
        if len(data)>8_000_000: raise ValueError('author source exceeds size limit')
        text = data.decode('utf-8')
        if not text.startswith('---') or urllib.parse.urlsplit(url).path not in text.split('---',2)[1]:
            raise ValueError('author source does not declare original path as an alias')
        title = re.search(r'^title:\s*"([^"\n]+)"',text,re.M)
        if not title: raise ValueError('author source lacks title')
        return {'title':title.group(1),'body':text.split('---',2)[-1].strip(),
                'links':[], 'resolved_url':alternative,'source_format':'author_markdown',
                'sha256':hashlib.sha256(data).hexdigest(),
                'extraction_note':'Recovered from publisher-owned source declaring exact original path. Original failure: '+str(original_error)}


def import_text(file, url, title, note=''):
    url = canonical(url)
    if urllib.parse.urlsplit(url).scheme != 'https':
        raise ValueError('source URL must use HTTPS')
    raw = Path(file).read_bytes()
    body = raw.decode('utf-8-sig')
    if len(body.strip()) < 200:
        raise ValueError('insufficient article text')
    records = json.loads((REF/'coverage.json').read_text())['sources'] if (REF/'coverage.json').exists() else []
    previous = next((r for r in records if r['url'] == url), None)
    digest = hashlib.sha256(raw).hexdigest()
    if previous and previous['status'] == 'available':
        if previous.get('source_format') == 'user_provided_text' and previous.get('sha256') == digest:
            return previous
        raise ValueError('available source already exists; preserve it before replacing')
    name = hashlib.sha256(url.encode()).hexdigest()[:16]
    folder = REF/'documents'; folder.mkdir(parents=True, exist_ok=True)
    (folder/(name+'.txt')).write_bytes(raw)
    document = folder/(name+'.md')
    document.write_text('# '+title+'\n\nSource: '+url+'\n\n'+body, encoding='utf-8')
    record = {'url':url,'title':title,'title_status':'descriptive_label_original_title_unverified',
              'status':'available','source_format':'user_provided_text',
              'file':'references/documents/'+name+'.md','raw_file':'references/documents/'+name+'.txt',
              'sha256':digest,'text_sha256':hashlib.sha256(document.read_bytes()).hexdigest(),
              'imported_at':datetime.now(timezone.utc).isoformat(),
              'source_verification':'URL association supplied by user; live page not independently retrieved',
              'author':None,'published_at':None,'limitations':[note] if note else [],
              'evidence_scope':'pasted text only; case-specific methods and numbers are not universal defaults'}
    if previous:
        record['previous_access_attempt'] = {k:previous[k] for k in ('reason','attempted_at') if k in previous}
    records = [record if r['url'] == url else r for r in records]
    if previous is None: records.append(record)
    save(records)
    return record


def crawl(max_pages, retry_failed=False, exclude_domains=()):
    existing = json.loads((REF/'coverage.json').read_text())['sources'] if (REF/'coverage.json').exists() else []
    old = existing if retry_failed else [r for r in existing if r.get('source_format') == 'user_provided_text']
    records = [r for r in old if r['status'] != 'failed' or urllib.parse.urlsplit(r['url']).hostname in exclude_domains]
    queue = [(r['url'],r.get('depth',1)) for r in old if r['status']=='failed' and urllib.parse.urlsplit(r['url']).hostname not in exclude_domains] if retry_failed else [(FAQ,0),(WECHAT,0)]
    seen = {r['url'] for r in records}
    while queue:
        url, depth = queue.pop(0)
        if url in seen: continue
        seen.add(url)
        if len(records) >= max_pages:
            records.append({'url':url,'title':url,'status':'excluded','reason':'page budget reached'}); continue
        rec = {'url':url,'title':url,'depth':depth}
        try:
            document = fetch_document(url)
            rec.update({k:v for k,v in document.items() if k not in ('body','links')})
            body = document['body']
            name = hashlib.sha256(url.encode()).hexdigest()[:16]+'.md'
            folder = REF/'documents'; folder.mkdir(parents=True,exist_ok=True)
            (folder/name).write_text('# '+rec['title']+'\n\nSource: '+url+'\n\n'+body+'\n')
            rec.update(status='available',file='references/documents/'+name,text_sha256=hashlib.sha256((folder/name).read_bytes()).hexdigest(),retrieved_at=datetime.now(timezone.utc).isoformat())
            if url == FAQ or (urllib.parse.urlsplit(url).hostname == 'hamel.dev' and depth == 1):
                for link in document['links']:
                    target = canonical(urllib.parse.urljoin(document['resolved_url'],link)); p = urllib.parse.urlsplit(target)
                    if p.scheme != 'https' or target == url: continue
                    relevant = p.hostname == 'hamel.dev' and ('/blog/posts/' in p.path or '/notes/llm/' in p.path) and re.search(r'eval|judge|llm|error|agent',p.path,re.I)
                    if url == FAQ or relevant:
                        if target == canonical(url) or target in seen: continue
                        reason = None
                        if p.path.endswith(('.png','.jpg','.css','.js')): reason = 'asset, not substantive article'
                        elif p.hostname == 'maven.com' or p.path in ('','/'): reason = 'course or site landing page, not substantive article'
                        if reason:
                            if target not in seen: records.append({'url':target,'title':target,'status':'excluded','reason':reason}); seen.add(target)
                        else: queue.append((target,depth+1))
        except ExcludedSource as e:
            rec.update(status='excluded',reason=str(e),fetched_at=datetime.now(timezone.utc).isoformat())
        except Exception as e:
            rec.update(status='failed',reason=str(e),attempted_at=datetime.now(timezone.utc).isoformat())
        records.append(rec)
        save(records)
    save(records)
    return records

def main():
    parser = argparse.ArgumentParser(); sub = parser.add_subparsers(dest='command',required=True)
    s = sub.add_parser('search'); s.add_argument('query'); s.add_argument('--limit',type=int,default=5)
    c = sub.add_parser('crawl'); c.add_argument('--max-pages',type=int,default=250); c.add_argument('--retry-failed',action='store_true'); c.add_argument('--exclude-domain',action='append',default=[])
    i = sub.add_parser('import-text'); i.add_argument('--file',required=True); i.add_argument('--url',required=True); i.add_argument('--title',required=True); i.add_argument('--note',default='')
    sub.add_parser('status')
    args = parser.parse_args()
    if args.command == 'search': result = search(args.query,args.limit)
    elif args.command == 'import-text': result = import_text(args.file,args.url,args.title,args.note)
    elif args.command == 'crawl':
        records = crawl(args.max_pages,args.retry_failed,args.exclude_domain)
        result = {'sources':len(records),'statuses':{status:sum(r['status']==status for r in records) for status in ('available','failed','excluded')},'coverage':'references/coverage.json'}
    else: result = json.loads((REF/'coverage.json').read_text())
    print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__ == '__main__': main()
