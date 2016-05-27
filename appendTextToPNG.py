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

if len(argv) == 3:
    if posixpath.exists(argv[1]) and posixpath.exists(argv[2]):
	iname = argv[1]
	pname = argv[2]
    else:
	print "files do not exist"
	raise SystemExit

elif len(argv) == 4:
    if posixpath.exists(argv[3]):
        iname = None
        key = argv[1]
        text = argv[2]
        pname = argv[3]
    else:
        print "file does not exist"
        raise SystemExit

else: # usage
    print "Usage: %s <file> <png>" % argv[0]
    print "\tReads data from <file> and appends its data as text-chunk (tEXt) to the <png> file\n"
    print "Usage: %s <key> <text> <png>" % argv[0]
    print "\tUse inline <key> and <text> to append them as text-chunk (tEXt) to the <png> file\n"
    print "\tthe text is added as second-to-last chunk (last chunk is always the magic PNG ending)"
    print "\tthe new PNG data is written to standard output"
    raise SystemExit

if iname is None:
    input_data = (key + "\x00" + text)
else:
    ihandle = open(iname, "rb")
    input_data = ihandle.read()
    ihandle.close()


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

# check for last chunk
iend_index = img_data.index("IEND")-4
img_data_pre = img_data[:iend_index]
img_data_post = img_data[iend_index:]

# new chunk
length = struct.pack(">I", len(input_data))
chunktype = "tEXt"
chunk_crc = zlib.crc32(chunktype)
chunk_crc = zlib.crc32(input_data, chunk_crc)
chunk_crc  &= 2**32 - 1 # see # http://bugs.python.org/issue1202, lol
chunk_crc = struct.pack("!I", chunk_crc)
newchunk = (length + chunktype + input_data + chunk_crc)

# new image = old image + new chunk before "end of image" chunk
stdout.write(img_data_pre + newchunk + img_data_post)
