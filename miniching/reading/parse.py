from textwrap import wrap

from miniching.serialization import get_config, REFERENCE
from miniching.reading.format import SECTION_BREAK, WIDTH, LINE_BREAK, INDENT, INITIAL_INDENT


def format_result(result):
    hex_decimal = result[0]
    hex_sign = REFERENCE[hex_decimal]['sign']
    if len(result) == 1:
        result = f"{hex_decimal}"
        if get_config()["formats"].getboolean("unicode_result_mirroring"):
            result += f" : {hex_sign}"
    else:
        transformed_hex_decimal = result[1]
        transformed_hex_sign = REFERENCE[transformed_hex_decimal]['sign']
        result = f"{hex_decimal} -> {transformed_hex_decimal}"
        if get_config()["formats"].getboolean("unicode_result_mirroring"):
            result += f" : {hex_sign} -> {transformed_hex_sign}"

    return result


def format_hexagram_header(header):
    if "(" in header:
        header = header[:header.index("(") - 1]
    elif "[" in header:
        header = header[:header.index("[") - 1]

    return header


class ReadingParser:

    def __init__(self, reading: dict):
        self.parsed_reading = []
        self.reading = reading

    def get_history_record(self) -> str:
        history_record = [
            f"{self.reading['timestamp']}\n",
            f"{self.reading['query']}",
            f"{format_result(self.reading['result'])}"
        ]

        if self.reading.get("changing_lines"):
            history_record.append(f"{self.reading['changing_lines']}")

        history_record.append('\n')
        return "\n".join(history_record)

    def get_printable_reading(self, full_text=False) -> str:
        if not self.parsed_reading:
            result = format_result(self.reading['result'])

            if full_text:
                self._parse(result.center(WIDTH), SECTION_BREAK)
                self._parse_hexagram_dictionary(self.reading["hexagram"])

                if self.reading.get("transformed_hexagram"):
                    self._parse_hexagram_dictionary(self.reading["transformed_hexagram"])

            else:
                self._parse_summary_reading_item('result', result)
                if self.reading.get("changing_lines"):
                    self._parse_summary_reading_item("changing_lines", self.reading["changing_lines"])
                if self.reading.get("lines_to_read"):
                    self._parse_summary_reading_item("lines_to_read", self.reading["lines_to_read"])

        return "".join(self.parsed_reading)

    def _parse(self, *values):
        [self.parsed_reading.append(value) for value in values]

    def _parse_header(self, header, capitalize=True, center=True):
        header = header.replace("_", " ")
        header = header.capitalize() if capitalize else header
        header = header.center(WIDTH) if center else header + ":"

        self._parse(header, SECTION_BREAK)

    def _parse_summary_reading_item(self, key, value):
        self._parse(f"{key.capitalize()}:{SECTION_BREAK}{INDENT}{value}{SECTION_BREAK}")

    def _parse_text(self, text, preserve_line_breaks=False):
        if preserve_line_breaks:
            lines = text.split(LINE_BREAK)
            indented_line_breaks = "".join([LINE_BREAK, INDENT])
            self._parse(INDENT, indented_line_breaks.join(lines), SECTION_BREAK)
        else:
            wrapped_text = wrap(text, width=WIDTH, initial_indent=INITIAL_INDENT)
            formatted_text = LINE_BREAK.join(wrapped_text)
            formatted_text += SECTION_BREAK

            self._parse(formatted_text)

    def _parse_lines(self, lines):
        for line_key, line_dictionary in lines.items():
            if line_key == "special_comment":
                self._parse_header(line_key, capitalize=True)
            else:
                self._parse(INDENT, "Line ", str(line_key), ":", SECTION_BREAK)

            self._parse_text(line_dictionary["text"], preserve_line_breaks=True)
            self._parse_text(line_dictionary["comment"])

    def _parse_hexagram_dictionary(self, hexagram):
        self._parse_header(format_hexagram_header(hexagram["title"]))
        self._parse_text(hexagram["intro"])

        self._parse_text(hexagram["judgement"], preserve_line_breaks=True)
        self._parse_text(hexagram["commentary"])

        self._parse_text(hexagram["image"], preserve_line_breaks=True)
        self._parse_text(hexagram["image_commentary"])

        if hexagram.get("lines"):
            self._parse_lines(hexagram.get("lines"))
