from cement import Controller, ex
import json

class Switches(Controller):

    class Meta:
        label = 'switches'
        stacked_type = 'embedded'
        stacked_on = 'base'

    @ex(help='list hardware sensors')
    def switches(self):
        restclient = self.app.tetpyclient
        response = restclient.get('/switches')
        self.app.log.debug('command returned: %s' % response.status_code)
        data = {}
        data['results'] = json.loads(response.content.decode("utf-8"))
        self.app.log.debug('data returned: %s' % data)
        self.app.render(data, 'switches_list.jinja2')