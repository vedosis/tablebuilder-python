from tablebuilder import truncate_line


def test_simple_string():
    (base, overflow) = truncate_line("This is a simple string", 16)
    assert base == "This is a simple"
    assert overflow == "string"


def test_short_string():
    (base, overflow) = truncate_line("This is a short line", 20)
    assert base == "This is a short line"
    assert overflow is None


def test_short_width():
    (base, overflow) = truncate_line("Sometimes you have to truncate words", 6)
    assert base == "Someti"
    assert overflow == "mes you have to truncate words"


def test_short_first_word():
    (base, overflow) = truncate_line("In Liberty we assert", 9)
    assert base == "In"
    assert overflow == "Liberty we assert"
