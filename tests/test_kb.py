import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1]/'skills/agent-eval-tutor/scripts/kb.py'
spec = importlib.util.spec_from_file_location('kb', SCRIPT)
kb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kb)

class RetrievalTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.original = kb.ROOT, kb.REF
        kb.ROOT = Path(self.temp.name)
        kb.REF = kb.ROOT/'references'
        kb.REF.mkdir()
        (kb.REF/'sample.md').write_text('Synthetic test fixture, not knowledge.\n\nError analysis reviews failures in agent trajectories.\n\n人工标注用于分析错误。')
        kb.save([{'title':'TEST FIXTURE','url':'https://example.invalid/test','status':'available','file':'references/sample.md'}, {'title':'Blocked','url':'https://example.invalid/blocked','status':'failed','reason':'403'}])
    def tearDown(self):
        kb.ROOT, kb.REF = self.original
        self.temp.cleanup()
    def test_english_with_provenance(self):
        result = kb.search('error analysis', 5)
        self.assertEqual(result['results'][0]['paragraph'], 2)
        self.assertEqual(result['results'][0]['url'], 'https://example.invalid/test')
        self.assertEqual(result['missing_sources'], 1)
    def test_chinese(self):
        self.assertTrue(kb.search('人工标注', 5)['results'])
    def test_unsupported_returns_empty(self):
        self.assertEqual(kb.search('quantum cryptography', 5)['results'], [])
    def test_failed_source_excluded(self):
        self.assertEqual(kb.search('blocked', 5)['results'], [])
    def test_no_sources_does_not_invent(self):
        kb.save([{'title':'Missing','url':'https://example.invalid','status':'failed'}])
        result = kb.search('evals', 5)
        self.assertEqual(result['available_sources'],0)
        self.assertEqual(result['results'],[])
    def test_ignore_page_instructions_and_navigation(self):
        page = kb.Page()
        page.feed('<nav>navigation<a href="/ad">ad</a></nav><script>secret()</script><p>article evidence</p>')
        self.assertNotIn('secret', ''.join(page.text))
        self.assertNotIn('/ad', page.links)
        self.assertIn('article evidence',''.join(page.text))
    def test_canonical_preserves_wechat_identity(self):
        self.assertEqual(kb.canonical('https://example.invalid/a?idx=1#section'), 'https://example.invalid/a?idx=1')

    def test_manual_import_preserves_raw_text_and_is_idempotent(self):
        import hashlib
        file = kb.ROOT/'pasted.txt'
        raw = ('用户提供的合成测试正文，包含多轮对话评测。\n'*25).encode()
        file.write_bytes(raw)
        first = kb.import_text(file,kb.WECHAT,'测试内容标签','图片缺失')
        second = kb.import_text(file,kb.WECHAT,'测试内容标签','图片缺失')
        self.assertEqual(first['imported_at'],second['imported_at'])
        self.assertEqual((kb.ROOT/first['raw_file']).read_bytes(),raw)
        self.assertEqual(first['sha256'],hashlib.sha256(raw).hexdigest())
        result = kb.search('多轮对话评测',5)
        candidate = next(r for r in result['results'] if r['url']==kb.WECHAT)
        self.assertEqual(candidate['limitations'],['图片缺失'])
        self.assertIsNone(first['author'])

    def test_full_crawl_preserves_manual_source_when_network_fails(self):
        from unittest.mock import patch
        file = kb.ROOT/'pasted.txt';file.write_text('手动提供的正文，不应被网络失败覆盖。'*30)
        imported = kb.import_text(file,kb.WECHAT,'测试内容标签')
        with patch.object(kb,'fetch_document',side_effect=RuntimeError('network unavailable')) as fetch:
            records = kb.crawl(250)
        kept = next(r for r in records if r['url']==kb.WECHAT)
        self.assertEqual(kept,imported)
        fetch.assert_called_once_with(kb.FAQ)

    def test_short_import_does_not_change_coverage(self):
        file = kb.ROOT/'empty.txt';file.write_text('empty')
        previous = (kb.REF/'coverage.json').read_bytes()
        with self.assertRaisesRegex(ValueError,'insufficient'):
            kb.import_text(file,kb.WECHAT,'测试')
        self.assertEqual((kb.REF/'coverage.json').read_bytes(),previous)


