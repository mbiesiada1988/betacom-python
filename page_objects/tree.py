class TreePageObject:
    def __init__(self, page):
        self.page = page
        self.resources = page.locator(".resources-card-beta")

    def tree_tab(self):
        return self.page.get_by_role('tab')

    def resource(self, index):
        return self.resources.all()[index]
