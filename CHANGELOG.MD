
# Changelog

## next release v0.0.4

- changed FlatFile, FlatWriter, FlatReader internal token representation to `#k#`,`#i#`,`#s#`,`#t#`,`#c#`, or `#v#` 
- added TabFlatWriter and TabFlatReader as most readable option to persist the token stream. 
 token and terminal are written in a tab separated text file, followed by newline
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
