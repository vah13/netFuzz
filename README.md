# netFuzzTapor
![Logo](http://www.logosolinfo.ru/store/media/catalog/product/cache/9/image/9df78eab33525d08d6e5fb8d27136e95/4/8/485-gr_nsfors-bruks-knutyxa.jpg)
This another fuzzer for netRequests
how use
1. need install radamsa from https://github.com/aoh/radamsa
```
netFuzz_main.py --dfile <inputfile> -n <loop_count> -o <remote_address> -p <port> -m <fuzz_mode> -s <seed> -b <bypass_fuzz_package>
```
inputfile -> package or packages file in hex format like this (\n - separation packages char)
```
414141\n
424242\n
10111213\n
```
* -n -> mutation package count
* -o -> remote address
* -p -> remote port
* -m -> fuzz mode
        m = 0 for dumb fuzzing
        m = 1 for step-by-step fuzzing (use where need send handshake)
* -s -> fuzzing seed
* -b -> which package should be sent without the mutation

example
```
root@kali:~/Desktop/netFuzz# cat test.bin | hexdump
0000000 4141 4141 4141 4141 420a 4242 4242 4242
0000010 0a42
```
1. run netFuzz_testServer.py and listn 8080 port

2. run fuzzer with --dfile ./test.bin parametr
```
/usr/bin/python2.7 /root/Desktop/netFuzz/netFuzz_main.py --dfile ./test.bin
('Fuzz input file is ', './test.bin')
('Fuzz loop count ', 1)
('Fuzz address:port ', '192.168.213.1:8080')
Fuzz mode -m=1 step-by-step fuzzing,  -m=0 dumb fuzzing
('Fuzz seed ', '60906781022444159195513')
('Fuzz bypass package (experimental)', '10')
```
fuzzer will send to *:8080 2 package 
```
New connection from 192.168.213.138
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA�󠁟�AA�󠁟�AAAAAAAA
BBBBBBBB


New connection from 192.168.213.138
AAAAAAAA

BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB�󠁟�BB�󠁟�BBBBBBBB

```


founded

CVE           | program    | credit
--------------|------------|-----------
CVE-2015-2819 | Sybase SQL    | vah_13 (ERPScan)
CVE-2015-2820 | SAP Afaria    | vah_13 (ERPScan)
CVE-2015-8330 | SAP PCo agent | Mathieu GELI (ERPScan)
CVE-2016-1928 | SAP HANA hdbxsengine |Mathieu Geli (ERPScan)
