from collections import OrderedDict
from textwrap import wrap

from miniching.files import REFERENCE, get_config


class ReadingParser:
    width = 80
    indent = " " * 4
    line_break = "\n"
    item_break = "\n" * 2

    SKIP_FOR_SIMPLE_HISTORY_OUTPUT = ["hexagram", "transformed_hexagram", "lines_to_read"]
    SKIP_FOR_PRINTABLE_OUTPUT = ["timestamp", "query", "hexagram", "transformed_hexagram"]
    SKIP_FOR_FULL_TEXT_PRINTABLE_OUTPUT = ["timestamp", "query", "changing_lines", "lines_to_read"]

    def __init__(self, reading: dict):
        self.reading = reading
        self.parsed_reading = ""

    def get_reading_as_printable_output(self, full_text_mode: bool) -> str:
        self.parsed_reading = ""
        keys_to_skip = self.SKIP_FOR_FULL_TEXT_PRINTABLE_OUTPUT if full_text_mode else self.SKIP_FOR_PRINTABLE_OUTPUT
        for key, value in self.reading.items():
            if key in keys_to_skip:
                continue
            elif key == "result":
                self._parse_section_divider(key)
                formatted_result = self.get_formatted_result()
                self._parse_section_content(formatted_result)
            elif type(value) is dict:
                self._parse_hex_dictionary(value)
            else:
                self._parse_section_divider(key)
                self._parse_section_content(value)
        return self.parsed_reading

    def get_reading_as_simple_history_record(self) -> str:
        self.parsed_reading = ""
        for key, value in self.reading.items():
            if key == "timestamp":
                self._parse_section_divider(value, capitalize=False)
            elif key == "result":
                self._parse_section_divider(key)
                formatted_result = self.get_formatted_result()
                self._parse_section_content(formatted_result)
            elif key in self.SKIP_FOR_SIMPLE_HISTORY_OUTPUT:
                continue
            else:
                self._parse_section_content(value, item_break=False)
        return "".join([self.parsed_reading, self.line_break])

    def get_reading_as_map_history_record(self) -> dict:
        map_record = {"hex_decimal": self.reading['result'][0]}
        map_record_content = {"timestamp": self.reading["timestamp"], "query": self.reading["query"]}

        if self.reading.get('changing_lines'):
            map_record_content["result"] = self.get_formatted_result(unicode_mirroring=False)
            map_record_content["changing_lines"] = self.reading['changing_lines']

        map_record["content"] = OrderedDict(map_record_content)
        return map_record

    def _parse_hex_dictionary(self, hex_dictionary):
        for key, value in hex_dictionary.items():
            if key == "title":
                hex_title_key = value
                if "(" in hex_title_key:
                    hex_title_key = hex_title_key[:hex_title_key.index("(") - 1]
                elif "[" in hex_title_key:
                    hex_title_key = hex_title_key[:hex_title_key.index("[") - 1]
                self._parse_section_divider(f"'{hex_title_key}'", capitalize=False)
            elif type(value) is dict:
                self._parse_line_dictionary(key, value)
            elif key == "judgement" or key == "image":
                self._parse_section_content(value, preserve_line_breaks=True, double_indent=True)
            else:
                self._parse_section_content(value)

    def _parse_line_dictionary(self, line_key, line_dictionary):
        if line_key != "special_comment":
            self._parse_section_divider(" ".join(["Line ", str(line_key)]), capitalize=False, indent=True)
        else:
            self._parse_section_divider(line_key, capitalize=True, indent=True)

        self._parse_section_content(line_dictionary["text"], preserve_line_breaks=True, double_indent=True)
        self._parse_section_content(line_dictionary["comment"])

    def _parse_section_divider(self, key, capitalize=True, indent=False):
        formatted_key = "".join([str(key).replace("_", " "), ':'])
        if capitalize:
            formatted_key = formatted_key.capitalize()
        if indent:
            self.parsed_reading = "".join([self.parsed_reading, self.indent])

        self.parsed_reading = "".join([self.parsed_reading, formatted_key, self.item_break])

    def _parse_section_content(self, value, preserve_line_breaks=False, double_indent=False, item_break=True):
        indent = (self.indent * 2) if double_indent else self.indent
        if preserve_line_breaks:
            value_lines = value.split(self.line_break)
            self.parsed_reading = "".join([self.parsed_reading, indent])
            joined_lines = ("".join([self.line_break, indent])).join(value_lines)
            self.parsed_reading = "".join([self.parsed_reading, joined_lines])
        else:
            wrapped_value = wrap(value, width=self.width, initial_indent=indent, subsequent_indent=indent)
            self.parsed_reading = "".join([self.parsed_reading, self.line_break.join(wrapped_value)])

        if item_break:
            self.parsed_reading = "".join([self.parsed_reading, self.item_break])
        else:
            self.parsed_reading = "".join([self.parsed_reading, self.line_break])

    def get_formatted_result(self, unicode_mirroring=True) -> str:
        result = self.reading["result"]
        hex_decimal = result[0]
        hex_sign = REFERENCE[hex_decimal]['sign']
        if len(result) == 1:
            result = f"{hex_decimal}"
            if unicode_mirroring:
                result += f" : {hex_sign}"
        else:
            transformed_hex_decimal = result[1]
            transformed_hex_sign = REFERENCE[transformed_hex_decimal]['sign']
            result = f"{hex_decimal} -> {transformed_hex_decimal}"
            if unicode_mirroring:
                result += f" : {hex_sign} -> {transformed_hex_sign}"
        return result
