from cement import Controller, ex
import json

class Roles(Controller):

    class Meta:
        label = 'roles'
        stacked_type = 'embedded'
        stacked_on = 'base'

    @ex(help='list roles')
    def roles(self):
        restclient = self.app.tetpyclient
        response = restclient.get('/roles')
        self.app.log.debug('command returned: %s' % response.status_code)
        data = {}
        data['results'] = json.loads(response.content.decode("utf-8"))
        self.app.log.debug('data returned: %s' % data)
        self.app.render(data, 'roles_list.jinja2')