from time import time
from json import dump
from playwright.sync_api import Page
from support.crawler import GUICrawler

RESOURCES_TO_CHECK = 15
CRAWLER = GUICrawler()


def test_tree0(page: Page):
    try:
        CRAWLER.crawl(page, 0, RESOURCES_TO_CHECK)
    except IndexError:
        raise IndexError(f'Number of resources less than {RESOURCES_TO_CHECK}')
    finally:
        with open(f'output/{time()}_GUI_tree0.json', 'w', encoding='utf-8') as output_file:
            dump(CRAWLER.output, output_file, indent=2, ensure_ascii=False)


def test_tree1(page: Page):
    try:
        CRAWLER.crawl(page, 1, RESOURCES_TO_CHECK)
    except IndexError:
        raise IndexError(f'Number of resources less than {RESOURCES_TO_CHECK}')
    finally:
        with open(f'output/{time()}_GUI_tree1.json', 'w', encoding='utf-8') as output_file:
            dump(CRAWLER.output, output_file, indent=2, ensure_ascii=False)
