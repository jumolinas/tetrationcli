from cement import Controller, ex
import json

class Scopes(Controller):
    """
    Object 
    Attribute	        Type	Description
    id	                string  Unique identifier for the scope.
    short_name	        string	User specified name of the scope.
    name	            string	Fully qualified name of the scope. This is a fully qualified name, i.e. it has name of parent scopes (if applicable) all the way to the root scope.
    description	        string	User specified description of the scope.
    short_query	        JSON	Filter (or match criteria) associated with the scope.
    query	            JSON	Filter (or match criteria) associated with the scope in conjunction with the filters of the parent scopes (all the way to the root scope).
    vrf_id	            integer	ID of the VRF to which scope belongs to.
    parent_app_scope_id	string	ID of the parent scope.
    child_app_scope_ids	array	An array of scope children’s ids.
    policy_priority	 	        Used to sort application priorities. See Semantics and Viewing.
    dirty	            bool	Indicates a child or parent query has been updated and that the changes need to be committed.
    dirty_short_query	JSON	Non-null if the query for this scope has been updated but not yet committed.
    """
    class Meta:
        label = 'scopes'
        stacked_type = 'nested'
        # stacked_on = 'base'

    def root_scope(self, restclient, scope_id):
        response = restclient.get('/app_scopes/{0}'.format(scope_id))
        json_resp = json.loads(response.content.decode('utf-8'))
        self.app.log.debug('Getting root_scope for {0}: {1} - {2}'.format(scope_id,     
                                                                    response.status_code,
                                                                    response.content.decode('utf-8')))
        return json_resp['parent_app_scope_id']


    @ex(help='list scopes', arguments=[
        # (['-all'],
        #     {'help': 'show more columns', 'action': 'store_true', 'dest': 'all'})
        # TODO: Create option for extra columns
    ])
    def list(self):
        restclient = self.app.tetpyclient
        
        response = restclient.get('/app_scopes')
        self.app.log.debug('command returned: %s' % response.status_code)

        data = json.loads(response.content.decode("utf-8"))
        headers = ['Scope ID', 'Name', 'Parent Scope', 'VRF']
        data_list = [[x['id'],
                    x['name'],
                    x['parent_app_scope_id'],
                    x['vrf_id']] for x in data ]

        self.app.render(data_list, headers=headers)

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

    @ex(help='show policy order from scope', arguments=[
        (['-scope'], 
            {'help': 'Scope ID to Update', 'action': 'store', 'dest': 'scope_id'}),
    ])
    def policy(self):
        restclient = self.app.tetpyclient
        data = {}
        scope_id = self.app.pargs.scope_id

        response = restclient.get('/app_scopes/{0}/policy_order'.format(scope_id))
        json_content = json.loads(response.content.decode('utf-8'))
        self.app.log.debug('Response {0}: {1}'.format(response.status_code, 
                                                    response.content.decode("utf-8")))
        
        if response.status_code > 299:
            self.app.log.error('{0} - {1}'.format(json_content['status'], json_content['error']))
        else:
            headers = ['Policy Priority', 'Scope ID', 'Name']
            data_list = [[x['policy_priority'],
                        x['id'],
                        x['name']] for x in json_content ]
            
            self.app.render(data_list, headers=headers)
