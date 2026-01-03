"""
AI service for report generation using Gemini 2.0 Flash
Uses LangChain for orchestration with UK-specific prompts
"""

import json
from datetime import datetime
from typing import AsyncIterator
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from src.config import settings
from src.api.models.report import ReportContent, ReportSection, Citation

# Initialize Gemini model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-exp",
    google_api_key=settings.GEMINI_API_KEY,
    temperature=0.3,  # Low temperature for factual accuracy
)

# UK-specific system prompt
UK_SYSTEM_PROMPT = """You are an expert educational consultant specializing in UK higher education and migration.

CRITICAL REQUIREMENTS:
1. ALL information must be specific to the United Kingdom ONLY
2. Include citations for every major claim (minimum 3 citations per section, except Executive Summary)
3. Generate exactly 10 sections in this EXACT order:

   SECTION 1: Executive Summary (5-10 bullet points)
   SECTION 2: Study Options in the UK
   SECTION 3: Estimated Cost of Studying (Tuition Ranges + Living Costs)
   SECTION 4: Visa & Immigration Overview (high-level, non-legal)
   SECTION 5: Post-Study Work Options
   SECTION 6: Job Prospects in the Chosen Subject
   SECTION 7: Fallback Job Prospects (Out-of-Field)
   SECTION 8: Risks & Reality Check
   SECTION 9: 30/60/90-Day Action Plan
   SECTION 10: Sources & Citations

4. Each section (except Executive Summary) must be 200-300 words
5. Executive Summary must be 5-10 concise bullet points
6. Citations must include: title, url, and snippet
7. All URLs must be real and verifiable
8. Focus on current 2024-2025 academic year information
9. If data is uncertain, state uncertainty clearly - NO uncited confident claims allowed

FORMAT YOUR RESPONSE AS VALID JSON:
{
  "query": "user's original query",
  "summary": "brief 2-3 sentence summary",
  "sections": [
    {
      "heading": "Executive Summary",
      "content": "• Bullet point 1\\n• Bullet point 2\\n• Bullet point 3\\n...",
      "citations": []
    },
    {
      "heading": "Study Options in the UK",
      "content": "detailed content with markdown formatting (200-300 words)",
      "citations": [
        {
          "title": "source title",
          "url": "https://...",
          "snippet": "relevant quote or summary"
        }
      ]
    }
  ]
}
"""


async def generate_report(query: str) -> ReportContent:
    """
    Generate a complete research report for UK study query
    Returns structured ReportContent with citations
    """
    # Validate UK-only query
    if not is_uk_query(query):
        raise ValueError(
            "Query must be related to studying in the United Kingdom. "
            "Please specify UK universities, courses, or migration."
        )

    # Create prompt
    prompt = f"""Generate a comprehensive research report for the following UK study query:

QUERY: {query}

Provide detailed, factual information with proper citations.
Remember: UK-specific information only!"""

    try:
        # Generate response
        messages = [
            SystemMessage(content=UK_SYSTEM_PROMPT),
            HumanMessage(content=prompt),
        ]

        response = llm.invoke(messages)
        content = response.content

        # Parse JSON response
        report_data = json.loads(content)

        # Validate and structure the response
        sections = []
        for section_data in report_data.get("sections", []):
            citations = [
                Citation(
                    title=cit["title"],
                    url=cit["url"],
                    snippet=cit.get("snippet", ""),
                    accessed_at=datetime.utcnow(),
                )
                for cit in section_data.get("citations", [])
            ]

            sections.append(
                ReportSection(
                    heading=section_data["heading"],
                    content=section_data["content"],
                    citations=citations,
                )
            )

        # Validate we have all 10 sections
        if len(sections) != 10:
            raise ValueError(
                f"Expected 10 sections, got {len(sections)}. Report generation incomplete."
            )

        # Validate citations exist
        total_citations = sum(len(s.citations) for s in sections)
        if total_citations == 0:
            raise ValueError("Report must include citations for credibility")

        return ReportContent(
            query=query,
            summary=report_data.get("summary", ""),
            sections=sections,
            total_citations=total_citations,
            generated_at=datetime.utcnow(),
        )

    except json.JSONDecodeError:
        raise ValueError("Failed to parse AI response as JSON")
    except Exception as e:
        raise Exception(f"Report generation failed: {str(e)}")


