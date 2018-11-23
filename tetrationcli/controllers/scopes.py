from cement import Controller, ex
import json

class Scopes(Controller):

    class Meta:
        label = 'scopes'
        stacked_type = 'nested'
        # stacked_on = 'base'

    @ex(help='list scopes', arguments=[
        # (['-all'],
        #     {'help': 'show more columns', 'action': 'store_true', 'dest': 'all'})
        # TODO: Create option for extra columns
    ])
    def list(self):
        restclient = self.app.tetpyclient
        show_all = False
        # if self.app.pargs.all:
        #     show_all = True
        response = restclient.get('/app_scopes')
        self.app.log.debug('command returned: %s' % response.status_code)
        data = {
            'results': json.loads(response.content.decode("utf-8")),
            'all': False
        }
        
        self.app.log.debug('Scopes Data: %s' % data)
        self.app.render(data, 'scopes_list.jinja2')

    @ex(help='create new scope', arguments=[
        (['-name'],
            {'help': 'Name of the scope', 'action': 'store', 'dest': 'name'}),
        (['-query'],
            {'help': 'Query in JSON format', 'action': 'store', 'dest': 'query'}),
        (['-parent'],
            {'help': 'Parent Scope ID', 'action': 'store', 'dest': 'parent'}),
    ])
    def create(self):
        """
        {
            "short_name": "App Scope Name",
            "short_query": {"type":"eq",
                "field":"ip",
                "value": <....>
            },
            "parent_app_scope_id": <parent_app_scope_id>
        }
        """
        restclient = self.app.tetpyclient
        data = {}
        query_check = json.loads(self.app.pargs.query)

        if query_check['type'] is None or query_check['field'] is None or query_check['value'] is None:
            query_tmplate = '{ "type": "eq", "field": "ip", "value": <...> }'
            self.app.log.error('Incorrect query: as example {0}'.format(query_tmplate))
            
        else:
            data = {
                'short_name': self.app.pargs.name,
                'short_query': query_check,
                'parent_app_scope_id': self.app.pargs.parent
            }

        response = restclient.post('/app_scopes', json_body=json.dumps(data))
        self.app.log.debug('Response {0}: {1}'.format(response.status_code, 
                                                    response.content.decode("utf-8")))

        ret_content = json.loads(response.content.decode('utf-8'))
        
        if response.status_code > 299:
            self.app.log.error('{0} - {1}'.format(ret_content['status'], ret_content['error']))
        else:
            self.app.log.info('Scope {} created successfully'.format(ret_content['name']))
    
    @ex(help='delete scope', arguments=[
        (['-scope'], 
            {'help': 'Scope ID to Remove', 'action': 'store', 'dest': 'scope_id'})
    ])
    def delete(self):
        """
        DELETE /openapi/v1/app_scopes/{app_scope_id}
        """
        restclient = self.app.tetpyclient
        data = {
            'scope_id': self.app.pargs.scope_id
        }
        response = restclient.delete('/app_scopes/{0}'.format(data['scope_id']))
        self.app.log.debug('Response {0}: {1}'.format(response.status_code, 
                                                    response.content.decode("utf-8")))
        if response.status_code == 422:
            error_details = json.loads(response.content.decode("utf-8"))
            error_message = '{0} \nDetails:\n'.format(error_details['error'])
            
            for detail in error_details['details']:
                error_message += '> {0} \n> Dependencies:\n'.format(detail['error'])
                for dependency in detail['dependents']:
                    error_message += '>> {0} {1}'.format(dependency['id'], dependency['name'])
                    
            self.app.log.error(error_message)
        else:
            self.app.log.info('Scope {0} successfully deleted'.format(data['scope_id']))

    @ex(help='update')
    def update(self):
        self.app.log.error('FEATURE NOT IMPLEMENTED YET, OPEN A ISSUE')