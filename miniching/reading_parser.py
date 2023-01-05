from textwrap import wrap


class ReadingParser:
    WIDTH = 80
    INDENT = " " * 4
    LINE_BREAK = "\n"
    ITEM_BREAK = "\n" * 2

    SKIP_FOR_SIMPLE_HISTORY_OUTPUT = ["hexagram", "transformed_hexagram", "lines_to_read"]
    SKIP_FOR_PRINTABLE_OUTPUT = ["timestamp", "query", "hexagram", "transformed_hexagram"]
    SKIP_FOR_FULL_TEXT_PRINTABLE_OUTPUT = ["timestamp", "query", "changing_lines", "lines_to_read"]

    def __init__(self, reading: dict, default_formatting=True):
        self.reading = reading
        self.parsed_reading = self.LINE_BREAK
        if not default_formatting:
            self._get_formatting_from_config()

    def get_reading_as_simple_history_record(self):
        self.parsed_reading = ""
        for key, value in self.reading.items():
            if key == "timestamp":
                self._parse_section_divider(value, capitalize=False)
            elif key in self.SKIP_FOR_SIMPLE_HISTORY_OUTPUT:
                continue
            else:
                self._parse_section_content(value, item_break=False)
        return "".join([self.parsed_reading, self.LINE_BREAK])

    def get_reading_as_printable_output(self, full_text: bool):
        self.parsed_reading = ""
        keys_to_skip = self.SKIP_FOR_FULL_TEXT_PRINTABLE_OUTPUT if full_text else self.SKIP_FOR_PRINTABLE_OUTPUT
        for key, value in self.reading.items():
            if key in keys_to_skip:
                continue
            elif type(value) is dict:
                self._parse_hex_dictionary(value)
            else:
                self._parse_section_divider(key)
                self._parse_section_content(value)
        return self.parsed_reading

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
            self.parsed_reading = "".join([self.parsed_reading, self.INDENT])

        self.parsed_reading = "".join([self.parsed_reading, formatted_key, self.ITEM_BREAK])

    def _parse_section_content(self, value, preserve_line_breaks=False, double_indent=False, item_break=True):
        indent = (self.INDENT * 2) if double_indent else self.INDENT
        if preserve_line_breaks:
            value_lines = value.split(self.LINE_BREAK)
            self.parsed_reading = "".join([self.parsed_reading, indent])
            joined_lines = ("".join([self.LINE_BREAK, indent])).join(value_lines)
            self.parsed_reading = "".join([self.parsed_reading, joined_lines])
        else:
            wrapped_value = wrap(value, width=self.WIDTH, initial_indent=indent, subsequent_indent=indent)
            self.parsed_reading = "".join([self.parsed_reading, self.LINE_BREAK.join(wrapped_value)])

        if item_break:
            self.parsed_reading = "".join([self.parsed_reading, self.ITEM_BREAK])
        else:
            self.parsed_reading = "".join([self.parsed_reading, self.LINE_BREAK])

    def _get_formatting_from_config(self):
        pass


