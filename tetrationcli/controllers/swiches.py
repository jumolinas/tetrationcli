from cement import ex
from .tet_controller import TetController
import json

class Switches(TetController):

    class Meta:
        label = 'switches'
        stacked_type = 'nested'
        help= 'Interact with Hardware Sensors from Tetration Cluster'

    @ex(help='list hardware sensors')
    def list(self):
        response = self.tetration().get('/switches')
        self.app.log.debug('{0} - {1}'.format(response.status_code,
                                                response.content.decode('utf-8')))
        data = json.loads(response.content.decode("utf-8"))
        
        headers = ['IP', 'Name', 'Serial', 'NXOS Version']
        data_list = [[x['ip'],
                    x['name'],
                    x['serial'],
                    x['nxos_version']] for x in data ]

        self.app.render(data_list, headers=headers)

