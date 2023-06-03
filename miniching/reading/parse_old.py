from textwrap import wrap

from miniching import config
from miniching.reading.helpers import get_result, format_hexagram_title
from miniching.reading.models import Reading

WIDTH = 80
LINE_BREAK = "\n"
SECTION_BREAK = LINE_BREAK * 2
INDENT = 2 * " "


class ReadingParser:
    def __init__(self, reading: Reading):
        self.parsed_reading = []
        self.reading = reading

    def get_history_record(self, width: int = WIDTH) -> str:
        history_record = [f"{str(self.reading.timestamp).center(WIDTH)}\n"]
        query = self.reading.query.center(WIDTH)
        if len(self.reading.query) > WIDTH:
            query = "\n".join(
                wrap(self.reading.query.center(WIDTH), width=width))

        history_record.append(query)
        history_record.append(
            f"{get_result(self.reading.hexagram).center(WIDTH)}")

        return "\n".join(history_record) + "\n"

    def get_printable_reading(self, full_text=False) -> str:
        if self.parsed_reading:
            return "".join(self.parsed_reading)

        result = get_result(self.reading.hexagram)
        if config.HEX_MIRROR:
            result = " | ".join(
                [result, get_unicode_hexagram_result(self.reading.hexagram)])
        if full_text:
            self._parse(result.center(WIDTH), SECTION_BREAK)

            if self.reading.trans_text and self.reading.trans_lines:
                self._parse_hexagram_text(self.reading.origin_text)
                self._parse_hexagram_text(self.reading.trans_text,
                                          self.reading.lines_to_read)
            elif self.reading.trans_text:
                self._parse_hexagram_text(self.reading.origin_text,
                                          self.reading.lines_to_read)
                self._parse_hexagram_text(self.reading.trans_text)
            else:
                self._parse_hexagram_text(self.reading.origin_text)
                return "".join(self.parsed_reading)
        else:
            return self.get_summary_result()

    def _parse(self, *values):
        [self.parsed_reading.append(value) for value in values]

    def _parse_header(self, header, capitalize=True, center=True):
        header = header.replace("_", " ")
        header = header.capitalize() if capitalize else header
        header = header.center(WIDTH) if center else header + ":"

        self._parse(header, SECTION_BREAK)

    def get_summary_result(self):
        result = SECTION_BREAK
        if self.reading.trans_lines:
            result = "".join([result, self.reading.hexagram.origin, " -> ",
                              self.reading.hexagram.trans, ":",
                              ','.join([line_to_read.line for line_to_read in
                                        self.reading.lines_to_read])])
            if config.HEX_MIRROR:
                # todo
                result = " | ".join([result, f"{self.reading.hexagram.origin}"])
            return f"{SECTION_BREAK}{self.reading.hexagram.origin} -> {self.reading.hexagram.trans}" \
                   f":{','.join([line_to_read.line for line_to_read in self.reading.lines_to_read])}"
        elif self.reading.hexagram.trans:
            return f"{SECTION_BREAK}{self.reading.hexagram.origin}" \
                   f":{','.join([line_to_read.line for line_to_read in self.reading.lines_to_read])}" \
                   f" -> {self.reading.hexagram.trans}"
        else:
            return f"{SECTION_BREAK}{self.reading.hexagram.origin}"


