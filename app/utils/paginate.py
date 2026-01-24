from flask import request

from utils.log import Log


def paginate_query(query, per_page=9):
    """Return paginated data for a SQLAlchemy query.

    Args:
        query: SQLAlchemy query object.
        per_page: Number of items per page.

    Returns:
        tuple: (items, page, total_pages)
    """
    page = request.args.get("page", 1, type=int)

    Log.info(f"Paginating query, page {page}, per_page {per_page}")

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    items = pagination.items
    total_pages = max(pagination.pages, 1)

    return items, page, total_pages
