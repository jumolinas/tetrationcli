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
        
        if response.status_code == 403:
            roles_needed = '"sensor_management", "flow_inventory_query" or "hw_sensor_management"'
            self.app.log.error('{0}You need one of the three options {1}'
                                    .format(response.content.decode('utf-8'), roles_needed))
            return
        
        data = json.loads(response.content.decode("utf-8"))
        
        headers = ['VRF ID', 'Name']
        data_list = [[x['id'],
                    x['name']] for x in data ]

        self.app.render(data_list, headers=headers)
    
