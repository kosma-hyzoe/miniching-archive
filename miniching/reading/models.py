from datetime import datetime
from typing import NamedTuple, Optional, List

from miniching.hexagrams import Hexagram


class LineText(NamedTuple):
    line: str
    text: str
    comment: str


class HexagramText(NamedTuple):
    title: str
    intro: str
    judgement: str
    commentary: str
    image: str
    image_commentary: str


class Reading(NamedTuple):
    timestamp: datetime
    query: str
    hexagram: Hexagram
    origin_text: HexagramText
    trans_text: Optional[HexagramText]
    lines_to_read: Optional[List[LineText]]
    lines_apply_to_trans: bool
