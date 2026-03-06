"""
blueprints/query_utils.py — Reusable sorting, filtering and pagination helper.

Usage
-----
In any blueprint get_all() view:

    from .query_utils import apply_list_params

    @bp.route('')
    def get_all():
        items, meta = apply_list_params(
            MyModel,
            MyModel.query,
            filterable={
                'name':   'like',   # partial, case-insensitive LIKE
                'city':   'exact',  # equality (also handles bool coercion)
                'active': 'exact',
            },
            sortable=['id', 'name', 'city'],
        )
        return jsonify({'data': [MyDTO.from_model(i) for i in items], 'pagination': meta})

Query-string parameters accepted
---------------------------------
  ?page=1          — page number, 1-based (default 1)
  ?per_page=20     — page size, capped at MAX_PER_PAGE (default 20)
  ?sort=name       — field to sort by; must be in *sortable* (default "id")
  ?order=asc|desc  — sort direction (default "asc")
  ?<field>=<value> — filter by field; must be in *filterable*

Response envelope
-----------------
{
  "data": [...],
  "pagination": {
    "page": 1,
    "perPage": 20,
    "total": 135,
    "totalPages": 7
  }
}
"""

from flask import request
from sqlalchemy import asc, desc

_DEFAULT_PAGE     = 1
_DEFAULT_PER_PAGE = 20
_MAX_PER_PAGE     = 100


def apply_list_params(model, query, filterable: dict, sortable: list):
    """
    Apply filters, ordering and pagination from the current request's query-string.

    Parameters
    ----------
    model       : SQLAlchemy model class (used to resolve column attributes).
    query       : Base SQLAlchemy Query to build on.
    filterable  : Mapping of {column_name: 'like'|'exact'}.
                  'like'  → case-insensitive substring match.
                  'exact' → equality; bool columns accept 'true'/'false'.
    sortable    : List of column names that may be used as sort keys.

    Returns
    -------
    (items, pagination_meta)
      items          : list of ORM instances for the current page.
      pagination_meta: dict ready to be JSON-serialised.
    """
    # ------------------------------------------------------------------ filters
    for field, mode in filterable.items():
        value = request.args.get(field)
        if value is None:
            continue
        col = getattr(model, field)
        if mode == 'like':
            query = query.filter(col.like(f'%{value}%'))
        else:
            coerced = _coerce(col, value)
            query = query.filter(col == coerced)

    # ------------------------------------------------------------------ sorting
    sort_field = request.args.get('sort', 'id')
    sort_dir   = request.args.get('order', 'asc').lower()
    if sort_field in sortable:
        col = getattr(model, sort_field)
        query = query.order_by(desc(col) if sort_dir == 'desc' else asc(col))
    else:
        query = query.order_by(asc(model.id))

    # --------------------------------------------------------------- pagination
    try:
        page     = max(1, int(request.args.get('page',     _DEFAULT_PAGE)))
        per_page = min(_MAX_PER_PAGE, max(1, int(request.args.get('per_page', _DEFAULT_PER_PAGE))))
    except (ValueError, TypeError):
        page, per_page = _DEFAULT_PAGE, _DEFAULT_PER_PAGE

    total = query.count()
    items = query.offset((page - 1) * per_page).limit(per_page).all()

    return items, {
        'page':       page,
        'perPage':    per_page,
        'total':      total,
        'totalPages': (total + per_page - 1) // per_page if per_page else 1,
    }


# --------------------------------------------------------------------------- #

def _coerce(col, value: str):
    """Coerce a query-string string value to the column's Python type."""
    try:
        python_type = col.property.columns[0].type.python_type
        if python_type is bool:
            return value.lower() in ('true', '1', 'yes')
        if python_type is int:
            return int(value)
        if python_type is float:
            return float(value)
    except (NotImplementedError, AttributeError):
        pass
    return value
