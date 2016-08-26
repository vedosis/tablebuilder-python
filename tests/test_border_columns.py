from tablebuilder import generate_border_columns


def test_default():
    border_columns = generate_border_columns(
        num_data_cols=4
    )
    assert border_columns == ["| ", " | ", " | ", " | ", " |"]


def test_too_wide_border_char():
    border_columns = generate_border_columns(
        num_data_cols=2,
        border_char=")("
    )
    assert border_columns == [") ", " ) ", " )"]


def test_no_border():
    border_columns = generate_border_columns(
        num_data_cols=1,
        border_char=""
    )
    assert border_columns == [" ", " "]


def test_no_padding():
    border_columns = generate_border_columns(
        num_data_cols=3,
        padding_width=0
    )
    assert border_columns == ["|", "|", "|", "|"]
