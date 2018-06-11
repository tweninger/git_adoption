import struct
inv_idx = dict()

with open('./post_inv_idx.json', mode='rb') as r:
    buff = bytearray()
    first = True


    while True:
        whole_leng = struct.unpack('i', r.read(4))[0]
        len_str = struct.unpack('i', r.read(4))[0]
        whole_leng -= len_str
        term = r.read(len_str).decode("utf-8")
        while whole_leng > 0:
            id, date, wc = struct.unpack('iii', r.read(12))
            whole_leng -= 12
            print(term, id, date, wc)



    #w.write(bytes(key, encoding="utf8"))
    #for v in inv_idx[key]:
    #    w.write(struct.pack('i', v.id))struct.unpack('iii', buff[-12:])
    #    w.write(struct.pack('i', v.date))
    #    w.write(struct.pack('i', v.viewcount))
    #w.write(bytes('\n', encoding="utf8"))

