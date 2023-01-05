import yaml

from miniching.files import read_serialization_data, REFERENCE
from miniching.files import RESOURCES_PATH


def main():
    add_yaml_representers()
    json_ref = read_serialization_data(RESOURCES_PATH + "/original_reference.json")
    yaml_ref = read_serialization_data(RESOURCES_PATH + "/reference.yaml")

    for i in range(1, 65):
        yaml_ref[i] = {}

    for json_hex in json_ref:
        yaml_hex = yaml_ref[json_hex["kingWen"]]
        parse_hex(yaml_hex, json_hex)

    write_reference(yaml_ref)


def write_reference(value: dict, append_mode=True):
    mode = "a" if append_mode else "w"
    with open(RESOURCES_PATH + "/reference.yaml", mode) as f:
        yaml.dump(value, f, allow_unicode=True, width=120, sort_keys=False)


def parse_hex(yaml_hex, json_hex):
    def parse_value(key, original_key=None):
        if original_key:
            yaml_hex[key] = json_hex[original_key]
        else:
            yaml_hex[key] = json_hex[key]

    def parse_long_text(key, original_key=None):
        yaml_hex[key] = ""
        long_text = json_hex[key] if not original_key else json_hex[original_key]
        for fragment in long_text:
            yaml_hex[key] += " ".join(fragment)
            yaml_hex[key] += "\n"
        yaml_hex[key] = FoldedUnicode(yaml_hex[key][:-1])

    def parse_versed_text(key, original_key=None):
        if original_key:
            yaml_hex[key] = LiteralUnicode("\n".join(json_hex[original_key]))
        else:
            yaml_hex[key] = LiteralUnicode("\n".join(json_hex[key]))

    parse_value("name", "title")
    parse_value("chinese_name", "name")
    parse_value("unicode", "unicodeChar")
    parse_long_text("intro")
    parse_versed_text("judgement")
    parse_long_text("commentary", "judgeText")
    parse_versed_text("image")
    parse_long_text("image_commentary", "imageText")

    yaml_hex["lines"] = {}
    for position, line_content in zip(range(1, 6 + 1), json_hex["lines"]):
        yaml_hex["lines"][position] = {"text": LiteralUnicode("\n".join(line_content["text"])),
                                       "comment": FoldedUnicode(" ".join(line_content["comment"]))}


class LiteralUnicode(str):
    @staticmethod
    def representer(dumper, data):
        return dumper.represent_scalar(u'tag:yaml.org,2002:str', data, style='|')


class FoldedUnicode(str):
    @staticmethod
    def representer(dumper, data):
        return dumper.represent_scalar(u'tag:yaml.org,2002:str', data, style='>')


def add_yaml_representers():
    yaml.add_representer(FoldedUnicode, FoldedUnicode.representer)
    yaml.add_representer(LiteralUnicode, LiteralUnicode.representer)


if __name__ == "__main__":
    main()
