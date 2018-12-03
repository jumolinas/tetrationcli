from cement import ex
from .tet_controller import TetController
import json

class Applications(TetController):
    
    class Meta:
        label = 'applications'
        stacked_type = 'nested'
    
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
 
        headers = ['Application ID', 'Name', 'Scope ID']
        data_list = [[x['id'],
                    x['name'],
                    x['app_scope_id']] for x in content ]
        

        self.app.render(data_list, headers=headers)
