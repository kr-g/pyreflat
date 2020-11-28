import io

import json

from pyreflat import DictTokenizer, DictIterpreter, FlatWriter, FlatReader
from pyreflat import FlatFile


def p(dic):
    try:
        print(json.dumps(dic, indent=4))
    except Exception as ex:
        # print(ex)
        print(dic)


d = {
    "a": 1,
    "b": 2.0,
    "c": "hello world",
    "d": {
        "z": 100,
        "y": 100.0,
        "x": "sub dict",
    },
    "e": [1, 3, 5, 7],
    "f": {
        "w": 200,
        "v": 200.0,
        "u": "sub dict 2",
        "fu": [11, 13, 17, {"fua": 153}, 19],
    },
    "g": [{"ga": 3000}, 1, [1, 2, 3, 4]],
    "h": [[1], [2, [2.1]], [3, [3.1, [3.2, 3.3, {"deep": True, "deeper": False}, -1]]]],
    "i": set([100, 300, 500, 700]),
    "j": tuple([1000, 3000, 5000, 7000]),
    "cplx": complex(1, 2),
    "lastentry": False,
    "done": True,
}

toknizr = DictTokenizer(emitType=True)
toknizr.from_dict(d)

alltokens = list(toknizr)  # iterator result as list

fltwr = FlatWriter(
    toknizr,  # iterable, or use alltokens here as parameter
    write_nl=True,  # write nl is the default behaviour
)

buf = io.StringIO()
fltwr.write(file=buf)

content = buf.getvalue()

fltrd = FlatReader()
ipret = DictIterpreter()

# read also next example below
lines = content.splitlines()
for line in lines:
    for token in fltrd.emit_from(line):
        ipret.run(token)

r = ipret.result()  # this will not reset the internal state
p(r)

# reset the internal state
ipret.reset()
r = ipret.result()
p(r)

# this will produce additional nl at string endings
# call FlatWriter with write_nl=False
# when emitting from e.g. a human readable file
# or use code as sample above
for t in fltrd.emit_from(content):
    ipret.run(t)

r = ipret.result()
p(r)

# reset the internal state
ipret.reset()
r = ipret.result()
p(r)

# emit from iterator
ipret.run_all(fltrd.emit_from_i(content.splitlines()))

r = ipret.result()
p(r)

# do more comfy

with FlatFile("test.flt.txt", "w") as f:
    f.write(d)

with FlatFile("test.flt.txt") as f:
    dic = f.read()

p(dic)

print("equal?", d == dic)
del d["a"]
print("equal?", d == dic)
