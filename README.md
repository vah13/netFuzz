# netFuzzTapor
This another fuzzer for netRequests
how use
1. need install radamsa from https://github.com/aoh/radamsa
```
netFuzz_main.py --dfile <inputfile> -n <loop_count> -o <remote_address> -p <port> -m <fuzz_mode> -s <seed> -b <bypass_fuzz_package>
```
inputfile -> package or packages file in hex format like this (0a - separation packages char)
```
60 00 00 00 03 5b 00 00 01 00 00 00 ff ff ff ff
00 00 04 00 60 00 00 00 00 02 48 00 04 09 00 00
00 40 00 00 d0 3f 00 00 00 40 00 00 70 00 00 00
50 4f 50 00 00 00 00 00 00 00 00 00 00 00 00 00
07 49 35 31 36 34 00 04 50 1c 20 03 59 01 03 72
01 09 70 64 62 6d 73 72 76 00 06 58 50 4f 50 00
*0a* 28 00 00 00 03 3f 00 00 01 00 00 00 9c 77 00
00 00 00 04 00 28 00 00 00 64 62 6d 5f 76 65 72
73 69 6f 6e 20 20 20 20 20
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
