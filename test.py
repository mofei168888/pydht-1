import hashing
import hashlib
import b


if __name__ == "__main__":
    with open("20130831074709741.torrent", encoding="latin-1") as f:
        s = f.read()
        ss = b.bdecode(s)
        info = b.bencode(ss["info"])
        print(hashlib.sha1(info.encode()).hexdigest())
