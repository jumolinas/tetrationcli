from cement import ex
from .tet_controller import TetController
import json

class Inventory(TetController):

    class Meta:
        label = 'inventory'
        stacked_type = 'nested'
        help= 'Interact with Inventory from Tetration Cluster'

    @ex(help='List inventories', arguments=[
        (['-all'],
            {'help': 'Show more columns', 'action': 'store_true', 'dest': 'all'})
    ])
    def list(self):
        """
        """
        response = self.tetration().get('/filters/inventories')
        self.app.log.debug('{0} - {1}'.format(response.status_code,
                                                response.content.decode('utf-8')))
        
        if response.status_code == 403:
            self.app.log.error('{0}Request "flow_inventory_query" permissions'.format(response.content.decode('utf-8')))
            return

        data = json.loads(response.content.decode('utf-8'))
        headers = ['UUID', 'Name', 'Scope ID', 'Query']
        data_list = [[x['id'],
                    x['name'],
                    x['app_scope_id'],
                    x['short_query']] for x in data ]

        self.app.render(data_list, headers=headers)

    @ex(help='List inventory details', arguments=[
        (['-id'],
            {'help': 'Inventory ID', 'action': 'store', 'dest': 'inventory_id'})
    ])
    def details(self):
        """
        """
        data = {
            'inventory_id': self.app.pargs.inventory_id
        }

        response = self.tetration().get('/filters/inventories/{0}'.format(data['inventory_id']))
        self.app.log.debug('{0} - {1}'.format(response.status_code,
                                                response.content.decode('utf-8')))

        if response.status_code == 403:
            self.app.log.error('{0}Request "flow_inventory_query" permissions'.format(response.content.decode('utf-8')))
            return

        data = json.loads(response.content.decode('utf-8'))
        UUID = data['id']
        NAME = data['name']
        SCOPE_ID = data['app_scope_id']
        headers = ['UUID', 'Name', 'Scope ID', 'Query']
        data_list = [[UUID,
                        NAME,
                        SCOPE_ID,
                        x] for x in data['query']['filters']]


        self.app.render(data_list, headers=headers)

    
