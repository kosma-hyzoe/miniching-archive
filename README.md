# miniching

## What is miniching?

A console-friendly, minimalist I Ching library written in Python 3 with smart
line selection, custom line evaluation and some extra features.

### How to run miniching?

1. Make sure Python 3 is installed. The project was developed on Python 3.10.6.
   Older and newer versions should also work, but were not tested.
2. Install the requirements from `requirements.txt`
   (currently it only contains `pyyaml==6.0`)
3. Navigate to where the `miniching` package is located
   (a `pip`-installable package coming soon)
4. Modify the `config.ini` file if needed. Currently, it supports changing some
   formatting options and changing the path to the history file.
5. Run `$ python3 -m miniching` in console with chosen flags/arguments.

### How does miniching work?

#### Definitions



```
options:
  -h, --help            show this help message and exit
  -f, --full-reading    get a full reading
  -w, --write-history   write to a history.txt file
  -s, --skip-print      don't print the reading
  -q, --quick           get a reading with an empty query
  -c, --classic         use classic evaluation / 'read all changing lines' instead of the default modified Zhu Xi method
  -e MANUAL_EXCERPT, --manual-excerpt MANUAL_EXCERPT
                        provide an excerpt using '64' format for pure hexes or '63:1,2' with changing lines
  -t MANUAL_TIMESTAMP, --manual-timestamp MANUAL_TIMESTAMP
                        provide a timestamp matching the provided format (by default it's %d-%m-%Y)
```

## What is I Ching?

An ancient divination and wisdom book, easily one of, if not the most
influential chinese text. Think jungian dream generator and Bible
studies for the cool kids or a less woo-woo Tarot.

### Isn't it still a bit esoteric and weird?

**It probably is.** I hope that mentioning Jung makes it digestible enough for
an average western intellectual. Here's his I Ching foreword at
[carljungdepthpsychologysite.blog](https://carljungdepthpsychologysite.blog/2020/02/03/foreword-to-the-i-ching-by-carl-gustav-jung/)

### How does I Ching divination work?

The user writes down a query (usually a question) and gets a result with one
of the divination methods - usually tossing coins or arranging yarrow stalks
(the latter coming soon).

The main part of the text consists of 64 hexagrams.
Their signs consist of six lines - yin ("unbroken") and yang ("broken") ones.

When tossing coins, each coin is assigned a value of 3 (usually "heads") or
2 (usually "tails"). A 7 or 8 gets you "old" yin and yang, a 9 or 6 gets you
a "new" yin and yang and produce changing lines.

The result to a query can either pe a "pure" hexagram, (i.e. 3 : ䷂) or a
hexagram transition if one or more changing lines apply
(i.e. 3 -> 27 : ䷂ -> ䷚, where changing lines are 5th and 6th).
The user should now read all of related text using preferred evaluation method.

*This is of course nothing but a major oversimplification.*

## Credits and references

The modified Zu Xhi evaluation method that miniching uses by default is from
[biroco.com](https://www.biroco.com/yijing/basics.htm)

The default `iching_reference.yaml` file (more translations coming soon)
is the classic Richard Wilhelm's and Cary F. Baynes' translation.
I found it as a JSON file in a public
[GitHub repo of a user called `dkloke`](https://github.com/dkloke/I-Ching-ref/blob/master/iChing.json),
converted it to YAML and edited for my needs.

## Recommended sources for an in-depth reference
* [Wikipedia](https://en.wikipedia.org/wiki/I_Ching)
* [Biroco](https://www.biroco.com/yijing/index.htm)
* [The Gnostic Book Of Changes](https://www.jamesdekorne.com/GBCh/GBCh.htm)
* [Carl Jung and the I Ching](https://carl-jung.net/iching.html)
