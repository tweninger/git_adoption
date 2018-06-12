import struct
inv_idx = dict()

try:
    with open('./post_inv_idx.json', mode='rb') as r:
        buff = bytearray()
        first = True
        cnt = 0


        while True:
            whole_leng = struct.unpack('i', r.read(4))[0]
            len_str = struct.unpack('i', r.read(4))[0]
            whole_leng -= len_str
            term = r.read(len_str).decode("utf-8")
            data = list()
            while whole_leng > 0:
                id, date, wc = struct.unpack('iii', r.read(12))
                whole_leng -= 12
                data.append((date, wc))
            if len(data) > 2000:
                if cnt %2000 == 0:
                    print(term)
                inv_idx[term] = len(data)
except:
    pass
print("LOADED")
print(inv_idx['numpy'])


    #w.write(bytes(key, encoding="utf8"))
    #for v in inv_idx[key]:
    #    w.write(struct.pack('i', v.id))struct.unpack('iii', buff[-12:])
    #    w.write(struct.pack('i', v.date))
    #    w.write(struct.pack('i', v.viewcount))
    #w.write(bytes('\n', encoding="utf8"))

