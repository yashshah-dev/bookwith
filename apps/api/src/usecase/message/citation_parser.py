"""Citation information parser."""

import logging
import re
from typing import TypedDict

logger = logging.getLogger(__name__)


class CitationData(TypedDict):
    """Citation data type definition."""

    marker: str
    number: str
    chapter: str
    position_percent: float | None
    cfi: str | None
    location_info: str | None
    is_highlight: bool | None


class CitationResult(TypedDict):
    """Citation extraction result type definition."""

    citations: list[CitationData]
    has_citations: bool
    markers_found: list[str]


class CitationParser:
    """Parser for extracting citation information from AI responses."""

    # Superscript number mapping
    SUPERSCRIPT_MAP = {
        "¹": "1",
        "²": "2",
        "³": "3",
        "⁴": "4",
        "⁵": "5",
        "⁶": "6",
        "⁷": "7",
        "⁸": "8",
        "⁹": "9",
    }

    # Reverse mapping (from number to superscript character)
    REVERSE_SUPERSCRIPT_MAP = {v: k for k, v in SUPERSCRIPT_MAP.items()}

    @classmethod
    def extract_citations(cls, text: str) -> CitationResult:
        """Extract citation information from text.

        Args:
            text: AI response text

        Returns:
            Dictionary containing citation information

        """
        citations = []

        # Detect superscript numbers in the main text
        superscript_pattern = r"[¹²³⁴⁵⁶⁷⁸⁹]"
        markers_in_text = re.findall(superscript_pattern, text)

        # Look for "Reference Location:" section
        reference_section_match = re.search(r"参照箇所[：:]\s*\n((?:.*\n?)*)", text, re.MULTILINE)

        if reference_section_match:
            reference_section = reference_section_match.group(1)

            # Parse each reference line
            # Pattern: ¹ Chapter 3: Title (about 25% position)
            reference_pattern = r"([¹²³⁴⁵⁶⁷⁸⁹])\s+([^（]+)（約(\d+(?:\.\d+)?)%の位置）"

            for match in re.finditer(reference_pattern, reference_section):
                marker = match.group(1)
                chapter_info = match.group(2).strip()

                try:
                    position_percent = float(match.group(3))
                except ValueError:
                    logger.warning(f"Invalid position percent: {match.group(3)}")
                    position_percent = 0.0

                citations.append(
                    CitationData(
                        marker=marker,
                        number=cls.SUPERSCRIPT_MAP.get(marker, "?"),
                        chapter=chapter_info,
                        position_percent=position_percent,
                        cfi=None,  # CFI information to be added in the future
                        location_info=None,
                        is_highlight=None,
                    )
                )

        # Also detect highlight citations (★ marker)
        highlight_pattern = r"(★\d+)\s+([^（]+)（([^）]+)）"

        for match in re.finditer(highlight_pattern, text):
            marker = match.group(1)
            chapter_info = match.group(2).strip()
            location_info = match.group(3)

            # For highlights, position information may be different
            citations.append(
                CitationData(
                    marker=marker,
                    number=marker[1:],  # Number without ★
                    chapter=chapter_info,
                    position_percent=None,  # Highlights may not have position %
                    location_info=location_info,
                    is_highlight=True,
                    cfi=None,
                )
            )

        return CitationResult(
            citations=citations,
            has_citations=len(citations) > 0,
            markers_found=list(set(markers_in_text)),
        )

    @classmethod
    def add_citation_links(cls, text: str, citations: list[CitationData]) -> str:
        """Convert citation markers in text to linkable format.

        Surround markers with special tags for easy frontend processing.

        Args:
            text: Original text
            citations: List of citation information

        Returns:
            Text with markers surrounded by tags

        """
        # Add type checking
        if not isinstance(text, str):
            raise TypeError("text must be a string")
        if not isinstance(citations, list):
            raise TypeError("citations must be a list")

        result = text

        # Surround citation markers with tags
        for citation in citations:
            marker = citation["marker"]
            # Example: ¹ → <citation-link marker="¹" index="0">¹</citation-link>
            # Frontend will detect this tag and convert to links
            replacement = f'<citation-link marker="{marker}" number="{citation["number"]}">{marker}</citation-link>'
            result = result.replace(marker, replacement)

        return result
