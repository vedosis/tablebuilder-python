from enum import Enum
from math import floor, ceil

import click


class TableStyle(Enum):
    Compact = 'compact'
    Borderless = 'borderless'
    Unicode = 'unicode'
    Default = 'default'


class TableSeparator(object):
    def __len__(self):
        return 0


class TableBorder(object):
    crossing_char = "+"
    horizontal_char = "="
    vertical_char = "|"


def truncate_line(string, width):
    """
    Takes in a string and tries to break it on spaces. If there aren't sufficient spaces, breaks on character count
    :param str string: Intended string to break up... duh.
    :param int width: Max width to break the string upon.
    :rtype: tuple[str, str]
    """
    if len(string) <= width:
        return string, None

    pieces = string.split(" ")
    if len(pieces[0]) > width:
        return string[0:width], string[width:]

    for i in range(len(pieces)):
        if len(" ".join(pieces[0:i + 1])) > width:
            if i <= 1:
                return pieces[0], " ".join(pieces[1:])
            return " ".join(pieces[0:i]), " ".join(pieces[i:])


def resolve_max_width(index_position, headers, rows):
    """
    Given an index, get the max length of column data.
    :param int index_position: index to compare
    :param list[str] headers: The headers of the table object
    :param list[list[str]] rows: The rows of the table object
    :rtype: int
    """
    try:
        header_value = headers[index_position]
    except IndexError:
        header_value = ""

    if header_value is None:
        header_value = ""

    row_values = []
    for i in range(len(rows[0:20])):
        try:
            if not isinstance(rows[i], TableSeparator) and rows[i][index_position] is not None:
                row_values.append(len(rows[i][index_position]))
        except IndexError:
            row_values.append(0)
    return max(
        len(header_value),
        *row_values
    )


def resolve_min_width(index_position, headers, rows):
    """
    Evaluates what is the largest single word.
    :param int index_position: index of the column to evaluate.
    :param list[str|None] headers: A list of the Table headers
    :param list[list[str]] rows: All the Table Rows
    :rtype: int
    """
    header_max = 0
    if headers[index_position] is not None:
        header_max = max([len(x) for x in headers[index_position].split(" ")])

    row_max = 0
    if len(rows):
        row_max = max([max(len(word) for word in x[index_position].split(' ')) for x in rows if len(x) > index_position])
    return max([row_max, header_max])


def reduce_by_list(current_width, reduction_amount, column_widths, index_list, min_width):
    """
    Reduces a list of column widths to the correct width
    :param int current_width: the current width of the columns
    :param int reduction_amount: intended reduction amount
    :param list[int] column_widths: current column width list
    :param list[int] index_list: a lists of indexes that can be reduced.
    :param int min_width: minimum with a column can be
    :rtype: int
    """
    if len(index_list):
        intended_reduction = int(ceil(reduction_amount / len(index_list)))
        for index in index_list:
            if column_widths[index] - intended_reduction >= min_width:
                column_widths[index] -= intended_reduction
                current_width -= intended_reduction
    return current_width


def generate_border_columns(num_data_cols, padding_width=1, padding_char=" ", border_char="|"):
    """
    Creates the padding/border columns for the number of columns provided.
    :param int num_data_cols: total number of data columns
    :param int padding_width: width of the padding between the data columns
    :param str padding_char: actual character to print.
    :param str border_char: character to be used as the border
    :rtype: list[str]
    """

    if len(border_char) > 1:
        border_char = border_char[0]

    border_columns = []
    for i in range(num_data_cols + 1):
        if len(border_char):
            border = ""
            if i != 0:
                border += padding_char * padding_width
            border += border_char
            if i != num_data_cols:
                border += padding_char * padding_width

            border_columns.append(border)
        else:
            border_columns.append(padding_char * padding_width)
    return border_columns


