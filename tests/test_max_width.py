from tablebuilder import resolve_max_width, TableSeparator

headers = ['This is a long header', 'Short', None]
rows = [
    ['short', 'Super Long Row', 'Longer Row'],
    TableSeparator(),
    ['short', 'Less Long'],
    ['short', None, 'cell'],
    [None, 'short', 'cell'],
    ['marker', 'short', 'cell']
]


def test_null_headers():
    max_length = resolve_max_width(1, [], rows)
    assert max_length == 14


def test_empty_column():
    max_length = resolve_max_width(2, headers, rows)
    assert max_length == 10


def test_header_max():
    max_length = resolve_max_width(0, headers, rows)
    assert max_length == 21


def test_out_of_index():
    max_length = resolve_max_width(3, headers, rows)
    assert max_length == 0
