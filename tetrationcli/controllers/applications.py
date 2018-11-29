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
        self.app.log.debug('command returned: %s' % response.status_code)
        self.app.log.debug('data returned: %s' % content)
        data = {
            'all' : self.app.pargs.all,
            'results': content
        }

        self.app.render(data, 'applications_list.jinja2')

    @ex(help='Create new Application from file', arguments=[
        (['-template'],
            {'help': 'Generate template to create the Application', 'action': 'store_true', 'dest': 'template'}),
        (['-file'],
            {'help': 'File to generate the Application', 'action': 'store', 'dest': 'file'}),
    ])
    # def create(self):
    #     """
    #     POST /openapi/v1/applications
    #     """
    #     if self.app.pargs.template:
    #         template = {
    #             'app_scope_id': 'The scope ID to assign to the application',
    #             'name': 'A name for the application',
    #             'description': 'A description for the application',
    #             'alternate_query_mode' : 'false',
    #             'strict_validation': 'false',
    #             'primary': 'true'
    #         }
    #         with open('template_create_application.json', 'w') as fp:
    #             json.dump(template, fp, indent=4)
    #     elif self.app.pargs.file:
    #         content = ''
    #         with open(self.app.pargs.file) as fp:
    #             content = json.loads(fp.read())
    #         self.app.log.debug('File content {0}'.format(content))
    #         restclient = self.app.tetpyclient
    #         response = restclient.post('/applications',json_body=json.dumps(content))
    #         self.app.log.debug('Response {0} Message {1}'.format(response.status_code,response.content))
    #         if response.status_code > 299:
    #             error_message = json.loads(response.text)
    #             self.app.log.error('Error {0} > {1}'.format(error_message['status'], error_message['error']))
    #         else:
    #             self.app.log.info('Application {0} Created on Scope {1}'.format(content['name'],content['app_scope_id']))

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
        self.app.log.debug('command returned: %s' % response.status_code)
        if response.status_code in [200,204]:
            self.app.log.info('Deleted Application {0}'.format(data['application_id']))
        else:
            error_message = json.loads(response.text)
            self.app.log.error('Error: {0} \n> Message {1}'.format(error_message['status'],
                                                                error_message['error']))

    # @ex(help='update', arguments=[
    #         (['-application'], 
    #             {'help': 'Application ID','action': 'store', 'dest': 'application_id'}),
    #         (['-name'], 
    #             {'help': 'Application Updated Name','action': 'store', 'dest': 'name'}),
    #         (['-description'], 
    #             {'help': 'Application Updated Description','action': 'store', 'dest': 'description'}),
    #         (['-primary'], 
    #             {'help': 'Application Updated Primary?','action': 'store', 'dest': 'primary'}),
    # ],)
    # def update(self):
    #     """
    #     TODO: applications update
    #     {
    #         "name": "Updated Name",
    #         "description": "Updated Description",
    #         "primary": "true"
    #     }
    #     """
    #     update_application_id = self.app.pargs.application_id
    #     update_application_name = self.app.pargs.name
    #     update_application_description = self.app.pargs.description
    #     update_application_primary = self.app.pargs.primary

    #     self.app.log.debug('Parameter: application_id = %s' % update_application_id)
    #     self.app.log.debug('Parameter: name = %s' % update_application_name)
    #     self.app.log.debug('Parameter: description = %s' % update_application_description)
    #     self.app.log.debug('Parameter: primary = %s' % update_application_primary)

    #     data = {
    #         "name": update_application_name,
    #         "description": update_application_description,
    #         "primary": update_application_primary
    #     }

    #     # restclient_data = self.restclient('PUT', 
    #     #                                 '/applications/%s' % update_application_id,
    #     #                                 json.dumps(req_payload))
    #     self.app.log.error('FEATURE NOT IMPLEMENTED YET, OPEN A ISSUE')


    # @ex(help='details', arguments=[
    #     (['-application'], 
    #         {'help': 'Application ID for details', 'action': 'store', 'dest': 'application_id'})
    # ],)
    # def details(self):
    #     """
    #     TODO: applications details
    #     """
    #     data = {
    #         'details_application_id': self.app.pargs.application_id
    #     }
        
    #     # self.app.log.debug('Parameter: details_application_id = %s' % data['details_application_id'])
    #     # data['restclient_data'] = self.restclient('GET', '/applications/%s/details' % data['details_application_id'])
    #     # self.app.render(data, 'applications_details_list.jinja2')
    #     self.app.log.error('FEATURE NOT IMPLEMENTED YET, OPEN A ISSUE')

    # @ex(help='enforce', arguments=[
    #     (['-application'], 
    #         {'help': 'Application ID to enforce', 'action': 'store', 'dest': 'application_id'})
    # ],)
    # def enforce(self):
    #     """
    #     TODO: applications enforce
    #     """
    #     data = {
    #         'enforce_application_id': self.app.pargs.application_id
    #     }
        
    #     self.app.log.debug('Parameter: enforce_application_id = %s' % data['enforce_application_id'])
    #     # restclient_data = self.restclient('POST', 
    #     #                             '/applications/%s/enable_enforce' % data['enforce_application_id'])
    #     self.app.log.error('FEATURE NOT IMPLEMENTED YET, OPEN A ISSUE')
        
    # @ex(help='disable', arguments=[
    #     (['-application'], 
    #         {'help': 'Application ID to disable', 'action': 'store', 'dest': 'application_id'})
    # ],)
    # def disable(self):
    #     """
    #     TODO: applications disable
    #     """
    #     data = {
    #         'disable_application_id': self.app.pargs.application_id
    #     }

    #     self.app.log.debug('Parameter: disable_application_id = %s' % data['disable_application_id'])
    #     # restclient_data = self.restclient('POST', 
    #     #                         '/applications/%s/disable_enforce' % data['disable_application_id'])
    #     self.app.log.error('FEATURE NOT IMPLEMENTED YET, OPEN A ISSUE')
        