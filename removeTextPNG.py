#!/usr/bin/python2
"""

Length 	Chunk type 	Chunk data 	CRC
4 bytes 	4 bytes 	Length bytes 	4 bytes



 89 50 4E 47 0D 0A 1A 0A


"""
import struct
import zlib
import posixpath

from sys import argv,stdout

if len(argv) == 2:
    if posixpath.exists(argv[1]):
        key = None
	pname = argv[1]
    else:
	print "file does not exist"
	raise SystemExit

elif len(argv) == 3:
    if posixpath.exists(argv[2]):
        key = argv[1]
        pname = argv[2]
    else:
        print "file does not exist"
        raise SystemExit

else: # usage
    print "Usage: %s <png>" % argv[0]
    print "\tRemove all text-chunks (tEXt) in the <png> file\n"
#    print "Usage: %s <key> <png>" % argv[0]
#    print "\tRemove text-chunks (tEXt) with <key> in the <png> file\n"
    raise SystemExit

f = open(pname, 'rb')
img_data = f.read()
#size = f.tell()
f.seek(0)
header = f.read(8)

try:
    assert header == "\x89\x50\x4E\x47\x0D\x0A\x1A\x0A"
except:
    print pname, "is not a valid PNG"
    raise SystemExit
f.close()

text_index = img_data.find("tEXt")
img_data_post = img_data
while text_index != -1:
    text_chunk = text_index-4
    length = struct.unpack(">I",img_data_post[text_chunk:text_index])[0]
    img_data_pre = img_data_post[:text_chunk]
    stdout.write(img_data_pre)
    img_data_post = img_data_post[text_index+length+8:]
    text_index = img_data_post.find("tEXt")

stdout.write(img_data_post)
