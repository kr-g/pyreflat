
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


# pyreflat - flatten python dict support

transform a python dict to a flat structure and back

features:

- 2-way transformation
  - from dict to flatten
  - from flaten to dict
- supported types
  - bool
  - int
  - float
  - complex
  - list
  - set
  - tupel
  - dict 
- support for nested heterogeneous types in list 
- support for list in lists
- no dependencies
- pure python


# how to use

refer to [`sample.py`](https://github.com/kr-g/pyreflat/blob/main/sample.py)

code:

    from pyreflat import FlatFile

    fnam = "test-file.txt"
    test_dict = { "a": 1 }

    with FlatFile(fnam, "w") as f:
        f.write(test_dict)

    with FlatFile(fnam) as f:
        dic = f.read()


# how it works

with using techniques from compiler construction a stream of tokens are produced
which can be saved into a simple file.

the tokens can later send to an interpreter for constructing the former dict again

use REPL to find out more:

    toknizr = DictTokenizer(emitType=True)
    toknizr.from_dict({"a":1,"b":2.0,"c":[1,2,3],"d":[ [1], [2,2], [3,3,3] ]})

    alltokens = list(toknizr)  # iterator result as list


# Platform

Tested on Python3, and Linux.


# Development status

alpha state.
the API or logical call flow might change without prior notice.

read [`CHANGELOG`](https://github.com/kr-g/pyreflat/blob/master/CHANGELOG.MD)
for latest, or upcoming news.


# limitations

unknown


# installation
    
available on pypi. install with:

    python3 -m pip install pyreflat
    
