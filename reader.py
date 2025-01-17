from html.parser import HTMLParser
import requests
import argparse
import os


class Reader(HTMLParser):
    def __init__(self, file_handle=None):
        super().__init__()
        self.print_me = False
        self.file_handle = file_handle

    def handle_starttag(self, tag, attrs):
        if tag == "p":
            self.print_me = True

    def handle_endtag(self, tag):
        if tag == "p":
            self.print_me = False
            if self.file_handle:
                self.file_handle.write(os.linesep)
            else:
                print("")

    def handle_data(self, data):
        if self.print_me:
            if self.file_handle:
                self.file_handle.write(data)
                self.file_handle.write(os.linesep)
            else:
                print(data)


def main():
    parser = argparse.ArgumentParser(description="Provide news article and file path if you desire to save it.")
    parser.add_argument("url", type=str, help="URL of article to read.")
    parser.add_argument("--output", dest='output', type=str, help="filename to write to.")

    args = parser.parse_args()

    file_handle = None
    if args.output:
        file_name = args.output
        file_handle = open(file_name, 'w')

    htmlparser = Reader(file_handle)
    htmlparser.feed(requests.get(args.url).text)


if __name__ == "__main__":
    main()
