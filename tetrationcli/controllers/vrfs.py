from cement import Controller, ex
import json

class VRFs(Controller):

    class Meta:
        label = 'vrfs'
        stacked_type = 'nested'
        # stacked_on = 'base'

    @ex(help='list vrfs')
    def list(self):
        restclient = self.app.tetpyclient
        response = restclient.get('/vrfs')
        self.app.log.debug('command returned: %s' % response.status_code)
        data = json.loads(response.content.decode("utf-8"))
        
        headers = ['VRF ID', 'Name']
        data_list = [[x['id'],
                    x['name']] for x in data ]

        self.app.render(data_list, headers=headers)
    
    @ex(help='delete')  
    def delete(self):
        self.app.log.error('FEATURE NOT IMPLEMENTED YET, OPEN A ISSUE')
