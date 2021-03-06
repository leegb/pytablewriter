# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import, unicode_literals

import copy

import dataproperty
import typepy
from mbstrdecoder import MultiByteStrDecoder

from ._text_writer import IndentationTextTableWriter


class RstTableWriter(IndentationTextTableWriter):
    """
    A base class of reStructuredText table writer.
    """

    def __init__(self):
        super(RstTableWriter, self).__init__()

        self.table_name = ""
        self.char_header_row_separator = "="
        self.char_cross_point = "+"
        self.indent_string = "    "
        self.is_write_header_separator_row = True
        self.is_write_value_separator_row = True
        self.is_write_opening_row = True
        self.is_write_closing_row = True

        self._quoting_flags = copy.deepcopy(dataproperty.NOT_QUOTING_FLAGS)

    def write_table(self):
        with self._logger:
            self._write_line(self._get_table_directive())
            self._verify_property()
            self._write_table()
            if self.is_write_null_line_after_table:
                self.write_null_line()

    def _get_table_directive(self):
        if typepy.is_null_string(self.table_name):
            return ".. table:: \n"

        return ".. table:: {}\n".format(MultiByteStrDecoder(self.table_name).unicode_str)

    def _write_table(self):
        self.inc_indent_level()
        super(RstTableWriter, self)._write_table()
        self.dec_indent_level()


class RstCsvTableWriter(RstTableWriter):
    """
    A table class writer for reStructuredText
    `CSV table <http://docutils.sourceforge.net/docs/ref/rst/directives.html#id4>`__
    format.
    """

    @property
    def format_name(self):
        return "rst_csv_table"

    @property
    def support_split_write(self):
        return True

    def __init__(self):
        super(RstCsvTableWriter, self).__init__()

        self.column_delimiter = ", "
        self.char_cross_point = ""
        self.is_padding = False
        self.is_write_header_separator_row = False
        self.is_write_value_separator_row = False
        self.is_write_closing_row = False

        self._quoting_flags[typepy.Typecode.STRING] = True

    def write_table(self):
        """
        |write_table| with reStructuredText CSV table format.

        :raises pytablewriter.EmptyTableDataError:
            If the |header_list| and the |value_matrix| is empty.
        :Example:
            :ref:`example-rst-csv-table-writer`

        .. note::
            - |None| values are written as an empty string
        """

        IndentationTextTableWriter.write_table(self)

    def _get_opening_row_item_list(self):
        directive = ".. csv-table:: "

        if typepy.is_null_string(self.table_name):
            return [directive]

        return [directive + MultiByteStrDecoder(self.table_name).unicode_str]

    def _write_opening_row(self):
        self.dec_indent_level()
        super(RstCsvTableWriter, self)._write_opening_row()
        self.inc_indent_level()

    def _write_header(self):
        if not self.is_write_header:
            return

        if typepy.is_not_empty_sequence(self.header_list):
            self._write_line(
                ':header: "{:s}"'.format(
                    '", "'.join(
                        [MultiByteStrDecoder(header).unicode_str for header in self.header_list]
                    )
                )
            )

        self._write_line(
            ":widths: "
            + ", ".join([str(col_dp.ascii_char_width) for col_dp in self._column_dp_list])
        )
        self._write_line()

    def _get_value_row_separator_item_list(self):
        return []

    def _get_closing_row_item_list(self):
        return []


class RstGridTableWriter(RstTableWriter):
    """
    A table writer class for reStructuredText
    `Grid Tables <http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html#grid-tables>`__
    format.

    .. py:method:: write_table

        |write_table| with reStructuredText grid tables format.

        :Example:
            :ref:`example-rst-grid-table-writer`

        .. note::
            - |None| values are written as an empty string
    """

    @property
    def format_name(self):
        return "rst_grid_table"

    @property
    def support_split_write(self):
        return False

    def __init__(self):
        super(RstGridTableWriter, self).__init__()

        self.char_left_side_row = "|"
        self.char_right_side_row = "|"


class RstSimpleTableWriter(RstTableWriter):
    """
    A table writer class for reStructuredText
    `Simple Tables <http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html#simple-tables>`__
    format.

    .. py:method:: write_table

        |write_table| with reStructuredText simple tables format.

        :Example:
            :ref:`example-rst-simple-table-writer`

        .. note::
            - |None| values are written as an empty string
    """

    @property
    def format_name(self):
        return "rst_simple_table"

    @property
    def support_split_write(self):
        return False

    def __init__(self):
        super(RstSimpleTableWriter, self).__init__()

        self.column_delimiter = "  "
        self.char_cross_point = "  "

        self.char_opening_row = "="
        self.char_closing_row = "="

        self.is_write_value_separator_row = False
