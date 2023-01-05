# __lxiv-ching__
## _the minified, terminal-friendly I Ching program_

### What is this I Ching thing?
* [Quick reference](https://en.wikipedia.org/wiki/I_Ching)
* Sources for an in-depth reference:
  * [Biroco](https://www.biroco.com/yijing/index.htm)
  * [The Gnostic Book Of Changes](https://www.jamesdekorne.com/GBCh/GBCh.htm)
  * [Carl Jung and the I Ching](https://carl-jung.net/iching.html)


### Usage:
1. make sure (Python 3)[https://www.python.org] is installed
2. install via `pip install miniching`
3. run `python3.10 -m lxiv-ching {optional_flags}` where:
   * _{optional flags}_:
      * --nohistory - dont write to history .txt file(the history file needs fixing since updating to pypi, will do soon)
      * --debug - enter debug mode(still in development)
4. the program will prompt a query. write it down or leave blank and press the 'enter' key.

*__This version uses the three coin divination method. Yarrow stalks method possibly coming soon__* 

### Demo:
```
$ python3 -m lxiv-ching
Query: Demo query

Time:
        2022-06-04T09:34
Query: 
        Demo query
Result:
        19->51
Comments:
        Original hexagram's changing lines apply. the uppermost line of the two is most important.
        Lines to read: 2, 4
```


# miniching
