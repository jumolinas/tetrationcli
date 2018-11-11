from cement import Controller, ex
import json

class Sensors(Controller):

    class Meta:
        label = 'sensors'
        stacked_type = 'embedded'
        stacked_on = 'base'

    @ex(help='list sensors')
    def sensors(self):
        restclient = self.app.tetpyclient
        response = restclient.get('/sensors')
        self.app.log.debug('command returned: %s' % response.status_code)
        data = {}
        data = json.loads(response.content.decode("utf-8"))
        self.app.log.debug('data returned: %s' % data)
        self.app.render(data, 'sensors_list.jinja2')