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
        (['-description'],
            {'help': 'Description of the scope', 'action': 'store', 'dest': 'description'}),
        (['-query'],
            {'help': 'Query in JSON format', 'action': 'store', 'dest': 'query'}),
        (['-parent'],
            {'help': 'Parent Scope ID', 'action': 'store', 'dest': 'parent'}),
        (['-priority'],
            {'help': 'Policy Priority number', 'action': 'store', 'dest': 'priority'}),
    ])
    # def create(self):
    #     """
    #     {
    #         "short_name": "App Scope Name",
    #         "short_query": {"type":"eq",
    #             "field":"ip",
    #             "value": <....>
    #         },
    #         "parent_app_scope_id": <parent_app_scope_id>
    #     }
    #     """
    #     restclient = self.app.tetpyclient
    #     data = {}
    #     query_check = json.loads(self.app.pargs.query)

    #     if query_check['type'] is None or query_check['field'] is None or query_check['value'] is None:
    #         query_tmplate = '{ "type": "eq", "field": "ip", "value": <...> }'
    #         self.app.log.error('Incorrect query: as example {0}'.format(query_tmplate))            
    #     else:
    #         data = {
    #             'short_name': self.app.pargs.name,
    #             'short_query': query_check,
    #             'parent_app_scope_id': self.app.pargs.parent
    #         }

    #     if self.app.pargs.description:
    #         data['description'] = self.app.pargs.description
    #     if self.app.pargs.priority:
    #         data['priority'] = self.app.pargs.priority

    #     response = restclient.post('/app_scopes', json_body=json.dumps(data))
    #     self.app.log.debug('Response {0}: {1}'.format(response.status_code, 
    #                                                 response.content.decode("utf-8")))

    #     ret_content = json.loads(response.content.decode('utf-8'))
        
    #     if response.status_code > 299:
    #         self.app.log.error('{0} - {1}'.format(ret_content['status'], ret_content['error']))
    #     else:
    #         self.app.log.info('Scope {} created successfully'.format(ret_content['name']))
    
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

    # @ex(help='update', arguments=[
    #     (['-scope'], 
    #         {'help': 'Scope ID to Update', 'action': 'store', 'dest': 'scope_id'}),
    #     (['-name'],
    #         {'help': 'Name of the scope', 'action': 'store', 'dest': 'name'}),
    #     (['-description'],
    #         {'help': 'Description of the scope', 'action': 'store', 'dest': 'description'}),
    #     (['-query'],
    #         {'help': 'Query in JSON format', 'action': 'store', 'dest': 'query'}),
    # ])
    # def update(self):
    #     """
    #     {
    #         "short_name": "App Scope Name",
    #         "short_query": {"type":"eq",
    #             "field":"ip",
    #             "value": <....>
    #         },
    #         "parent_app_scope_id": <parent_app_scope_id>
    #     }
    #     """
    #     restclient = self.app.tetpyclient
    #     data = {}
    #     dirty_query = False
    #     scope_id = self.app.pargs.scope_id
    #     if self.app.pargs.name:
    #         data['short_name'] = self.app.pargs.name
    #     if self.app.pargs.description:
    #         data['description'] = self.app.pargs.description
        
    #     if self.app.pargs.query:
    #         query_check = json.loads(self.app.pargs.query)
    #         if query_check['type'] is None or query_check['field'] is None or query_check['value'] is None:
    #             query_tmplate = '{ "type": "eq", "field": "ip", "value": <...> }'
    #             self.app.log.error('Incorrect query: as example {0}'.format(query_tmplate)) 
    #         else:
    #             data['short_query'] = query_check
    #             dirty_query = True


    #     response = restclient.put('/app_scopes/{0}'.format(scope_id), json_body=json.dumps(data))
    #     self.app.log.debug('Response {0}: {1}'.format(response.status_code, 
    #                                                 response.content.decode("utf-8")))

    #     ret_content = json.loads(response.content.decode('utf-8'))
        
    #     if response.status_code > 299:
    #         self.app.log.error('{0} - {1}'.format(ret_content['status'], ret_content['error']))
    #     else:
    #         self.app.log.info('Scope {} updated successfully'.format(ret_content['name']))
        
    #     if dirty_query:
    #         root_scope = self.root_scope(restclient, scope_id)
    #         self.app.log.info('Dirty update detected, committing scope query changes')
    #         resp_commit = restclient.post('/app_scopes/commit_dirty?root_app_scope_id={0}'.format(root_scope))
    #         self.app.log.debug('Response {0}: {1}'.format(resp_commit.status_code, 
    #                                                 resp_commit.content.decode("utf-8")))
    #         if resp_commit.status_code < 299:
    #             self.app.log.info('Scope {0} successfully commited'.format(ret_content['name']))
        
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
            data['results'] = json_content
            self.app.render(data, 'scopes_policy_order.jinja2')
