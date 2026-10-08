# Q: How do you review a trace that is really large? – Hamel’s Blog

Source: https://hamel.dev/blog/posts/evals-faq/what-if-the-source-material-is-too-large-for-a-person-to-review.html

Q: How do you review a trace that is really large?

    
LLMs

evals

faq

faq-individual

  

  

    Review large AI agent traces efficiently by prioritizing the first upstream failure and making relevant evidence easier to inspect.

    

    
Authors

             
Hamel Husain 

Shreya Shankar 

  

    

    
Published

      
September 13, 2026

  

    

    
Modified

      
September 14, 2026

  

  

Traces can get large when an agent runs for a long time or retrieves a large amount of context. A useful heuristic is to focus on the first upstream failure. Errors tend to compound, which means you can prioritize earlier ones to save time.

Use progressive disclosure in your review tool by showing the most relevant information first and letting reviewers expand details as needed. For example, show the conversation initially, with tool outputs collapsed until a reviewer needs to inspect them.

If a single trace is still too large to review, work with the domain expert to identify what they need to check. Build a tool that extracts the relevant evidence and links back to its location in the trace or retrieved document. For example, when reviewing an answer about a long contract, the tool could show the relevant clauses with links to their original pages. Always validate this kind of extraction with a domain expert.

Quality is more important than quantity. You can usually learn more from carefully investigating a few failures than from rushing through many traces.

↩︎ Back to main FAQ

This article is part of our AI Evals FAQ, a collection of common questions (and answers) about LLM evaluation. View all FAQs or return to the homepage.
