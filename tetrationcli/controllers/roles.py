from cement import ex
from .tet_controller import TetController
import json

class Roles(TetController):

    class Meta:
        label = 'roles'
        stacked_type = 'nested'
        help= 'Interact with Roles in Tetration Cluster'

    @ex(help='list roles')
    def list(self):
        response = self.tetration().get('/roles')
        self.app.log.debug('{0} - {1}'.format(response.status_code,
                                                response.content.decode('utf-8')))
        
        if response.status_code == 403:
            self.app.log.error('{0}Request "user_role_scope_management" permissions'.format(response.content.decode('utf-8')))
            return
        
        data = json.loads(response.content.decode("utf-8"))
        
        headers = ['Role ID', 'Name']
        data_list = [[x['id'],
                    x['name']] for x in data ]

        self.app.render(data_list, headers=headers)

    @ex(help='delete', arguments=[
        (['-role'],
            {'help': 'Role ID to delete', 'action': 'store', 'dest': 'role_id'})
    ])
    def delete(self):
        """
        DELETE /openapi/v1/roles/{role_id}
        """
        role_id =  self.app.pargs.role_id
    
        self.app.log.debug("Deleting Role ID: %s" % role_id)
        response = self.tetration().delete('/roles/%s' % role_id)
        self.app.log.debug('{0} - {1}'.format(response.status_code,
                                                response.content.decode('utf-8')))
        
        if response.status_code == 403:
            self.app.log.error('{0}Request "user_role_scope_management" permissions'
                                    .format(response.content.decode('utf-8')))
            return
        
        if response.status_code == 204:
            self.app.log.info('Role %s deleted' % role_id)
        else:
            self.app.log.error('{0}: Role ID {1} - {2}'.format(response.status_code
                                                , role_id
                                                , response.content.decode('utf8')))
