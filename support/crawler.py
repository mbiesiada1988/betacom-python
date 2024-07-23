from config import config
from requests import get
from page_objects.tree import TreePageObject
from page_objects.details import DetailsPageObject


class GUICrawler:
    def __init__(self):
        self.output = dict()

    def crawl(self, page, tree_index, resources_to_check):
        tree = TreePageObject(page)
        details = DetailsPageObject(page)
        tree.page.goto(f'{config["host"]}{config["path_gui"]}')
        tree.tree_tab().first.wait_for()
        tree.tree_tab().all()[tree_index].click()
        tree.resources.first.wait_for()
        for resource_index in range(resources_to_check):
            tree.resource(resource_index).click()
            resource_output = dict()
            details.title.wait_for()
            resource_output['title'] = details.title.text_content()
            resource_output['rate'] = details.rate.text_content()[1:]
            resource_output['thumbnail'] = details.thumbnail.get_attribute('src')
            resource_output['description'] = details.parse_description()
            details.tab_path.click()
            details.path.wait_for()
            resource_output['path'] = details.parse_path()
            details.tab_metadata.click()
            details.metadata.wait_for()
            resource_output['metadata'] = details.parse_metadata()
            details.tab_keywords.click()
            details.keywords.wait_for()
            resource_output['keywords'] = details.parse_keywords()
            details.back_button.click()
            tree.resources.first.wait_for()
            self.output[resource_index] = resource_output


class APICrawler:
    def __init__(self):
        self.url = f'{config["host"]}{config["path_api"]}'
        self.params_tree = {'targetRole': 'anonymous'}
        self.headers = {'X-Preferred-Language': 'en-US'}
        self.output = dict()

    def get_trees_ids(self):
        ids = list()
        trees = get(f'{self.url}trees', params=self.params_tree, verify=False).json()
        for tree in trees:
            ids.append(tree['rootId'])
        return ids

    @staticmethod
    def parse_rate(rate_response):
        if rate_response['numRatings'] > 0:
            return rate_response['rating']
        return 'Not rated yet'

    @staticmethod
    def parse_description(details):
        try:
            return details['description']
        except KeyError:
            return ""

    @staticmethod
    def parse_path(paths):
        nodes = list()
        for node in paths[0]['paths'][0]['path']:
            nodes.append(node['name'])
        return ' > '.join(nodes)

    @staticmethod
    def parse_metadata(details):
        parsed = dict()
        for tag in details['tags']:
            if 'textValue' in tag.keys():
                parsed[tag['displayName']] = tag['textValue']
            if 'values' in tag.keys():
                values = [value['displayName'] for value in tag['values']]
                parsed[tag['displayName']] = ', '.join(values)
        return parsed

    def crawl(self, tree_id, resources_to_check):
        resources = get(
            f'{self.url}resources',
            params={'node': self.get_trees_ids()[tree_id], 'sort': 'externalId', 'dir': 'asc', 'limit': 15},
            headers=self.headers,
            verify=False
        ).json()
        for resource_index in range(resources_to_check):
            resource_output = dict()
            details = get(
                f'{self.url}resources/{resources[resource_index]["id"]}',
                headers=self.headers,
                verify=False
            ).json()
            rate = get(
                f'{self.url}resources/{resources[resource_index]["id"]}/rating',
                headers=self.headers,
                verify=False
            ).json()
            paths = get(
                f'{self.url}resources/{resources[resource_index]["id"]}/paths',
                headers=self.headers,
                verify=False
            ).json()
            resource_output['title'] = details['title']
            resource_output['rate'] = self.parse_rate(rate)
            resource_output['thumbnail'] = f'{config["host"]}{details["thumbnail"]}'
            resource_output['description'] = self.parse_description(details)
            resource_output['path'] = self.parse_path(paths)
            resource_output['metadata'] = self.parse_metadata(details)
            resource_output['keywords'] = details['keywords']
            self.output[resource_index] = resource_output
