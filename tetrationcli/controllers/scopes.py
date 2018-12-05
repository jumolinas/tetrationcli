from cement import ex
from .tet_controller import TetController
import json

class Scopes(TetController):
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
        help= 'Interact with Scopes configured in Tetration Cluster'

    @ex(help='list scopes', arguments=[
        # (['-columns'],
        #     {'help': 'show columns', 'action': 'store', 'dest': 'columns'})
    ])
    def list(self):
        
        response = self.tetration().get('/app_scopes')
        self.app.log.debug('{0} - {1}'.format(response.status_code,
                                                response.content.decode('utf-8')))

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
        data = {
            'scope_id': self.app.pargs.scope_id
        }
        response = self.tetration().delete('/app_scopes/{0}'.format(data['scope_id']))
        self.app.log.debug('{0} - {1}'.format(response.status_code,
                                                response.content.decode('utf-8')))
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
        scope_id = self.app.pargs.scope_id

        response = self.tetration().get('/app_scopes/{0}/policy_order'.format(scope_id))
        json_content = json.loads(response.content.decode('utf-8'))
        self.app.log.debug('{0} - {1}'.format(response.status_code,
                                                response.content.decode('utf-8')))
        
        if response.status_code > 299:
            self.app.log.error('{0} - {1}'.format(json_content['status'], json_content['error']))
        else:
            headers = ['Policy Priority', 'Scope ID', 'Name']
            data_list = [[x['policy_priority'],
                        x['id'],
                        x['name']] for x in json_content ]
            
            self.app.render(data_list, headers=headers)
