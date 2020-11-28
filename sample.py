import io
import os
import json

from pyreflat import DictTokenizer, DictIterpreter, FlatWriter, FlatReader
from pyreflat import FlatFile
from pyreflat.conv import Convert, ConvertHex, ConvertUTF8


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
    "c_nl": "hello\nworld\n",
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

toknizr = DictTokenizer(emitType=True, converter=ConvertHex)
toknizr.from_dict(d)

alltokens = list(toknizr)  # iterator result as list

fltwr = FlatWriter(
    toknizr,  # iterable, or use alltokens here as parameter
    write_nl=False,  # write nl is the default behaviour
)

buf = io.StringIO()
fltwr.write(file=buf)

content = buf.getvalue()

fltrd = FlatReader()
ipret = DictIterpreter(converter=ConvertHex)

# read also next example below
for token in fltrd.emit_from(content):
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
ipret.run_all(fltrd.emit_from(content))

r = ipret.result()
p(r)

# do more comfy

os.remove("test.flt.txt")

with FlatFile("test.flt.txt", "w", converter=ConvertHex) as f:
    f.write(d)

with FlatFile("test.flt.txt", converter=ConvertHex) as f:
    test_dic = f.read()

p(test_dic)

print("equal?", test_dic == d)
del test_dic["a"]
print("equal?", test_dic == d)

#
# without converter and without nl in output
#

os.remove("test.flt.txt")

with FlatFile("test.flt.txt", "w", converter=Convert) as f:
    f.write(d, write_nl=False)

with FlatFile("test.flt.txt", converter=Convert) as f:
    test_dic = f.read(split_lines=False)

p(test_dic)

print("equal?", test_dic == d)
del test_dic["a"]
print("equal?", test_dic == d)

#
# with readable converter output and nl in output
#

os.remove("test.flt.txt")

with FlatFile("test.flt.txt", "w", converter=ConvertUTF8) as f:
    f.write(d, write_nl=True)

with FlatFile("test.flt.txt", converter=ConvertUTF8) as f:
    test_dic = f.read()

p(test_dic)

print("equal?", test_dic == d)
del test_dic["a"]
print("equal?", test_dic == d)
