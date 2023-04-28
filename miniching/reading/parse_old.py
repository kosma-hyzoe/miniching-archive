from textwrap import wrap

from miniching import config
from miniching.reading.format import get_result, format_hexagram_header, get_unicode_hexagram_result
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
            query = "\n".join(wrap(self.reading.query.center(WIDTH), width=width))

        history_record.append(query)
        history_record.append(f"{get_result(self.reading.hexagram).center(WIDTH)}")

        return "\n".join(history_record) + "\n"

    def get_printable_reading(self, full_text=False) -> str:
        if self.parsed_reading:
            return "".join(self.parsed_reading)

        result = get_result(self.reading.hexagram)
        if config.UNICODE_HEXAGRAM_MIRROR:
            result = " | ".join([result, get_unicode_hexagram_result(self.reading.hexagram)])
        if full_text:
            self._parse(result.center(WIDTH), SECTION_BREAK)

            if self.reading.trans_text and self.reading.lines_apply_to_trans:
                self._parse_hexagram_text(self.reading.origin_text)
                self._parse_hexagram_text(self.reading.trans_text, self.reading.lines_to_read)
            elif self.reading.trans_text:
                self._parse_hexagram_text(self.reading.origin_text, self.reading.lines_to_read)
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
        if self.reading.lines_apply_to_trans:
            result = "".join([result, self.reading.hexagram.origin, " -> ", self.reading.hexagram.trans, ":",
                              ','.join([line_to_read.line for line_to_read in self.reading.lines_to_read])])
            if config.UNICODE_HEXAGRAM_MIRROR:
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

    def _parse_text(self, text, preserve_line_breaks=False):
        if preserve_line_breaks:
            lines = text.split(LINE_BREAK)
            indented_line_breaks = "".join([LINE_BREAK, INDENT])
            self._parse(INDENT, indented_line_breaks.join(lines), SECTION_BREAK)
        else:
            wrapped_text = wrap(text, width=WIDTH)
            formatted_text = LINE_BREAK.join(wrapped_text)
            formatted_text += SECTION_BREAK

            self._parse(formatted_text)

    def _parse_lines(self, lines):
        # todo
        for line_key, line_dictionary in lines.items():
            if line_key == "special_comment":
                self._parse_header(line_key, capitalize=True)
            else:
                self._parse(INDENT, "Line ", str(line_key), ":", SECTION_BREAK)

            self._parse_text(line_dictionary["text"], preserve_line_breaks=True)
            self._parse_text(line_dictionary["comment"])

    def _parse_hexagram_text(self, hexagram, lines=None):
        self._parse_header(format_hexagram_header(hexagram.title))
        self._parse_text(hexagram.intro)

        self._parse_text(hexagram.judgement, preserve_line_breaks=True)
        self._parse_text(hexagram.commentary)

        self._parse_text(hexagram.image, preserve_line_breaks=True)
        self._parse_text(hexagram.image_commentary)

        if lines:
            self._parse_lines(lines)
