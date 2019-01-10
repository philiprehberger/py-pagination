# philiprehberger-pagination

[![Tests](https://github.com/philiprehberger/py-pagination/actions/workflows/publish.yml/badge.svg)](https://github.com/philiprehberger/py-pagination/actions/workflows/publish.yml)
[![PyPI version](https://img.shields.io/pypi/v/philiprehberger-pagination.svg)](https://pypi.org/project/philiprehberger-pagination/)
[![License](https://img.shields.io/github/license/philiprehberger/py-pagination)](LICENSE)

Cursor and offset pagination utilities for any data source.

## Installation

```bash
pip install philiprehberger-pagination
```

## Usage

```python
from philiprehberger_pagination import paginate

items = list(range(100))
page = paginate(items, page=2, per_page=25)

print(page.items)     # [25, 26, ..., 49]
print(page.pages)     # 4
print(page.has_next)  # True
```

### Cursor Pagination

```python
from philiprehberger_pagination import CursorPage

rows = [{"id": 1, "name": "a"}, {"id": 2, "name": "b"}, {"id": 3, "name": "c"}]
page = CursorPage.encode(rows, key="id", limit=2)

print(page.items)       # first 2 rows
print(page.has_more)    # True
print(page.next_cursor) # base64-encoded cursor

decoded = CursorPage.decode(page.next_cursor)
print(decoded)  # {"id": 2}
```

## API

| Function / Class | Description |
|------------------|-------------|
| `paginate(items, page, per_page)` | Offset-paginate a list and return a `Page` |
| `Page.items` | Items on the current page |
| `Page.total` | Total number of items |
| `Page.page` | Current page number (1-based) |
| `Page.per_page` | Items per page |
| `Page.pages` | Total number of pages |
| `Page.has_next` | Whether a next page exists |
| `Page.has_prev` | Whether a previous page exists |
| `CursorPage.encode(items, key, limit)` | Build a cursor page from a list of items |
| `CursorPage.decode(cursor)` | Decode a cursor string back to a dict |
| `CursorPage.items` | Items on the current page |
| `CursorPage.next_cursor` | Encoded cursor for the next page |
| `CursorPage.has_more` | Whether more items exist |

## Development

```bash
pip install -e .
python -m pytest tests/ -v
```

## License

MIT
