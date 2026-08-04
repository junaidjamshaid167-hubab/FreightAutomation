from bs4 import BeautifulSoup


def parse_table(html):
    soup = BeautifulSoup(html, "lxml")
    return soup