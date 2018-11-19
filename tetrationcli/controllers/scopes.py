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
        data = {
            'results': json.loads(response.content.decode("utf-8"))
        }
        
        self.app.log.debug('Scopes Data: %s' % data)
        self.app.render(data, 'scopes_list.jinja2')

    @ex(help='create')
    def create(self):
        self.app.log.error('FEATURE NOT IMPLEMENTED YET, OPEN A ISSUE')
    
    @ex(help='delete')
    def remove(self):
        self.app.log.error('FEATURE NOT IMPLEMENTED YET, OPEN A ISSUE')

    @ex(help='update')
    def update(self):
        self.app.log.error('FEATURE NOT IMPLEMENTED YET, OPEN A ISSUE')