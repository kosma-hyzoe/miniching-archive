from collections import OrderedDict
from textwrap import wrap

from miniching.files import REFERENCE, MODIFIED_ZHU_XI_LINE_EVALUATION
from miniching.reading.format import get_formatted_result, get_formatted_title, get_human_readable_timestamp


class ReadingParser:
    width = 80
    indent = " " * 4
    line_break = "\n"
    section_break = "\n" * 2

    parsed_reading: str

    def __init__(self, timestamp: str, query: str, decoded_excerpt: dict, classic: bool):
        hex_decimal = decoded_excerpt["hex_decimal"]
        changing_lines = decoded_excerpt["changing_lines"]

        self.reading = OrderedDict({"timestamp": timestamp, "query": query})
        hexagram_dict = {
            "title": REFERENCE[hex_decimal]["title"],
            "intro": REFERENCE[hex_decimal]["intro"],
            "judgement": REFERENCE[hex_decimal]["judgement"],
            "commentary": REFERENCE[hex_decimal]["commentary"],
            "image": REFERENCE[hex_decimal]["image"],
            "image_commentary": REFERENCE[hex_decimal]["image_commentary"],
        }

        if not changing_lines:
            self.reading['result'] = tuple([hex_decimal])
            self.reading["hexagram"] = hexagram_dict
        else:
            transformed_hex_decimal = decoded_excerpt["transformed_hex_decimal"]
            self.reading['result'] = tuple([hex_decimal, transformed_hex_decimal])

            self.reading["changing_lines"] = ", ".join([str(line) for line in changing_lines])
            if not classic:
                self.reading["lines_to_read"] = MODIFIED_ZHU_XI_LINE_EVALUATION[len(changing_lines)]

            self.reading["hexagram"] = hexagram_dict
            self.reading["transformed_hexagram"] = {
                "title": REFERENCE[transformed_hex_decimal]["title"],
                "intro": REFERENCE[transformed_hex_decimal]["intro"],
                "judgement": REFERENCE[transformed_hex_decimal]["judgement"],
                "commentary": REFERENCE[transformed_hex_decimal]["commentary"],
                "image": REFERENCE[transformed_hex_decimal]["image"],
                "image_commentary": REFERENCE[transformed_hex_decimal]["image_commentary"],
            }
            if len(changing_lines) == 6 and hex_decimal == 1 or len(changing_lines) == 6 and hex_decimal == 2:
                self.reading["hexagram"]["lines"] = {}
                self.reading["hexagram"]["lines"]["special_comment"] = REFERENCE[hex_decimal]["lines"]["special"]
            elif not classic and len(changing_lines) == 4 or not classic and len(changing_lines) == 5:
                line_to_read = [line for line in range(1, 7) if line not in changing_lines][0]
                self.reading["transformed_hexagram"]["lines"] = {}
                line_to_read = REFERENCE[transformed_hex_decimal]["lines"][line_to_read]
                self.reading["transformed_hexagram"]["lines"][line_to_read] = line_to_read
            else:
                lines_reference = REFERENCE[hex_decimal]["lines"]
                self.reading["hexagram"]["lines"] = {}
                [self.reading["hexagram"]["lines"].update({line: lines_reference[line]}) for line in changing_lines]

    def get_reading(self, key=None):
        return self.reading if not key else self.reading.get(key)

    def get_reading_as_simple_history_record(self) -> str:
        self.parsed_reading = ""

        human_readable_timestamp = get_human_readable_timestamp(self.reading["timestamp"])
        self._parse_section_divider(human_readable_timestamp, capitalize=False)

        self._parse_section_content(self.reading["query"], item_break=False)

        formatted_result = get_formatted_result(self.reading["result"])
        self._parse_section_content(formatted_result)

        if self.reading.get("changing_lines"):
            self._parse_section_content(self.reading["changing_lines"], item_break=False)
        if self.reading.get("lines_to_read"):
            self._parse_section_content(self.reading["lines_to_read"], item_break=False)

        return "".join([self.parsed_reading, self.line_break])

    def get_reading_as_map_history_record(self) -> dict:
        map_record = {"hex_decimal": self.reading['result'][0]}
        human_readable_timestamp = get_human_readable_timestamp(self.get_reading("timestamp"))
        map_record_content = {"timestamp": human_readable_timestamp, "query": self.reading["query"]}

        if self.reading.get('changing_lines'):
            formatted_result = get_formatted_result(self.reading["result"], unicode_mirroring=False)
            map_record_content["result"] = formatted_result,
            map_record_content["changing_lines"] = self.reading['changing_lines']

        map_record["content"] = OrderedDict(map_record_content)
        return map_record

    def get_printable_reading(self, full_text=False):
        self.parsed_reading = ""

        self._parse_item_by_key("result", get_formatted_result(self.reading["result"]))

        if full_text:
            self._parse_hexagrams()
        else:
            if self.reading.get("changing_lines"):
                self._parse_item_by_key("changing_lines")
            if self.reading.get("lines_to_read"):
                self._parse_item_by_key("lines_to_read")

        return self.parsed_reading

    def _parse_hexagrams(self):
        self._parse_hexagram_dictionary(transformed=False)

        if self.reading.get("transformed_hexagram"):
            self._parse_hexagram_dictionary(transformed=True)

    def _parse_hexagram_dictionary(self, transformed: bool):
        hexagram = self.reading["hexagram"] if not transformed else self.reading["transformed_hexagram"]

        formatted_title = get_formatted_title(hexagram["title"])
        self._parse_section_divider(formatted_title, capitalize=False)
        self._parse_section_content(hexagram["intro"])

        self._parse_section_content(hexagram["judgement"], preserve_line_breaks=True, double_indent=True)
        self._parse_section_content(hexagram["commentary"])

        self._parse_section_content(hexagram["image"], preserve_line_breaks=True, double_indent=True)
        self._parse_section_content(hexagram["image_commentary"])

        if hexagram.get("lines"):
            self._parse_lines(transformed)

    def _parse_lines(self, transformed: bool):
        lines = self.reading.get("transformed_hexagram").get("lines") if transformed else self.reading.get("hexagram").get("lines")

        for line_key, line_dictionary in lines.items():
            if line_key == "special_comment":
                self._parse_section_divider(line_key, capitalize=True, indent=True)
            else:
                formatted_line_key = " ".join(["Line ", str(line_key)])
                self._parse_section_divider(formatted_line_key, capitalize=False, indent=True)

            self._parse_section_content(line_dictionary["text"], preserve_line_breaks=True, double_indent=True)
            self._parse_section_content(line_dictionary["comment"])

    def _parse_item_by_key(self, key, alt_value=None):
        self._parse_section_divider(key)
        if alt_value:
            self._parse_section_content(alt_value)
        else:
            self._parse_section_content(self.reading[key])

    def _parse_section_divider(self, key, capitalize=True, indent=False):
        formatted_key = "".join([str(key).replace("_", " "), ':'])
        if capitalize:
            formatted_key = formatted_key.capitalize()
        if indent:
            self.parsed_reading = "".join([self.parsed_reading, self.indent])

        self.parsed_reading = "".join([self.parsed_reading, formatted_key, self.section_break])

    def _parse_section_content(self, value, preserve_line_breaks=False, double_indent=False, item_break=True, width=width):
        indent = (self.indent * 2) if double_indent else self.indent
        if preserve_line_breaks:
            value_lines = value.split(self.line_break)
            self.parsed_reading = "".join([self.parsed_reading, indent])
            joined_lines = ("".join([self.line_break, indent])).join(value_lines)
            self.parsed_reading = "".join([self.parsed_reading, joined_lines])
        else:
            wrapped_value = wrap(value, width=width, initial_indent=indent, subsequent_indent=indent)
            self.parsed_reading = "".join([self.parsed_reading, self.line_break.join(wrapped_value)])

        if item_break:
            self.parsed_reading = "".join([self.parsed_reading, self.section_break])
        else:
            self.parsed_reading = "".join([self.parsed_reading, self.line_break])