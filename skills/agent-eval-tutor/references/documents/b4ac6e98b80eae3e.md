# Q: What is the best approach for generating synthetic data? – Hamel’s Blog

Source: https://hamel.dev/blog/posts/evals-faq/what-is-the-best-approach-for-generating-synthetic-data.html

Q: What is the best approach for generating synthetic data?

    
LLMs

evals

faq

faq-individual

  

  

    Handwritten dimension tuples can produce synthetic queries for testing full traces.

    

    
Authors

             
Hamel Husain 

Shreya Shankar 

  

    

    
Published

      
June 1, 2025

  

    

    
Modified

      
September 1, 2026

  

  

A common mistake is prompting an LLM to "give me test queries" without structure, resulting in generic, repetitive outputs. A structured approach using dimensions produces far better synthetic data for testing LLM applications.

When should I use synthetic data for evals?

Use synthetic data to start error analysis before you have enough production traffic, or to test a known failure that appears rarely in real data. Define the variation you need, generate examples, run them through the full system, and review the resulting traces.

Synthetic data cannot tell you how common a failure is in production. It can also miss details that matter in specialized domains. Compare synthetic examples with real data as soon as real data becomes available. See when synthetic data may be unreliable for cases that require extra review.

Define important dimensions first

Start by defining dimensions: categories that describe different aspects of user queries. Each dimension captures one type of variation in user behavior. For example:

For a recipe app, dimensions might include Dietary Restriction (vegan, gluten-free, none), Cuisine Type (Italian, Asian, comfort food), and Query Complexity (simple request, multi-step, edge case).

For a customer support bot, dimensions could be Issue Type (billing, technical, general), Customer Mood (frustrated, neutral, happy), and Prior Context (new issue, follow-up, resolved).

Start with failure hypotheses. If you lack intuition about failure modes, use your application extensively or recruit friends to use it. Then choose dimensions targeting those likely failures.

Create tuples manually first: Write 20 tuples by hand. Each tuple selects one value from each dimension. Example: (Vegan, Italian, Multi-step). This manual work helps you understand your problem space.

Scale with two-step generation:

Generate structured tuples: Have the LLM create more combinations like (Gluten-free, Asian, Simple)

Convert tuples to queries: In a separate prompt, turn each tuple into natural language

This separation avoids repetitive phrasing. The (Vegan, Italian, Multi-step) tuple becomes: "I need a dairy-free lasagna recipe that I can prep the day before."

Generation approaches

You can generate tuples two ways:

Cross product then filter: Generate all dimension combinations, then filter with an LLM. Guarantees coverage including edge cases. Use when most combinations are valid.

Direct LLM generation: Ask the LLM to generate tuples directly. This produces more realistic combinations, but it tends toward generic outputs and misses rare scenarios. Use it when many dimension combinations are invalid.

Fix obvious problems first: Don’t generate synthetic data for issues you can fix immediately. If your prompt doesn’t mention dietary restrictions, fix the prompt rather than generating specialized test queries.

After iterating on your tuples and prompts, run these synthetic queries through your actual system to capture full traces. A pool of roughly 100 diverse traces is a useful starting point for failure discovery. Have an agent help with sampling, annotate at least 30 traces yourself, then review the agent’s suggestions until your learning plateaus. See how many examples you need for error discovery for the full explanation.

Here is a visual that helps visualize the process.

↩︎ Back to main FAQ
