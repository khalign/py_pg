import requests
import hashlib
import sys


# request data from api and returns response
def request_data(chars):
    url = 'http://api.pwnedpasswords.com/range/' + chars
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching {res.status_code}, check url and try again')
    return res


# counts number of leaks the password hacked
def count_leaks(hashes, to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == to_check:
            return count
    return 0


# takes each password, encode and decrypt it with sha1 and split its first five character as api wants
def check(password):
    enc = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5, tail = enc[:5], enc[5:]
    response = request_data(first5)
    return count_leaks(response, tail)


def main(args):
    for password in args:
        count = check(password)
        if count:
            print(f'{password} was found {count} times. You should change it')
        else:
            print(f'{password} was NOT found. Carry on!')
    return 'done!'


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
