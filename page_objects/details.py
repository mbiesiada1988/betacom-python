class DetailsPageObject:
    def __init__(self, page):
        self.page = page
        self.title = page.locator('.resource-summary__title')
        self.rate = page.locator('div.rating__row').locator('span').first
        self.thumbnail = page.get_by_alt_text('Resource cover')
        self.description = page.locator('p.resource-description__description-wrapper')
        self.tab_path = page.get_by_role('tab', name="Path")
        self.path = page.locator('div.library-path__path-tree')
        self.path_nodes = page.locator('span.library-path__path-tree-name')
        self.tab_metadata = page.get_by_role('tab', name="Metadata")
        self.metadata = page.locator('app-metadata-view.resource-details__metadata')
        self.tab_keywords = page.get_by_role('tab', name="Keywords")
        self.keywords = page.locator('div.keyword-component__keywords')
        self.back_button = page.get_by_role('button', name="Navigate Back")

    def parse_description(self):
        if self.description.count() > 0:
            return self.description.inner_text()
        return ""

    def parse_path(self):
        parsed = list()
        for node in self.path_nodes.all():
            parsed.append(node.text_content())
        return ' > '.join(parsed)

    def parse_metadata(self):
        parsed = dict()
        metadata_titles = self.page.locator('span.metadata-item__title').all()
        metadata_values = self.page.locator('p.metadata-item__value').all()
        for title, value in zip(metadata_titles, metadata_values):
            parsed[title.inner_text()] = value.inner_text()
        return parsed

    def parse_keywords(self):
        parsed = list()
        for keyword in self.page.locator('span.keyword-component__name').all():
            parsed.append(keyword.inner_text())
        return parsed
