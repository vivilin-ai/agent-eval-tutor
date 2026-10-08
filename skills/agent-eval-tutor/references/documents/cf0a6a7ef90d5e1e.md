# Q: How do I surface problematic traces for review beyond user feedback? – Hamel’s Blog

Source: https://hamel.dev/blog/posts/evals-faq/how-do-i-surface-problematic-traces-for-review-beyond-user-feedback.html

Q: How do I surface problematic traces for review beyond user feedback?

    
LLMs

evals

faq

faq-individual

  

  

    Sampling and existing evals can surface problematic traces without relying only on user feedback.

    

    
Authors

             
Hamel Husain 

Shreya Shankar 

  

    

    
Published

      
July 27, 2025

  

    

  

While user feedback is a good way to narrow in on problematic traces, other methods are also useful. Here are three complementary approaches:

Start with random sampling

The simplest approach is reviewing a random sample of traces. If you find few issues, escalate to stress testing: create queries that deliberately test your prompt constraints to see if the AI follows your rules.

Use evals for initial screening

Use existing evals to find problematic traces and potential issues. Once you’ve identified these, you can proceed with the typical evaluation process starting with error analysis.

Leverage efficient sampling strategies

For more sophisticated trace discovery, use outlier detection, metric-based sorting, and stratified sampling to find interesting traces. Generic metrics can serve as exploration signals to identify traces worth reviewing, even if they don’t directly measure quality.

↩︎ Back to main FAQ

This article is part of our AI Evals FAQ, a collection of common questions (and answers) about LLM evaluation. View all FAQs or return to the homepage.
