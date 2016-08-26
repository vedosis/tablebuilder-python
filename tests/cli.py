import click


@click.command()
def main():
    from tablebuilder import Table, TableStyle, TableSeparator

    table = Table()
    table.headers = ['ISBN', 'Title', 'Author']
    table.rows = [
        ['99921-58-10-7', 'Divine Comedy', 'Dante Alighieri'],
        ['9971-5-0210-0', 'A Tale of Two Cities', 'Charles Dickens']
    ]
    table.render()

    table.rows.append(TableSeparator())
    table.rows.append(['80-902734-1-6', 'And Then There Were None Is A Really Long Title', 'Agatha Christie'])
    table.rows.append(['960-425-059-0', 'The Lord of the Rings', 'J. R. R. Tolkien'])
    table.render()

    table.column_widths = [0, 35, None]
    table.render()

    table.column_widths[1] = 25
    table.render()

    table.padding = 2
    table.padding_char = "."
    table.borders.horizontal_char = u'\u2501'
    table.borders.vertical_char = u'\u2503'
    table.borders.crossing_char = u'\u254B'
    table.render()

    table.style = TableStyle.Compact
    table.render()

    table.style = TableStyle.Borderless
    table.render()

    table.style = TableStyle.Unicode
    table.render()

    table.style = TableStyle.Default
    table.render()

    table.add_column(['Religion', 'Depression', 'Fantasy', 'Mystery'], header="Genre", width=None)
    table.render()

    table.borders.horizontal_char = "I"
    table.borders.vertical_char = "~"
    table.borders.crossing_char = "X"
    table.render()

    table.padding = False
    table.render()

    table.padding = True
    table.padding_char = "="
    table.render()

    table.add_row([TableCell('Der Things', col_span=2), 'Nobody', 'Other'])
    table.render()


if __name__ == '__main__':
    main()
