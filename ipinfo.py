from requests_html import HTMLSession
import argparse


class IpInfo:
    def __init__(self):
        self.session = HTMLSession()
        self.base = 'https://ipinfo.io/'
        self.r = None
        self.header = {
            'Accept': 'application/json',
        }

    @staticmethod
    def pairwise(data):
        a = iter(data)
        return zip(a, a)

    def run(self, ip=None):
        if ip is None:
            ip = self.session.get(self.base, headers=self.header).json()['ip']
        self.r = self.session.get(self.base + ip)
        texts = self.r.html.find('ul.address-list')
        info = []
        for text in texts:
            for item in text.find('span'):
                info.append(item)
        for x, y in self.pairwise(info):
            print("{}: {}".format(x.text, y.text))


def main():
    ipinfo = IpInfo()
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", type=str, help="IP Address to lookup")
    args = parser.parse_args()
    if args.i is None:
        ipinfo.run()
    else:
        ipinfo.run(args.i)


if __name__ == '__main__':
    main()
