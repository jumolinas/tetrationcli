from cement import Controller, ex
import json

class Scopes(Controller):

    class Meta:
        label = 'scopes'
        stacked_type = 'nested'
        # stacked_on = 'base'

    @ex(help='list scopes')
    def list(self):
        restclient = self.app.tetpyclient
        response = restclient.get('/app_scopes')
        self.app.log.debug('command returned: %s' % response.status_code)
        data = {}
        data['results'] = json.loads(response.content.decode("utf-8"))
        self.app.log.debug('data returned: %s' % data)
        self.app.render(data, 'scopes_list.jinja2')

    @ex(help='create')
    def create(self):
        pass
    
    @ex(help='delete')
    def remove(self):
        pass

    @ex(help='update')
    def update(self):
        pass