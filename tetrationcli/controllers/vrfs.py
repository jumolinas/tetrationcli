from cement import Controller, ex
import json

class VRFs(Controller):

    class Meta:
        label = 'vrfs'
        stacked_type = 'embedded'
        stacked_on = 'base'

    @ex(help='list vrfs')
    def vrfs(self):
        restclient = self.app.tetpyclient
        response = restclient.get('/vrfs')
        self.app.log.debug('command returned: %s' % response.status_code)
        data = {}
        data['results'] = json.loads(response.content.decode("utf-8"))
        self.app.log.debug('data returned: %s' % data)
        self.app.render(data, 'vrfs_list.jinja2')