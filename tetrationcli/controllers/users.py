from cement import ex
from .tet_controller import TetController
import json

class Users(TetController):

    class Meta:
        label = 'users'
        stacked_type = 'nested'
        # stacked_on = 'base'

    @ex(help='list users')
    def list(self):
        restclient = self.app.tetpyclient
        response = self.tetration().get('/users')
        self.app.log.debug('{0} - {1}'.format(response.status_code,
                                                response.content.decode('utf-8')))
        data = json.loads(response.content.decode("utf-8"))
        
        headers = ['User ID', 'Name', 'e-Mail']
        data_list = [[x['id'],
                    '{0} {1}'.format(x['first_name'],x['last_name']),
                    x['email']] for x in data ]

        self.app.render(data_list, headers=headers)

    @ex(help='delete')
    def delete(self):
        self.app.log.error('FEATURE NOT IMPLEMENTED YET, OPEN A ISSUE')