class CorpusIntegrityTests(unittest.TestCase):
    def test_real_corpus_sources_and_files(self):
        import hashlib
        root = SCRIPT.parents[1]
        sources = json.loads((root/'references/coverage.json').read_text())['sources']
        urls = [s['url'] for s in sources]
        self.assertEqual(len(urls),len(set(urls)))
        available = [s for s in sources if s['status']=='available']
        self.assertTrue(any(s['url']==kb.FAQ for s in available))
        for source in available:
            path = (root/source['file']).resolve()
            self.assertTrue(path.is_relative_to(root.resolve()))
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),source['text_sha256'])
            self.assertIn(source['url'],path.read_text())


class ExtractionTests(unittest.TestCase):
    def response(self, text):
        import io
        from email.message import Message
        class Response(io.BytesIO):
            headers = Message()
            headers['Content-Type'] = 'text/html; charset=utf-8'
            url = 'https://hamel.dev/notes/llm/finetuning/data_cleaning.html'
        return Response(text.encode())

    def test_constant_js_redirect(self):
        from unittest.mock import patch
        stub = '<script>var redirects = {"":"data_cleaning.html"}; window.location.replace(redirect);</script>'
        article = '<title>Curating data</title><main><p>'+('Evidence of data cleaning. '*20)+'</p></main>'
        with patch.object(kb.urllib.request,'urlopen',side_effect=[self.response(stub),self.response(article)]) as fetch:
            result = kb.fetch_document('https://hamel.dev/notes/llm/finetuning/04_data_cleaning.html')
        self.assertEqual(result['title'],'Curating data')
        self.assertEqual(fetch.call_count,2)
        self.assertIn('data_cleaning.html',fetch.call_args.args[0].full_url)

    def test_insecure_js_redirect_rejected(self):
        from unittest.mock import patch
        stub = '<script>var redirects = {"":"http://example.invalid"}; window.location.replace(redirect);</script>'
        with patch.object(kb.urllib.request,'urlopen',return_value=self.response(stub)):
            with self.assertRaisesRegex(ValueError,'HTTPS'):
                kb.fetch_document('https://hamel.dev/stub.html')

    def test_bad_pdf_rejected(self):
        with self.assertRaisesRegex(ValueError,'not a PDF'): kb.read_pdf(b'not a pdf')

    @unittest.skipUnless(kb.shutil.which('pdftotext'),'Poppler not installed')
    def test_real_pdf_text_extraction(self):
        # Locally generated synthetic PDF, never included in the knowledge corpus.
        text = 'Synthetic PDF test fixture. Error analysis examines failures. '*6
        stream = ('BT /F1 10 Tf 20 700 Td ('+text+') Tj ET').encode()
        objects = [b'<< /Type /Catalog /Pages 2 0 R >>',b'<< /Type /Pages /Kids [3 0 R] /Count 1 >>',b'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 2000 800] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>',b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>',b'<< /Length '+str(len(stream)).encode()+b' >>\nstream\n'+stream+b'\nendstream']
        pdf=b'%PDF-1.4\n'; offsets=[0]
        for i,obj in enumerate(objects,1):
            offsets.append(len(pdf));pdf+=str(i).encode()+b' 0 obj\n'+obj+b'\nendobj\n'
        xref=len(pdf);pdf+=b'xref\n0 6\n0000000000 65535 f \n'
        for offset in offsets[1:]:pdf+=f'{offset:010} 00000 n \n'.encode()
        pdf+=b'trailer\n<< /Size 6 /Root 1 0 R >>\nstartxref\n'+str(xref).encode()+b'\n%%EOF\n'
        title, body = kb.read_pdf(pdf)
        self.assertIn('PDF page 1',body)
        self.assertIn('Error analysis examines failures',body)

    def test_personal_profile_is_not_method_evidence(self):
        from unittest.mock import patch
        response=self.response('<title>Profile</title>'+('profile '*60))
        response.url='https://www.linkedin.com/in/person'
        with patch.object(kb.urllib.request,'urlopen',return_value=response):
            with self.assertRaises(kb.ExcludedSource): kb.fetch_document(response.url)

    def test_excluded_domain_is_not_retried(self):
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as directory:
            original=kb.ROOT,kb.REF
            try:
                kb.ROOT=Path(directory);kb.REF=kb.ROOT/'references'
                kb.save([{'url':kb.WECHAT,'title':'missing','status':'failed','reason':'original failure'}])
                with patch.object(kb,'fetch_document') as fetch:
                    records=kb.crawl(250,True,['mp.weixin.qq.com'])
                fetch.assert_not_called()
                self.assertEqual(records[0]['reason'],'original failure')
            finally:kb.ROOT,kb.REF=original

if __name__ == '__main__': unittest.main()
