from cement import Controller, ex
import json

class Policies(Controller):
    """
    This endpoint returns a list of policies for a particular application. This API is available to API keys with app_policy_management capability.
    """
    
    class Meta:
        label = 'policies'
        stacked_type = 'nested'

    @ex(help='List the policies from given application', arguments=[
        (['application'],
        {'help': 'Application ID to request policies', 'action': 'store', 'dest': 'application_id'}),
        (['-default'],
        {'help': 'Show the default policies', 'action': 'store_true', 'dest': 'default'}),
        (['-absolute'],
        {'help': 'Show the absolute policies', 'action': 'store_true', 'dest': 'absolute'}),
        (['-catch_all'],
        {'help': 'Show the catch_all policies', 'action': 'store_true', 'dest': 'catch_all'}),
    ])
    def list(self):
        """
        TODO: Finish implementing Policies List
        GET /openapi/v1/applications/:application_id/policies
        GET /openapi/v1/applications/:application_id/default_policies
        GET /openapi/v1/applications/:application_id/absolute_policies
        GET /openapi/v1/applications/:application_id/catch_all
        """
        application_id = self.app.pargs.application_id
        restclient = self.app.tetpyclient

        if self.app.pargs.default:
            response = restclient.get('/applications/{0}/default_policies'.format(application_id))
        elif self.app.pargs.absolute:
            response = restclient.get('/applications/{0}/absolute_policies'.format(application_id))
        elif self.app.pargs.catch_all:
            response = restclient.get('/applications/{0}/catch_all'.format(application_id))
        else:
            response = restclient.get('/applications/{0}/policies'.format(application_id))

        self.app.log.debug('{0} - {1}'.format(response.status_code, response.content.decode('utf-8')))

        data= {
            'results' = response.content.decode('utf-8')
        }

        self.app.render(data, 'policies_list.jinja2')
        self.app.log.error('FEATURE NOT IMPLEMENTED YET, OPEN A ISSUE')

        @ex(help='Returns instance policy',arguments=[
            (['policy_id'],
            {'help': 'Policy ID to return', 'action': 'store', 'dest': 'policy_id'}),
        ])
        def policy(self):
            """
            TODO: Finish implement policy
            GET /openapi/v1/policies/:policy_id
            """
            policy_id = self.app.pargs.policy_id
            restclient = self.app.tetpyclient

            response = restclient.get('/policies/{0}'.format(policy_id))
            self.app.log.debug('{0} - {1}'.format(response.status_code, response.content.decode('utf-8')))

            data = {
                'results', response.content.decode('utf-8')
            }
            
            self.app.render(data, 'policy_details.jinja2')
            self.app.log.error('FEATURE NOT IMPLEMENTED YET, OPEN A ISSUE')
        
        # @ex(help='create new policy', arguments=[
        #     ()
        # ])
        # def create(self):
        #     """
        #     {
        #         "version": "v1",
        #         "rank" : "DEFAULT",
        #         "policy_action" : "ALLOW",
        #         "priority" : 100,
        #         "consumer_filter_id" : "123456789",
        #         "provider_filter_id" : "987654321",
        #     }
        #     """
        #     self.app.log.error('FEATURE NOT IMPLEMENTED YET, OPEN A ISSUE')