def resolve_column_widths_and_borders(column_widths, headers, rows, padding, padding_char, border_char, terminal_width):
    """
    Reduces the column widths and returns the correct width
    :param list[int] column_widths: the known column widths
    :param list[str] headers: list of headers
    :param list[list[str]] rows: list of all the data rows
    :param int padding: how many padding characters to add to either side of a border
    :param str padding_char: the character to be used for padding
    :param str border_char: the character to be used as a horizontal border
    :param int terminal_width: how wide the characters should be before trimming
    :rtype: tuple[list[int], list[str]]
    """
    # setting all the missing columns to exact width
    for i in range(len(headers) - len(column_widths)):
        column_widths.append(0)
    for i in range(max(*[len(x) for x in rows]) - len(column_widths)):
        column_widths.append(0)

    borders = generate_border_columns(len(column_widths), padding, padding_char, border_char)
    border_length = sum([len(x) for x in borders])
    terminal_width_after_borders = terminal_width - border_length

    zeros = []
    nones = []
    floats = []
    ints = []
    for key, value in enumerate(column_widths):
        if value == 0:
            zeros.append(key)
        elif value is None:
            nones.append(key)
        elif isinstance(value, float):
            floats.append(key)
        elif isinstance(value, int):
            ints.append(key)
        else:
            raise ValueError("'Table.column_widths' cannot be of type '" + str(type(value)) + "'. Only int, float, None are supported.")

    for index in zeros:
        column_widths[index] = resolve_max_width(index, headers, rows)

    for index in floats:
        column_widths[index] = int(floor(terminal_width_after_borders * (column_widths[index] / 100)))

    if len(nones) > 0:
        remaining_width_for_nones = terminal_width_after_borders - sum([x for x in column_widths if x is not None])
        if remaining_width_for_nones <= 0:
            for index in nones:
                column_widths[index] = resolve_min_width(index, headers, rows)
        else:
            per_none_allotment = int(floor(remaining_width_for_nones / len(nones)))
            if per_none_allotment < len(nones):
                for index in nones:
                    column_widths[index] = resolve_min_width(index, headers, rows)
            else:
                for index in nones:
                    column_widths[index] = per_none_allotment

    current_width = border_length + sum(column_widths)
    for target_list in [nones, floats, zeros, range(len(column_widths))]:
        if current_width > terminal_width and len(target_list):
            current_width = reduce_by_list(
                current_width=current_width,
                reduction_amount=current_width - terminal_width,
                column_widths=column_widths,
                index_list=target_list,
                min_width=7
            )
    return column_widths, borders


class Table(object):
    def __init__(self, rows=None, column_widths=None, headers=None, style=None, padding_char=None, padding=None, borders=None, terminal_width=None):
        """
        Largest container for handling a single table of data
        :param list[list[str]] rows: List of a list of objects that represent the data for the Table
        :param list[int|float] column_widths: All the intended widths of columns
        :param list[str] headers: Headers to be applied to the table
        :param TableStyle|dict style: all the options to be passed into the renderer for displaying a table.
        :param str padding_char: Character to be used as padding around borders and string padding
        :param int padding: The width of padding around the borders
        :param TableBorder borders: a table border object that contains information about how borders should be rendered.
        :param int terminal_width: the maximum width of the terminal
        """
        self.rows = rows or []
        self.column_widths = column_widths or []
        self.headers = headers or []
        self.style = style or {}
        self.padding = padding or 1
        self.padding_char = padding_char or " "
        self.borders = borders or TableBorder()
        self.terminal_width = terminal_width or click.get_terminal_size()[0]

    def render(self):
        """
        Renders the table with the current settings
        :return:
        """
        column_widths, column_borders = resolve_column_widths_and_borders(
            column_widths=self.column_widths,
            headers=self.headers,
            rows=self.rows,
            padding=self.padding,
            padding_char=self.padding_char,
            border_char=self.borders.vertical_char,
            terminal_width=self.terminal_width
        )

        # Print headers and breaking row
        if len(self.headers):
            if len(self.borders.horizontal_char) > 0:
                self.print_row(TableSeparator(), widths=column_widths, borders=column_borders)
            self.print_row(self.headers, widths=column_widths, borders=column_borders)
            if len(self.borders.horizontal_char) > 0:
                self.print_row(TableSeparator(), widths=column_widths, borders=column_borders)

        # print rows
        for row in self.rows:
            self.print_row(row, widths=column_widths, borders=column_borders)

        if len(self.borders.horizontal_char) > 0:
            self.print_row(TableSeparator(), widths=column_widths, borders=column_borders)

    def print_row(self, row, widths, borders):
        """
        Prints a single row to the console
        :param list[str]|TableSeparator row:
        :param list[int] widths: column width printing (just for text)
        :param list[str] borders: border pieces to be stitched into thing
        :return:
        """
        output_string = ""
        overwidth = []
        if isinstance(row, TableSeparator):
            for i in range(len(widths) + len(borders)):
                index = int(i / 2)
                if i % 2 == 0:
                    for char in borders[index]:
                        if char == self.borders.vertical_char:
                            output_string += self.borders.crossing_char
                        else:
                            output_string += self.borders.horizontal_char
                else:
                    output_string += self.borders.horizontal_char * int(widths[index])
        else:
            for i in range(len(widths) + len(borders)):
                index = int(i / 2)
                if i % 2 == 0:
                    output_string += borders[index]
                else:
                    print_str = row[index] if row[index] is not None else self.padding_char
                    (element, overflow) = truncate_line(print_str, widths[index])
                    output_string += element.ljust(widths[index], self.padding_char)
                    overwidth.append(overflow)

        self.write_line(output_string, self.style)
        for string in overwidth:
            if string is not None:
                return self.print_row(overwidth, widths, borders)

    @staticmethod
    def write_line(message, style):
        """
        Bypass to allow monkey patching for testing
        :param str message:
        :param dict[str, str] style:
        :return:
        """
        click.secho(message, **style)
