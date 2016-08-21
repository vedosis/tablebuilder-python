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
        if len(" ".join(pieces[0:i + 1])) >= width:
            if i <= 1:
                return pieces[0], " ".join(pieces[1:])
            return " ".join(pieces[0:i + 1]), " ".join(pieces[i + 1:])


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


class Table(object):
    headers = []
    rows = []
    column_widths = []
    style = {}
    padding_char = " "
    padding = True
    borders = TableBorder()

    def render(self):
        """
        Renders the table with the current settings
        :return:
        """

        max_lengths = []
        # In this instance we need to count the number of cells in each row
        # as well as the number of cells in the headers
        num_cols = max(len(self.headers), *[len(x) for x in self.rows])

        # We're trying to build up a list of how wide each column should be
        for i in range(num_cols):
            try:
                width = self.column_widths[i]
                # a typed zero width should be resolved to the exact width required for these cells
                if width == 0:
                    # The additional (1) is for padding
                    max_lengths.append(resolve_max_width(i, self.headers, self.rows))
                else:
                    max_lengths.append(width)
            except IndexError:
                # The additional (1) is for padding
                max_lengths.append(resolve_max_width(i, self.headers, self.rows))

        # terminal_height is unnecessary
        (terminal_width, terminal_height) = click.get_terminal_size()

        # flexible elements nearly guarantee we don't have console overflow
        if None in max_lengths:
            nones = []
            other = 0
            for key, value in enumerate(max_lengths):
                if value is None:
                    nones.append(key)
                else:
                    other += value
            width = floor((terminal_width - other) / len(nones))
            for missing in nones:
                max_lengths[missing] = width
        # if there's no flexible element, we need to check for console overflow
        elif sum(max_lengths) > terminal_width:
            difference = sum(max_lengths) - terminal_width
            deduction = ceil(difference / num_cols)
            # uniformly truncate the width of the cells.
            for i in range(num_cols):
                if max_lengths[i] is not None and max_lengths[i] > 1:
                    max_lengths[i] -= deduction

        # Print headers and breaking row
        if len(self.headers):
            self.print_row(self.headers, column_widths=max_lengths, max_width=terminal_width)
            self.print_row(TableSeparator(), column_widths=max_lengths, max_width=terminal_width)
        # print rows
        for row in self.rows:
            self.print_row(row, column_widths=max_lengths, max_width=terminal_width)

    def print_row(self, row, column_widths, max_width):
        """
        Prints a single row to the console
        :param list[str]|TableSeparator row:
        :param column_widths:
        :param max_width:
        :return:
        """
        if isinstance(row, TableSeparator):
            click.secho(
                self.borders.horizontal_char * min(sum(column_widths), max_width),
                **self.style
            )
            return

        output_string = ""
        new_line_array = []
        for key, element in enumerate(row):
            if element is None:
                element = ""
            if len(element) >= column_widths[key]:
                (element, overflow) = truncate_line(element, column_widths[key] - 1)
                new_line_array.append(overflow)
            else:
                new_line_array.append(None)

            output_string += element.ljust(column_widths[key], self.padding_char)

        click.secho(output_string, **self.style)
        for test in new_line_array:
            if test is not None:
                self.print_row(new_line_array, column_widths=column_widths, max_width=max_width)
                break
