"""Cursor and offset pagination utilities for any data source."""

from __future__ import annotations

import base64
import json
import math
from dataclasses import dataclass
from typing import Any, Sequence

__all__ = ["Page", "paginate", "CursorPage"]


@dataclass(frozen=True)
class Page:
    """Result of offset-based pagination."""

    items: list[Any]
    total: int
    page: int
    per_page: int

    @property
    def pages(self) -> int:
        """Total number of pages."""
        if self.total == 0:
            return 0
        return math.ceil(self.total / self.per_page)

    @property
    def has_next(self) -> bool:
        """Whether a next page exists."""
        return self.page < self.pages

    @property
    def has_prev(self) -> bool:
        """Whether a previous page exists."""
        return self.page > 1

    def to_dict(self) -> dict[str, Any]:
        """Serialize page to a dictionary."""
        return {
            "items": list(self.items),
            "total": self.total,
            "page": self.page,
            "per_page": self.per_page,
            "pages": self.pages,
            "has_next": self.has_next,
            "has_prev": self.has_prev,
        }


def paginate(items: Sequence[Any], *, page: int = 1, per_page: int = 25) -> Page:
    """Paginate a list or sequence using offset-based pagination.

    Args:
        items: The full collection to paginate.
        page: The 1-based page number to retrieve.
        per_page: Number of items per page.

    Returns:
        A Page containing the sliced items and pagination metadata.
    """
    total = len(items)
    start = (page - 1) * per_page
    end = start + per_page
    return Page(
        items=list(items[start:end]),
        total=total,
        page=page,
        per_page=per_page,
    )


@dataclass(frozen=True)
class CursorPage:
    """Result of cursor-based pagination."""

    items: list[Any]
    next_cursor: str | None
    has_more: bool

    @classmethod
    def encode(
        cls,
        items: list[Any],
        key: str,
        limit: int = 25,
    ) -> CursorPage:
        """Build a CursorPage from a list of items.

        Extracts a cursor from the last item's *key* field and base64-encodes
        it.  If ``len(items) > limit``, ``has_more`` is ``True`` and only the
        first *limit* items are included.

        Args:
            items: The items returned from a data source (may include one extra
                   to detect whether more results exist).
            key: The field name on each item used as the cursor value.
            limit: Maximum number of items to return.

        Returns:
            A CursorPage with encoded cursor and truncated item list.
        """
        has_more = len(items) > limit
        page_items = items[:limit]

        if page_items:
            last = page_items[-1]
            value = last[key] if isinstance(last, dict) else getattr(last, key)
            payload = json.dumps({key: value}, default=str)
            next_cursor = base64.b64encode(payload.encode()).decode()
        else:
            next_cursor = None

        return cls(items=page_items, next_cursor=next_cursor, has_more=has_more)

    def to_dict(self) -> dict[str, Any]:
        """Serialize cursor page to a dictionary."""
        return {
            "items": list(self.items),
            "next_cursor": self.next_cursor,
            "has_more": self.has_more,
        }

    @staticmethod
    def decode(cursor: str) -> dict[str, Any]:
        """Decode a cursor string back into its key/value dict.

        Args:
            cursor: A base64-encoded cursor string produced by ``encode``.

        Returns:
            A dict containing the key and its value.
        """
        payload = base64.b64decode(cursor.encode()).decode()
        return json.loads(payload)
