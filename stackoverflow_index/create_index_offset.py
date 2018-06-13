import struct
import datetime

try:
    with open('./post_inv_idx.dat', mode='rb') as r, open('./post_inv_offset.dat', mode='wb') as offset:
        buff = bytearray()
        cnt = 0
        cur = 0
        while True:
            cur = r.tell()
            whole_leng = struct.unpack('i', r.read(4))[0]
            len_str = struct.unpack('i', r.read(4))[0]
            whole_leng -= len_str
            term = r.read(len_str).decode("utf-8")
            k = bytes(term, encoding="utf8")
            offset.write(struct.pack('i', len_str))
            offset.write(k)
            offset.write(struct.pack('i', cur))
            r.seek(cur + whole_leng+8+len_str, )
            if cnt % 1000 == 0:
                print(term)
            cnt += 1

except:
    print("EXCEPT")
    pass
print("LOADED")
