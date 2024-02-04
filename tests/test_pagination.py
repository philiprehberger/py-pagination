"""Tests for philiprehberger_pagination."""

from __future__ import annotations

from philiprehberger_pagination import CursorPage, Page, paginate


class TestPaginate:
    def test_basic(self) -> None:
        items = list(range(50))
        page = paginate(items, page=1, per_page=10)

        assert isinstance(page, Page)
        assert page.items == list(range(10))
        assert page.total == 50
        assert page.page == 1
        assert page.per_page == 10
        assert page.pages == 5

    def test_last_page(self) -> None:
        items = list(range(23))
        page = paginate(items, page=3, per_page=10)

        assert page.items == [20, 21, 22]
        assert page.total == 23
        assert page.pages == 3

    def test_has_next(self) -> None:
        items = list(range(30))
        page1 = paginate(items, page=1, per_page=10)
        page3 = paginate(items, page=3, per_page=10)

        assert page1.has_next is True
        assert page3.has_next is False

    def test_has_prev(self) -> None:
        items = list(range(30))
        page1 = paginate(items, page=1, per_page=10)
        page2 = paginate(items, page=2, per_page=10)

        assert page1.has_prev is False
        assert page2.has_prev is True


class TestCursorPage:
    def test_encode_decode_roundtrip(self) -> None:
        items = [{"id": i, "name": f"item-{i}"} for i in range(5)]
        page = CursorPage.encode(items, key="id", limit=10)

        assert len(page.items) == 5
        assert page.has_more is False
        assert page.next_cursor is not None

        decoded = CursorPage.decode(page.next_cursor)
        assert decoded == {"id": 4}

    def test_has_more(self) -> None:
        items = [{"id": i} for i in range(6)]
        page = CursorPage.encode(items, key="id", limit=5)

        assert len(page.items) == 5
        assert page.has_more is True

        decoded = CursorPage.decode(page.next_cursor)
        assert decoded == {"id": 4}

    def test_empty_items(self) -> None:
        page = CursorPage.encode([], key="id", limit=10)

        assert page.items == []
        assert page.next_cursor is None
        assert page.has_more is False


class TestToDict:
    def test_page_to_dict(self) -> None:
        page = paginate(list(range(50)), page=1, per_page=10)
        d = page.to_dict()
        assert d["items"] == list(range(10))
        assert d["total"] == 50
        assert d["pages"] == 5
        assert d["has_next"] is True
        assert d["has_prev"] is False

    def test_cursor_page_to_dict(self) -> None:
        items = [{"id": i} for i in range(5)]
        page = CursorPage.encode(items, key="id", limit=10)
        d = page.to_dict()
        assert d["items"] == items
        assert d["has_more"] is False
        assert "next_cursor" in d
