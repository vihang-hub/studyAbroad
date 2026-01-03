"""
Tests for AI service (Gemini 2.0 Flash report generation)
"""
import pytest
from unittest.mock import patch, Mock
import json
from datetime import datetime
from src.api.services.ai_service import (
    generate_report,
    is_uk_query,
    generate_report_stream,
)
from src.api.models.report import ReportContent, ReportSection, Citation


class TestIsUKQuery:
    """Test suite for UK query validation"""

    def test_is_uk_query_with_uk_keyword(self):
        """Test query containing 'UK' is validated as UK query"""
        assert is_uk_query("Best UK universities for Computer Science") is True

    def test_is_uk_query_with_united_kingdom(self):
        """Test query with 'United Kingdom' is validated"""
        assert is_uk_query("Studying in the United Kingdom") is True

    def test_is_uk_query_with_britain(self):
        """Test query with 'Britain' is validated"""
        assert is_uk_query("British universities for medicine") is True

    def test_is_uk_query_with_london(self):
        """Test query with 'London' is validated"""
        assert is_uk_query("London universities") is True

    def test_is_uk_query_with_oxford(self):
        """Test query with 'Oxford' is validated"""
        assert is_uk_query("Oxford Computer Science program") is True

    def test_is_uk_query_with_cambridge(self):
        """Test query with 'Cambridge' is validated"""
        assert is_uk_query("Cambridge University admissions") is True

    def test_is_uk_query_with_russell_group(self):
        """Test query with 'Russell Group' is validated"""
        assert is_uk_query("Russell Group universities") is True

    def test_is_uk_query_with_ucas(self):
        """Test query with 'UCAS' is validated"""
        assert is_uk_query("UCAS application process") is True

    def test_is_uk_query_case_insensitive(self):
        """Test UK validation is case insensitive"""
        assert is_uk_query("uk universities") is True
        assert is_uk_query("UK UNIVERSITIES") is True
        assert is_uk_query("uK UnIvErSiTiEs") is True

    def test_is_not_uk_query_usa(self):
        """Test non-UK query (USA) is rejected"""
        assert is_uk_query("Best universities in USA") is False

    def test_is_not_uk_query_canada(self):
        """Test non-UK query (Canada) is rejected"""
        assert is_uk_query("Canadian universities") is False

    def test_is_not_uk_query_australia(self):
        """Test non-UK query (Australia) is rejected"""
        assert is_uk_query("Study in Australia") is False

    def test_is_not_uk_query_generic(self):
        """Test generic query without country is rejected"""
        assert is_uk_query("Best universities for Computer Science") is False


