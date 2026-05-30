from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PageRange:
    start: int
    end: int
    label: str = ""

    @property
    def page_count(self) -> int:
        return self.end - self.start + 1


def parse_page_ranges(text: str, total_pages: int, allow_overlap: bool = False) -> list[PageRange]:
    """Parse 1-based page ranges such as "1-3, 5, 8-end"."""
    if total_pages < 1:
        raise ValueError("PDF has no pages.")
    if not text or not text.strip():
        raise ValueError("Enter at least one page range.")

    ranges: list[PageRange] = []
    seen: set[int] = set()
    for raw_part in text.replace(";", ",").split(","):
        part = raw_part.strip().lower()
        if not part:
            continue
        if "-" in part:
            left, right = [chunk.strip() for chunk in part.split("-", 1)]
        else:
            left, right = part, part
        start = _parse_bound(left, total_pages)
        end = _parse_bound(right, total_pages)
        if start > end:
            raise ValueError(f"Invalid range '{raw_part.strip()}': start is after end.")
        if start < 1 or end > total_pages:
            raise ValueError(f"Range '{raw_part.strip()}' is outside 1-{total_pages}.")
        pages = set(range(start, end + 1))
        if not allow_overlap and pages.intersection(seen):
            raise ValueError(f"Range '{raw_part.strip()}' overlaps an earlier range.")
        seen.update(pages)
        ranges.append(PageRange(start=start, end=end, label=f"{start}-{end}"))

    if not ranges:
        raise ValueError("Enter at least one page range.")
    return ranges


def _parse_bound(value: str, total_pages: int) -> int:
    if value in {"end", "last"}:
        return total_pages
    try:
        return int(value)
    except ValueError as exc:
        raise ValueError(f"Invalid page value '{value}'.") from exc
