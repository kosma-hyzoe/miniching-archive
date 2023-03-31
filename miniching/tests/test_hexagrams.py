from context import miniching
from miniching import hexagrams


def test_hexagrams():
    hexagram = hexagrams.Hexagram('1', '2', ['3'])
    assert str(hexagram) == '1:3'

    hexagram = hexagrams.Hexagram('53', None, None)
    assert str(hexagram) == '53'

    hexagram = hexagrams.get_from_excerpt('52:3')
    assert hexagram.trans == '23'
    assert str(hexagram) == '52:3'

    hexagram = hexagrams.get_from_excerpt('52')
    assert hexagram.trans == None

    hexagram = hexagrams.get_from_excerpt('788988')
    assert hexagram.origin == '52'
    assert hexagram.trans == '23'
    assert hexagram.changing_lines == ['3']
    assert str(hexagram) == '52:3'