class TestGenerateReport:
    """Test suite for report generation"""

    @pytest.mark.asyncio
    async def test_generate_report_success(self, sample_uk_query):
        """Test successful report generation with all sections"""
        from src.api.models.report import REQUIRED_SECTIONS

        mock_response_data = {
            "query": sample_uk_query,
            "summary": "UK universities offer excellent Computer Science programs",
            "sections": [
                {
                    "heading": REQUIRED_SECTIONS[i],
                    "content": f"Content for section {i+1}",
                    "citations": [
                        {
                            "title": f"Source {i+1}-{j+1}",
                            "url": f"https://example.com/source{i+1}-{j+1}",
                            "snippet": "Relevant information",
                        }
                        for j in range(3 if REQUIRED_SECTIONS[i] not in ["Executive Summary", "Sources & Citations"] else 0)
                    ],
                }
                for i in range(10)
            ],
        }

        with patch("src.api.services.ai_service.llm") as mock_llm:
            mock_response = Mock()
            mock_response.content = json.dumps(mock_response_data)
            mock_llm.invoke.return_value = mock_response

            result = await generate_report(sample_uk_query)

            assert isinstance(result, ReportContent)
            assert result.query == sample_uk_query
            assert len(result.sections) == 10
            # 8 sections with 3 citations each = 24 total
            # (Executive Summary and Sources & Citations have 0 citations)
            assert result.total_citations == 24
            assert all(isinstance(section, ReportSection) for section in result.sections)

    @pytest.mark.asyncio
    async def test_generate_report_non_uk_query(self, sample_non_uk_query):
        """Test report generation rejects non-UK queries"""
        with pytest.raises(ValueError) as exc_info:
            await generate_report(sample_non_uk_query)

        assert "United Kingdom" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_generate_report_insufficient_sections(self, sample_uk_query):
        """Test report generation fails with insufficient sections"""
        mock_response_data = {
            "query": sample_uk_query,
            "summary": "Test summary",
            "sections": [
                {
                    "heading": "Executive Summary",
                    "content": "Content",
                    "citations": [],
                }
            ],  # Only 1 section instead of 10
        }

        with patch("src.api.services.ai_service.llm") as mock_llm:
            mock_response = Mock()
            mock_response.content = json.dumps(mock_response_data)
            mock_llm.invoke.return_value = mock_response

            with pytest.raises(Exception) as exc_info:
                await generate_report(sample_uk_query)

            assert "10 sections" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_generate_report_no_citations(self, sample_uk_query):
        """Test report generation fails without citations"""
        from src.api.models.report import REQUIRED_SECTIONS

        mock_response_data = {
            "query": sample_uk_query,
            "summary": "Test summary",
            "sections": [
                {
                    "heading": REQUIRED_SECTIONS[i],
                    "content": "Content",
                    "citations": [],  # No citations
                }
                for i in range(10)
            ],
        }

        with patch("src.api.services.ai_service.llm") as mock_llm:
            mock_response = Mock()
            mock_response.content = json.dumps(mock_response_data)
            mock_llm.invoke.return_value = mock_response

            with pytest.raises(Exception) as exc_info:
                await generate_report(sample_uk_query)

            assert "citation" in str(exc_info.value).lower()

    @pytest.mark.asyncio
    async def test_generate_report_invalid_json(self, sample_uk_query):
        """Test report generation handles invalid JSON response"""
        with patch("src.api.services.ai_service.llm") as mock_llm:
            mock_response = Mock()
            mock_response.content = "Invalid JSON {{"
            mock_llm.invoke.return_value = mock_response

            with pytest.raises(ValueError) as exc_info:
                await generate_report(sample_uk_query)

            assert "JSON" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_generate_report_llm_error(self, sample_uk_query):
        """Test report generation handles LLM errors"""
        with patch("src.api.services.ai_service.llm") as mock_llm:
            mock_llm.invoke.side_effect = Exception("LLM API Error")

            with pytest.raises(Exception) as exc_info:
                await generate_report(sample_uk_query)

            assert "Report generation failed" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_generate_report_citations_structure(self, sample_uk_query):
        """Test report citations have correct structure"""
        from src.api.models.report import REQUIRED_SECTIONS

        mock_response_data = {
            "query": sample_uk_query,
            "summary": "Test summary",
            "sections": [
                {
                    "heading": REQUIRED_SECTIONS[i],
                    "content": "Content",
                    "citations": [
                        {
                            "title": f"Test Source {j+1}",
                            "url": f"https://example.com/source{j+1}",
                            "snippet": "Test snippet",
                        }
                        for j in range(3 if REQUIRED_SECTIONS[i] not in ["Executive Summary", "Sources & Citations"] else 0)
                    ],
                }
                for i in range(10)
            ],
        }

        with patch("src.api.services.ai_service.llm") as mock_llm:
            mock_response = Mock()
            mock_response.content = json.dumps(mock_response_data)
            mock_llm.invoke.return_value = mock_response

            result = await generate_report(sample_uk_query)

            # Check first section with citations (section 1, index 1)
            # Section 0 is Executive Summary which has no citations
            section_with_citations = result.sections[1]
            assert len(section_with_citations.citations) == 3

            first_citation = section_with_citations.citations[0]
            assert isinstance(first_citation, Citation)
            assert first_citation.title == "Test Source 1"
            assert first_citation.url == "https://example.com/source1"
            assert first_citation.snippet == "Test snippet"
            assert isinstance(first_citation.accessed_at, datetime)


class TestGenerateReportStream:
    """Test suite for streaming report generation"""

    @pytest.mark.asyncio
    async def test_generate_report_stream(self, sample_uk_query):
        """Test streaming report generation"""
        from src.api.models.report import REQUIRED_SECTIONS

        mock_response_data = {
            "query": sample_uk_query,
            "summary": "Test",
            "sections": [
                {
                    "heading": REQUIRED_SECTIONS[i],
                    "content": "Content",
                    "citations": [
                        {
                            "title": f"Source {j+1}",
                            "url": f"https://example.com/source{j+1}",
                            "snippet": "Info",
                        }
                        for j in range(3 if REQUIRED_SECTIONS[i] not in ["Executive Summary", "Sources & Citations"] else 0)
                    ],
                }
                for i in range(10)
            ],
        }

        # Mock the async streaming LLM
        async def mock_astream(messages):
            """Mock async stream that yields the complete response"""
            content = json.dumps(mock_response_data)
            # Simulate streaming by yielding the whole content at once
            mock_chunk = Mock()
            mock_chunk.content = content
            yield mock_chunk

        with patch("src.api.services.ai_service.ChatGoogleGenerativeAI") as mock_llm_class:
            mock_llm_instance = Mock()
            mock_llm_instance.astream = mock_astream
            mock_llm_class.return_value = mock_llm_instance

            chunks = []
            async for chunk in generate_report_stream("report_123", sample_uk_query):
                chunks.append(chunk)

            # Should have: 1 chunk event + 10 section events
            assert len(chunks) >= 1

            # Verify at least one chunk was yielded
            chunk_types = [json.loads(c)["type"] for c in chunks]
            assert "chunk" in chunk_types or "section" in chunk_types
