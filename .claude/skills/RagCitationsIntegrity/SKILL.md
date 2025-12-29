Name: RagCitationsIntegrity
Purpose: Enforce “no hallucinations” and mandatory citations for factual claims.

Any output that includes factual claims about visas, costs, salaries, rules, universities, job prospects must include a Sources & citations section.

Retrieval-first rule:
    If no sources are available, state uncertainty clearly and do not output confident factual assertions.

Citation requirements:
    Provide source URLs or references per section where claims appear.
    Distinguish between “estimate / heuristic” vs “source-backed facts”.

Applies both to:
    product outputs (the reports your app generates)
    internal engineering docs describing RAG behavior

If a spec asks for citations, ensure it defines what “citation” means in UI and storage.