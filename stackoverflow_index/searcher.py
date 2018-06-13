import datetime

import struct
offset_dict = {}

try:
    with open('./post_inv_offset.dat', mode='rb') as r:
        cnt = 0
        while True:
            term_leng = struct.unpack('i', r.read(4))[0]
            term = r.read(term_leng).decode("utf-8")
            offset = struct.unpack('i', r.read(4))[0]
            offset_dict[term] = offset
except:
    print("EXCEPT")
    pass

def search(term, fp):
    fp.seek(offset_dict[term])

    whole_leng = struct.unpack('i', r.read(4))[0]
    len_str = struct.unpack('i', r.read(4))[0]
    whole_leng -= len_str
    read_term = r.read(len_str).decode("utf-8")
    assert(read_term==term)
    data = list()
    while whole_leng > 0:
        id, date, wc = struct.unpack('iii', r.read(12))
        whole_leng -= 12
        data.append((id, date, wc))
    return data

with open('./post_inv_idx.dat', mode='rb') as r:
    print(len(search('numpy', r)))
    print(len(search('os', r)))
    print(len(search('pandas', r)))
    print(len(search('datetime', r)))
    print(len(search('scipy', r)))
