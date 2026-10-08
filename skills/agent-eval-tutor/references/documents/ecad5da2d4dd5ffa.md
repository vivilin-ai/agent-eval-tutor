# Q: What should an internal eval platform standardize across teams? – Hamel’s Blog

Source: https://hamel.dev/blog/posts/evals-faq/what-should-an-internal-eval-platform-standardize-across-teams.html

Q: What should an internal eval platform standardize across teams?

    
LLMs

evals

faq

  

  

    Help teams find real failures and validate their evals instead of imposing generic metrics or one set of tools.

    

    
Authors

             
Hamel Husain 

Shreya Shankar 

  

    

    
Published

      
September 19, 2026

  

    

    
Modified

      
September 21, 2026

  

  

When building an internal eval platform, it’s tempting to start with tools, infrastructure, and a shared set of metrics. That can lead teams to adopt whatever the platform offers without checking whether it helps them find and fix problems in their products.

Start by encouraging teams to perform error analysis and sample data effectively for review. They can use the failures they find to decide which automated checks to build, then validate evaluators against human labels. Standardize these processes while letting each team develop its own metrics and, when needed, tools. The field guide shows an example of how these might fit together.

Give teams the flexibility to build their own tools, especially now that AI coding agents make custom software cheaper to create. For example, tools to annotate data often need custom interfaces that fit the data being reviewed. Reviewing text extracted from a scanned document calls for a different interface than reviewing chat conversations.

A platform can still provide shared storage for results and support collaboration on labeling. Start by serving one team and one use case well, then expand as you learn which needs are shared. The benefit of standardization is smaller when teams have very different needs and can build their own tools cheaply.

Comparing eval scores across projects only makes sense when the checks and test data are comparable. We strongly advise against offering generic metrics, such as helpfulness or coherence, as a shortcut. They are rarely useful as quality measures and tend to distract teams from the failures that affect their users.

↩︎ Back to main FAQ

This article is part of our AI Evals FAQ, a collection of common questions (and answers) about LLM evaluation. View all FAQs or return to the homepage.
