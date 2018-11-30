from cement import Controller, ex
import json

class Applications(Controller):
    
    class Meta:
        label = 'applications'
        stacked_type = 'nested'
        # stacked_on = 'base'
    
    @ex(help='list applications', arguments=[
            (['-all'],
                    {'help': 'Show more columns', 'action': 'store_true', 'dest': 'all'})
    ])
    def list(self):
        """
        Return the list of all the applications
        """
        restclient = self.app.tetpyclient
        response = restclient.get('/applications')
        content = json.loads(response.content.decode("utf-8"))
        self.app.log.debug('{0} - {1}'.format(response.status_code,
                                                response.content.decode('utf-8')))
 
        headers = ['Application ID', 'Name', 'Scope ID']
        data_list = [[x['id'],
                    x['name'],
                    x['app_scope_id']] for x in content ]
        

        self.app.render(data_list, headers=headers)

    @ex(help='delete application', arguments=[
            (['-application'],
                {'help': 'Application ID', 'action': 'store', 'dest': 'application_id'})
    ])
    def delete(self):
        """
        DELETE /openapi/v1/applications/{application_id}
        """
        data = {
            'application_id': self.app.pargs.application_id
        }
        restclient = self.app.tetpyclient
        response = restclient.delete('/applications/{0}'.format(data['application_id']))
        self.app.log.debug('{0} - {1}'.format(response.status_code,
                                                response.content.decode('utf-8')))
        if response.status_code in [200,204]:
            self.app.log.info('Deleted Application {0}'.format(data['application_id']))
        else:
            error_message = json.loads(response.text)
            self.app.log.error('Error: {0} \n> Message {1}'.format(error_message['status'],
                                                                error_message['error']))
