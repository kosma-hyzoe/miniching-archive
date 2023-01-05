from textwrap import wrap
from miniching.files import get_config


class ReadingParser:
    width = 80
    indent = " " * 4
    line_break = "\n"
    item_break = "\n" * 2

    def __init__(self, reading: dict, default_formatting=True):
        self.reading = reading
        self.parsed_reading = self.line_break
        if not default_formatting:
            self._get_formatting_from_config()

    def get_parsed_reading(self, skip_query=False, skip_timestamp=False):
        for key, value in self.reading.items():
            if key == "query" and skip_query or key == "timestamp" and skip_timestamp:
                continue
            elif type(value) is dict:
                self._parse_hex_dictionary(value, "transformed" in key)
            else:
                self._parse_key(key)
                self._parse_value(value)
        return self.parsed_reading

    def _parse_hex_dictionary(self, hex_dictionary, transformed: bool):
        hex_key = hex_dictionary['title']
        if "(" in hex_key:
            hex_key = hex_key[:hex_key.index("(") - 1] + "'"
        elif "[" in hex_key:
            hex_key = hex_key[:hex_key.index("[") - 1] + "'"

        self._parse_key(hex_key, capitalize=False)
        for key, value in hex_dictionary.items():
            if type(value) is dict:
                self._parse_line_dictionary(key, value)
            elif key == "title":
                continue
            elif key == "judgement" or key == "image":
                self._parse_value(value, preserve_line_breaks=True, indent=self.indent * 2)
            else:
                self._parse_value(value)

    def _parse_line_dictionary(self, line_key, line_dictionary):
        line_prefix = "Line " if line_key != "special_comment" else None
        self._parse_key(line_key, False, line_prefix, line_prefix) if line_key != "special_comment" else self._parse_key(line_key)

        text, comment = line_dictionary["text"], line_dictionary["comment"]
        self._parse_value(text, preserve_line_breaks=True, indent=self.indent * 2)
        self._parse_value(comment)
        # self._parse_value(wrapped_text, wrap_value=False)
        # self.parsed_reading += self.line_break.join(wrapped_text) + self.item_break
        # self._parse_value(comment)
        # self.parsed_reading += self.line_break.join(wrapped_comment) + self.item_break

    def _parse_key(self, key, capitalize=True, prefix=None, indent=False):
        formatted_key = str(key).capitalize().replace("_", " ") if capitalize else str(key).replace("_", " ")
        formatted_key = prefix + formatted_key + ":" if prefix else formatted_key + ":"
        self.parsed_reading += self.indent + formatted_key + self.item_break if indent else formatted_key + self.item_break

    def _parse_value(self, value, preserve_line_breaks=False, indent=indent):
        if preserve_line_breaks:
            value_lines = value.split(self.line_break)
            self.parsed_reading += indent + (self.line_break + indent).join(value_lines) + self.item_break
        else:
            wrapped_value = wrap(value, width=self.width, initial_indent=indent, subsequent_indent=indent)
            self.parsed_reading += self.line_break.join(wrapped_value) + self.item_break

    def _get_formatting_from_config(self):
        config = get_config()
        self.width = config.get("reading_formatting", "width")
        self.indent = config.get("reading_formatting", "indent")
        self.line_break = config.get("reading_formatting", "line_break")
        self.item_break = config.get("reading_formatting", "item_break")


