from cement import Controller, ex
import json

class Switches(Controller):

    class Meta:
        label = 'switches'
        stacked_type = 'nested'
        # stacked_on = 'base'

    @ex(help='list hardware sensors')
    def list(self):
        restclient = self.app.tetpyclient
        response = restclient.get('/switches')
        self.app.log.debug('command returned: %s' % response.status_code)
        data = json.loads(response.content.decode("utf-8"))
        
        headers = ['IP', 'Name', 'Serial', 'NXOS Version']
        data_list = [[x['ip'],
                    x['name'],
                    x['serial'],
                    x['nxos_version']] for x in data ]

        self.app.render(data_list, headers=headers)

    @ex(help='delete')
    def delete(self):
        self.app.log.error('FEATURE NOT IMPLEMENTED YET, OPEN A ISSUE')