async def generate_report_stream(report_id: str, query: str) -> AsyncIterator[str]:
    """
    Generate report with streaming support per specification Section 5 & 9
    Uses LangChain streaming to yield sections progressively (Gemini-style)

    Yields JSON chunks in SSE format:
    - {"type": "section", "section_num": N, "heading": "...", "content": "...", "citations": [...]}
    - {"type": "complete", "report_id": "..."}
    - {"type": "error", "message": "..."}
    """
    # Validate UK-only query
    if not is_uk_query(query):
        error_msg = (
            "Query must be related to studying in the United Kingdom. "
            "Please specify UK universities, courses, or migration."
        )
        yield json.dumps({"type": "error", "message": error_msg})
        return

    try:
        # Create streaming-enabled LLM
        llm_stream = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            google_api_key=settings.GEMINI_API_KEY,
            temperature=0.3,
            streaming=True,  # Enable streaming
        )

        # Create prompt
        prompt = f"""Generate a comprehensive research report for the following UK study query:

QUERY: {query}

Provide detailed, factual information with proper citations.
Remember: UK-specific information only!"""

        messages = [
            SystemMessage(content=UK_SYSTEM_PROMPT),
            HumanMessage(content=prompt),
        ]

        # Accumulate response chunks
        full_response = ""

        # Stream response from LLM
        async for chunk in llm_stream.astream(messages):
            content = chunk.content
            full_response += content

            # Yield raw chunk for progressive rendering
            # Note: This yields incremental text, not complete sections
            # Frontend should accumulate and parse complete JSON
            yield json.dumps(
                {
                    "type": "chunk",
                    "content": content,
                    "report_id": report_id,
                }
            )

        # Parse complete response
        try:
            report_data = json.loads(full_response)

            # Validate and yield complete sections
            sections = []
            for i, section_data in enumerate(report_data.get("sections", []), 1):
                citations = [
                    Citation(
                        title=cit["title"],
                        url=cit["url"],
                        snippet=cit.get("snippet", ""),
                        accessed_at=datetime.utcnow(),
                    )
                    for cit in section_data.get("citations", [])
                ]

                section = ReportSection(
                    heading=section_data["heading"],
                    content=section_data["content"],
                    citations=citations,
                )
                sections.append(section)

                # Yield complete section
                yield json.dumps(
                    {
                        "type": "section",
                        "section_num": i,
                        "heading": section.heading,
                        "content": section.content,
                        "citations": [c.dict() for c in section.citations],
                    }
                )

            # Validate report structure (will raise if invalid)
            total_citations = sum(len(s.citations) for s in sections)
            # Validation via model instantiation
            ReportContent(
                query=query,
                summary=report_data.get("summary", ""),
                sections=sections,
                total_citations=total_citations,
                generated_at=datetime.utcnow(),
            )

            # Store complete report (TODO: integrate with report_service)
            # await store_report(report_id, ReportContent(...))

        except json.JSONDecodeError as e:
            yield json.dumps(
                {"type": "error", "message": f"Failed to parse AI response as JSON: {str(e)}"}
            )
            return
        except ValueError as e:
            # Pydantic validation error (wrong sections, missing citations, etc.)
            yield json.dumps({"type": "error", "message": f"Report validation failed: {str(e)}"})
            return

    except Exception as e:
        yield json.dumps({"type": "error", "message": f"Report generation failed: {str(e)}"})
        return


def is_uk_query(query: str) -> bool:
    """
    Validate that query is related to UK study/migration
    """
    uk_keywords = [
        "uk",
        "united kingdom",
        "britain",
        "british",
        "england",
        "scotland",
        "wales",
        "northern ireland",
        "london",
        "oxford",
        "cambridge",
        "russell group",
        "ucas",
    ]

    query_lower = query.lower()
    return any(keyword in query_lower for keyword in uk_keywords)
