# miniching

## What is miniching?

A CLI-friendly, customizable I Ching tool with smart line selection,
custom line evaluation and other improvements.

### How to run miniching?

1. Make sure Python 3 is installed. The project was developed on Python 3.10.6.
   Older versions should also work, but were not tested.
2. Install the requirements from `requirements.txt`
   (currently it only contains `pyyaml`)
3. Download this repo.
4. Modify `config.py` as needed.
5. Navigate to the repo's root and either:
    1. Run as a package/module with `python -m miniching`
    2. Execute as a script with `./mcng`

The second way will probably require you to add execute permissions to `mcng`
with something like `chmod u+x mcng`. I recommend adding the repo to your
`$PATH` variable and making some functions/aliases to fit your needs, i.e.:

```bash
alias ccng="mcng --write-history --classic-eval"
pcng() {mcng $1 | less}
```

Use `mcng -h` to see the options:

```
usage: mcng [-h] [-c] [-f] [-w] [-s] [-q QUERY] [-e EXCERPT] [-t TIMESTAMP]
            [-p HISTORY_PATH]

options:
  -h, --help            show this help message and exit
  -c, --classic         use classic evaluation / 'read all changing lines'
                        instead of the default modified Zhu Xi method
  -f, --full-reading    get a full reading instead of just the hexagram
                        transition result
  -w, --write-history   write history to a txt file using the specified path
                        (config.py or command or `-p` argument).will attempt
                        to write in $HOME if no path was specified
  -s, --skip-print      don't print the reading
  -q QUERY, --query QUERY
                        provide a query instead of using the default prompt
  -e EXCERPT, --excerpt EXCERPT
                        provide an excerpt using '64' /'61:1,2' or the 3 coin
                        sum notation ('788688' -> 23:3)
  -t TIMESTAMP, --timestamp TIMESTAMP
                        provide a timestamp, any format
  -p HISTORY_PATH, --history-path HISTORY_PATH
                        provide an alternative history path.
```

## What is I Ching?

An ancient divination and wisdom book, easily one of, if not the most
influential chinese text. Think jungian dream generator and Bible
studies for the cool kids or a less woo-woo Tarot.

### Isn't it still a bit esoteric and weird?

**It probably is.** I hope that mentioning Jung makes it digestible enough even for 
an average western intellectual. Here's his I Ching foreword at
[carljungdepthpsychologysite.blog](https://carljungdepthpsychologysite.blog/2020/02/03/foreword-to-the-i-ching-by-carl-gustav-jung/)

### How does I Ching divination work?

The user writes down a query (usually a question) and gets a result with one
of the divination methods - usually tossing 3 coins or arranging yarrow stalks.

The main part of the text consists of 64 hexagrams.
Their signs consist of six lines - yin ("unbroken") and yang ("broken") ones.

When tossing coins, each coin is assigned a value of 3 (usually "heads") or
2 (usually "tails"). A 7 or 8 gets you a "young", unchanging, yin or yang,
a 9 or 6 gets you  an "old" yin or yang and produce changing lines.

The result to a query can either be a static hexagram, (i.e. 3 : ䷂) or a
hexagram transition if one or more changing lines apply
(i.e. 3 -> 27 : ䷂ -> ䷚, with changing lines 5 and 6th).
The user should now read all of related text using preferred evaluation method.

*This is of course nothing but a major oversimplification.*

## Credits and references

The modified Zu Xhi evaluation method that miniching uses by default is from
[biroco.com](https://www.biroco.com/yijing/basics.htm)

The default `iching_reference.yaml` file
is the classic Richard Wilhelm's and Cary F. Baynes' translation.
I found it as a JSON file in a public GitHub repo
[here](https://github.com/dkloke/I-Ching-ref/blob/master/iChing.json),
converted it to YAML and edited for my needs.

## Recommended sources for an in-depth reference

* [Wikipedia](https://en.wikipedia.org/wiki/I_Ching)
* [Biroco](https://www.biroco.com/yijing/index.htm)
* [The Gnostic Book Of Changes](https://www.jamesdekorne.com/GBCh/GBCh.htm)
* [Carl Jung and the I Ching](https://carl-jung.net/iching.html)
