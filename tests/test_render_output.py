from tablebuilder import Table, TableSeparator


def output_wrapper(output):
    def write_line(self, message, style):
        output.append(message)

    return write_line


def build_table():
    table = Table(terminal_width=80)
    table.headers = ['ISBN', 'Title', 'Author']
    table.rows = [
        ['99921-58-10-7', 'Divine Comedy', 'Dante Alighieri'],
        ['9971-5-0210-0', 'A Tale of Two Cities', 'Charles Dickens']
    ]
    table.rows.append(TableSeparator())
    table.rows.append(['80-902734-1-6', 'And Then There Were None Is A Really Long Title', 'Agatha Christie'])
    table.rows.append(['960-425-059-0', 'The Lord of the Rings', 'J. R. R. Tolkien'])
    return table


def test_basic_render():
    output = []
    mnkyptch_write_line = output_wrapper(output)
    Table.write_line = mnkyptch_write_line
    table = build_table()
    table.render()
    comparison = (
        "+=============+===============================================+================+\n"
        "| ISBN        | Title                                         | Author         |\n"
        "+=============+===============================================+================+\n"
        "| 99921-58-10 | Divine Comedy                                 | Dante          |\n"
        "| -7          |                                               | Alighieri      |\n"
        "| 9971-5-0210 | A Tale of Two Cities                          | Charles        |\n"
        "| -0          |                                               | Dickens        |\n"
        "+=============+===============================================+================+\n"
        "| 80-902734-1 | And Then There Were None Is A Really Long     | Agatha         |\n"
        "| -6          | Title                                         | Christie       |\n"
        "| 960-425-059 | The Lord of the Rings                         | J. R. R.       |\n"
        "| -0          |                                               | Tolkien        |\n"
        "+=============+===============================================+================+"
    )
    assert comparison == "\n".join(output)


def test_column_widths():
    output = []
    mnkyptch_write_line = output_wrapper(output)
    Table.write_line = mnkyptch_write_line
    table = build_table()
    table.column_widths = [0, 35, None]
    table.render()
    comparison = (
        "+===============+=====================================+========================+\n"
        "| ISBN          | Title                               | Author                 |\n"
        "+===============+=====================================+========================+\n"
        "| 99921-58-10-7 | Divine Comedy                       | Dante Alighieri        |\n"
        "| 9971-5-0210-0 | A Tale of Two Cities                | Charles Dickens        |\n"
        "+===============+=====================================+========================+\n"
        "| 80-902734-1-6 | And Then There Were None Is A       | Agatha Christie        |\n"
        "|               | Really Long Title                   |                        |\n"
        "| 960-425-059-0 | The Lord of the Rings               | J. R. R. Tolkien       |\n"
        "+===============+=====================================+========================+"
    )
    assert comparison == "\n".join(output)


