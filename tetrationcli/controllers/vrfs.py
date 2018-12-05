from cement import ex
from .tet_controller import TetController
import json

class VRFs(TetController):

    class Meta:
        label = 'vrfs'
        stacked_type = 'nested'
        help= 'Interact with VRFs in Tetration Cluster'

    @ex(help='list vrfs')
    def list(self):
        response = self.tetration().get('/vrfs')
        self.app.log.debug('{0} - {1}'.format(response.status_code,
                                                response.content.decode('utf-8')))
        data = json.loads(response.content.decode("utf-8"))
        
        headers = ['VRF ID', 'Name']
        data_list = [[x['id'],
                    x['name']] for x in data ]

        self.app.render(data_list, headers=headers)
    
