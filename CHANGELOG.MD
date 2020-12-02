
# Changelog


## next release v0.0.5

- dropped `DictTokenizer` init parameter emitType=True. `TerminalValueType` is now always send to the stream
- 


## release v0.0.4

- **IMPORTANT**: changed FlatFile, FlatWriter, FlatReader internal token representation to `#k#`,`#i#`,`#s#`,`#t#`,`#c#`, and `#v#` 
 (key, index, set, tuple, typecast, and terminal value). **this is an incompatible change!!!**
- added [`TabFlatWriter` and `TabFlatReader`](https://github.com/kr-g/pyreflat/blob/main/pyreflat/tab_flat.py) 
 as most readable option to persist the token stream. 
 tokens and terminal value are written in a tab separated text file, followed by newline
- reworked FlatFile read and write methods to accept a writer and reader parameter

such as :

    with FlatFile(fnam, "w", converter=ConvertUTF8) as f:
        f.write(test_dict, writer=TabFlatWriter)

    with FlatFile(fnam, converter=ConvertUTF8) as f:
        dic = f.read(reader=TabFlatReader)

- 


## release v0.0.3

- added `TerminalWriter` class for creating a list with all terminal values only (1-way transformation)
- added `AnynomusPathWriter` class for creating a list with tupel( path, val ) pairs, where path is stripped 
 off any index information for latter seaching on a more abstract level (1-way transformation)
- 


## release v0.0.2

- added `FlatFile` for easy writing and reading
- reworked new line handling with custom `Converter` class
- added `ConvertUTF8` for readable format with escaped sequences such as \n,\t
- 


## release v0.0.1

- first release
