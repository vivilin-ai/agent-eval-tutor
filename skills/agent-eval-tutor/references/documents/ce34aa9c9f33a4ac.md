# Q: What is a trace? – Hamel’s Blog

Source: https://hamel.dev/blog/posts/evals-faq/what-is-a-trace.html

Q: What is a trace?

    
LLMs

evals

faq

faq-individual

  

  

    A trace is the full record from a user’s first query through the final response.

    

    
Authors

             
Hamel Husain 

Shreya Shankar 

  

    

    
Published

      
July 27, 2025

  

    

  

A trace is the complete record of all actions, messages, tool calls, and data retrievals from a single initial user query through to the final response. It includes every step across all agents, tools, and system components in a session: multiple user messages, assistant responses, retrieved documents, and intermediate tool interactions.

Note on terminology: Different observability vendors use varying definitions of traces and spans. Alex Strick van Linschoten’s analysis highlights these differences (screenshot below):

Vendor differences in trace definitions as of 2025-07-02

↩︎ Back to main FAQ

This article is part of our AI Evals FAQ, a collection of common questions (and answers) about LLM evaluation. View all FAQs or return to the homepage.
