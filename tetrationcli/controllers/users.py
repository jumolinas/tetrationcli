from cement import ex
from .tet_controller import TetController
import json

class Users(TetController):

    class Meta:
        label = 'users'
        stacked_type = 'nested'
        help= 'Interact with Users from Tetration Cluster'

    @ex(help='list users')
    def list(self):
        response = self.tetration().get('/users')
        self.app.log.debug('{0} - {1}'.format(response.status_code,
                                                response.content.decode('utf-8')))
        
        if response.status_code == 403:
            self.app.log.error('{0}Request "user_role_scope_management" permissions'
                                    .format(response.content.decode('utf-8')))
            return
        
        data = json.loads(response.content.decode("utf-8"))
        
        headers = ['User ID', 'Name', 'e-Mail']
        data_list = [[x['id'],
                    '{0} {1}'.format(x['first_name'],x['last_name']),
                    x['email']] for x in data ]

        self.app.render(data_list, headers=headers)

