from cement import ex
from .tet_controller import TetController
import json

class Applications(TetController):
    
    class Meta:
        label = 'applications'
        stacked_type = 'nested'
        help= 'Interact with ADM Application from Tetration Cluster'
    
    @ex(help='list applications', arguments=[
    ])
    def list(self):
        """
        Return the list of all the applications
        """
        response = self.tetration().get('/applications')
        content = json.loads(response.content.decode("utf-8"))
        self.app.log.debug('{0} - {1}'.format(response.status_code,
                                                response.content.decode('utf-8')))
        
        if response.status_code == 403:
            self.app.log.error('{0}Request "app_policy_management" permissions'.format(response.content.decode('utf-8')))
            return
        
        headers = ['Application ID', 'Name', 'Scope ID']
        data_list = [[x['id'],
                    x['name'],
                    x['app_scope_id']] for x in content ]
        

        self.app.render(data_list, headers=headers)
