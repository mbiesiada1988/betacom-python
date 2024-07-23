from json import dump
from time import time
from support.crawler import APICrawler

RESOURCES_TO_CHECK = 15
CRAWLER = APICrawler()


def test_tree0():
    try:
        CRAWLER.crawl(0, RESOURCES_TO_CHECK)
    except IndexError:
        raise IndexError(f'Number of resources less than {RESOURCES_TO_CHECK}')
    finally:
        with open(f'output/{time()}_API_tree0.json', 'w', encoding='utf-8') as output_file:
            dump(CRAWLER.output, output_file, indent=2, ensure_ascii=False)


def test_tree1():
    try:
        CRAWLER.crawl(1, RESOURCES_TO_CHECK)
    except IndexError:
        raise IndexError(f'Number of resources less than {RESOURCES_TO_CHECK}')
    finally:
        with open(f'output/{time()}_API_tree1.json', 'w', encoding='utf-8') as output_file:
            dump(CRAWLER.output, output_file, indent=2, ensure_ascii=False)
