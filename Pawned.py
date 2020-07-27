import requests
import hashlib 
import sys

def check(pwd):
    sha1pwd = hashlib.sha1(pwd.encode('utf-8')).hexdigest().upper()
    head, tail = sha1pwd[:5], sha1pwd[5:]

    url = 'https://api.pwnedpasswords.com/range/' + head

    res = requests.get(url)

    hashes = (line.split(":") for line in res.text.splitlines())
    count = next((int(count) for t, count in hashes if t==tail), 0 )

    return sha1pwd, count 



print(check(sys.argv[1]))
