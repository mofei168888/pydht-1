#! /usr/bin/env python3


def bdecode(x):
    try:
        r, l = decode_func[x[0]](x, 0)
        return r
    except (IndexError, KeyError, ValueError):
        pass


def decode_int(x, f):
    f += 1
    newf = x.index("e", f)
    n = int(x[f:newf])
    return (n, newf+1)


def decode_string(x, f):
    coln = x.index(":", f)
    n = int(x[f:coln])
    coln += 1
    return (x[coln:coln+n], coln+n)


def decode_list(x, f):
    r,f = [], f+1
    while x[f] != "e":
        v, f = decode_func[x[f]](x, f)
        r.append(v)
    return (r, f+1)


def decode_dict(x, f):
    r, f = {}, f+1
    while x[f] != "e":
        k, f = decode_string(x, f)
        r[k], f = decode_func[x[f]](x, f)
    return (r, f+1)


decode_func = {}
decode_func['l'] = decode_list
decode_func["d"] = decode_dict
decode_func['i'] = decode_int
decode_func['0'] = decode_string
decode_func['1'] = decode_string
decode_func['2'] = decode_string
decode_func['3'] = decode_string
decode_func['4'] = decode_string
decode_func['5'] = decode_string
decode_func['6'] = decode_string
decode_func['7'] = decode_string
decode_func['8'] = decode_string
decode_func['9'] = decode_string


def bencode(x):
    r = []
    encode_func[type(x)](x, r)
    return "".join(r)


def encode_int(x, r):
    r.extend(("i", str(x), "e"))


def encode_string(x, r):
    r.extend((str(len(x)), ":", x))


def encode_list(x, r):
    r.append("l")
    for i in x:
        print(type(i))
        encode_func(type(i))(i, r)
    r.append("e")


def encode_dict(x, r):
    r.append("d")
    ilist = sorted(x.items())
    ilist.sort()
    for k, v in ilist:
        r.extend((str(len(k)), ":", k))
        encode_func[type(v)](v, r)
    r.append("e")


encode_func = {}
encode_func[type(3)] = encode_int
encode_func[type("")] = encode_string
encode_func[type([])] = encode_list
encode_func[type(())] = encode_list
encode_func[type({})] = encode_dict


if __name__ == "__main__":
    e = {"t": "aa", "y": "q", "q": "ping", "a": {"id": "abcdefghij0123456789"}}
    d = "d1:ad2:id20:abcdefghij0123456789e1:q4:ping1:t2:aa1:y1:qe"

    assert bencode(e) == d
    assert bdecode(d) == e
