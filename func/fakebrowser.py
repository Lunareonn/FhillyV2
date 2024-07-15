import urllib.request

def fakebrowser(url: str):
    opener = urllib.request.build_opener()
    opener.addheaders = [("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36")]
    urllib.request.install_opener(opener)
    urllib.request.urlretrieve(url, "temp/image.png")
