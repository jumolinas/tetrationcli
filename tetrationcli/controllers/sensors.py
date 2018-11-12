from cement import Controller, ex
import json

class Sensors(Controller):

    class Meta:
        label = 'sensors'
        stacked_type = 'nested'
        # stacked_on = 'base'

    @ex(help='list sensors')
    def list(self):
        restclient = self.app.tetpyclient
        response = restclient.get('/sensors')
        self.app.log.debug('command returned: %s' % response.status_code)
        data = {}
        data = json.loads(response.content.decode("utf-8"))
        self.app.log.debug('data returned: %s' % data)
        self.app.render(data, 'sensors_list.jinja2')

    @ex(help='create')
    def create(self):
        pass
    
    @ex(help='delete')
    def remove(self):
        pass

    @ex(help='update')
    def update(self):
        pass