from datetime import datetime
from miniching import config as rc
from textwrap import wrap
from typing import NamedTuple, Optional, List


class Hexagram(NamedTuple):
    origin: str
    trans: Optional[str] = None
    lines: list[str] = []
    zhu_xi_eval: bool = False

    def __str__(self):
        if self.lines:
            return f"{self.origin}:{','.join(self.lines)}"
        else:
            return self.origin


class HistoryRecord(NamedTuple):
    timestamp: datetime
    query: str
    result: str

    def __str__(self):
        return "\n".join([
            self.timestamp,
            self.query,
            self.result])


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
    lines_to_read: List[LineText]
    trans_lines: bool = False
