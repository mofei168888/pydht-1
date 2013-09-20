

def port_ntol(s):
    p = []
    q = []
    for i in s:
        b = bin(i).replace("0b", "")
        p.append(b)

    for i in p:
        while len(i) < 8:
            i = "0" + i
        q.append(i)

    s = "0b" + q[1] + q[0]

    return int(s, 2)
            


s = b'\xc2^'

print(port_ntol(s))