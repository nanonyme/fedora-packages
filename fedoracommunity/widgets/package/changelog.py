import tw2.core as twc
from fedoracommunity.widgets.grid import Grid
from fedoracommunity.connectors.api import get_connector

class ChangelogGrid(Grid):
    template='mako:fedoracommunity.widgets.package.templates.changelog_table_widget'
    resource='koji'
    resource_path='query_changelogs'

    def prepare(self):
        self.filters = {'build_id': self.build_id}
        self.rows_per_page = 10

        # Must do this last for our Grids
        super(ChangelogGrid, self).prepare()


class ChangelogWidget(twc.Widget):
    template = 'mako:fedoracommunity.widgets.package.templates.changelog'
    changelog_grid = ChangelogGrid

    def prepare(self):
        self.package_name = self.kwds['package_name']
        self.subpackage_of = self.kwds.get('subpackage_of', '')
        xapian = get_connector('xapian')

        if self.subpackage_of:
            latest_builds = xapian.get_latest_builds(self.subpackage_of)
        else:
            latest_builds = xapian.get_latest_builds(self.package_name)

        self.default_build_id = latest_builds['Rawhide']['build_id']
        self.latest_builds = latest_builds

