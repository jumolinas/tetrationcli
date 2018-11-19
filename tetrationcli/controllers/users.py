from cement import Controller, ex
import json

class Users(Controller):

    class Meta:
        label = 'users'
        stacked_type = 'nested'
        # stacked_on = 'base'

    @ex(help='list users')
    def list(self):
        restclient = self.app.tetpyclient
        response = restclient.get('/users')
        self.app.log.debug('command returned: %s' % response.status_code)
        data = {
            'results': json.loads(response.content.decode("utf-8"))
        }
        
        self.app.log.debug('data returned: %s' % data)
        self.app.render(data, 'users_list.jinja2')

    @ex(help='create')
    def create(self):
        self.app.log.error('FEATURE NOT IMPLEMENTED YET, OPEN A ISSUE')
    
    @ex(help='delete')
    def remove(self):
        self.app.log.error('FEATURE NOT IMPLEMENTED YET, OPEN A ISSUE')

    @ex(help='update')
    def update(self):
        self.app.log.error('FEATURE NOT IMPLEMENTED YET, OPEN A ISSUE')