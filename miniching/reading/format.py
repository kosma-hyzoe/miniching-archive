from miniching.files import REFERENCE


def get_human_readable_timestamp(timestamp):
    return timestamp.strftime("%d-%m-%Y")


def get_formatted_result(result, unicode_mirroring=True) -> str:
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


def get_formatted_title(title):
    title_copy = title
    if "(" in title:
        title_copy = title[:title.index("(") - 1]
    elif "[" in title:
        title_copy = title[:title.index("[") - 1]
    return f"'{title_copy}'"