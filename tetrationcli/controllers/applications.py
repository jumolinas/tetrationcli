from cement import Controller, ex
import json

class Applications(Controller):
    
    class Meta:
        label = 'applications'
        stacked_type = 'nested'
        # stacked_on = 'base'

    def restclient(self, http, query, json_value=None):
        restclient = self.app.tetpyclient
        if http in 'GET':
            response = restclient.get(query)
        if http in 'POST':
            response = restclient.post(query)
        if http in 'DELETE':
            response = restclient.delete(query)
        if http in 'PUT':
            response = restclient.put(query,json_body=json_value)
        else:
            response = None
        self.app.log.debug('command returned: %s' % response.status_code)
        data = {}
        data['results'] = json.loads(response.content.decode("utf-8"))
        self.app.log.debug('data returned: %s' % data)
        return data
    
    @ex(help='list applications')
    def list(self):
        """
        Return the list of all the applications
        TODO: Optional parameter to send back only one application
        """
        restclient_data = self.restclient('GET','/applications')
        self.app.render(restclient_data, 'applications_list.jinja2')

    @ex(help='create')
    def create(self):
        """

        """
        pass
    
    @ex(help='delete')
    def remove(self):
        pass

    @ex(help='update', arguments=[
            (['application_id'], {'help': 'Application ID','action': 'store'}),
            (['name'], {'help': 'Application Updated Name','action': 'store'}),
            (['description'], {'help': 'Application Updated Description','action': 'store'}),
            (['primary'], {'help': 'Application Updated Primary?','action': 'store'}),
    ],)
    def update(self):
        """
        {
            "name": "Updated Name",
            "description": "Updated Description",
            "primary": "true"
        }
        """
        update_application_id = self.app.pargs.application_id
        update_application_name = self.app.pargs.name
        update_application_description = self.app.pargs.description
        update_application_primary = self.app.pargs.primary

        self.app.log.debug('Parameter: application_id = %s' % update_application_id)
        self.app.log.debug('Parameter: name = %s' % update_application_name)
        self.app.log.debug('Parameter: description = %s' % update_application_description)
        self.app.log.debug('Parameter: primary = %s' % update_application_primary)

        req_payload = {
            "name": update_application_name,
            "description": update_application_description,
            "primary": update_application_primary
        }

        restclient_data = self.restclient('PUT', 
                                        '/applications/%s' % update_application_id,
                                        json.dumps(req_payload))


    @ex(help='details', arguments=[
        (['application_id'], {'help': 'Application ID for details', 'action': 'store'})
    ],)
    def details(self):
        """
        """
        details_application_id = self.app.pargs.application_id

        self.app.log.debug('Parameter: details_application_id = %s' % details_application_id)
        restclient_data = self.restclient('GET', '/applications/%s/details' % details_application_id)
        self.app.render(restclient_data, 'applications_details_list.jinja2')

    @ex(help='delete', arguments=[
        (['application_id'], {'help': 'Application ID to delete', 'action': 'store'})
    ],)
    def delete(self):
        delete_application_id = self.app.pargs.application_id

        self.app.log.debug('Parameter: enforce_application_id = %s' % delete_application_id)
        restclient_data = self.restclient('DELETE', 
                                '/applications/%s/enable_enforce' % delete_application_id)


    @ex(help='enforce', arguments=[
        (['application_id'], {'help': 'Application ID to enforce', 'action': 'store'})
    ],)
    def enforce(self):
        enforce_application_id = self.app.pargs.application_id

        self.app.log.debug('Parameter: enforce_application_id = %s' % enforce_application_id)
        restclient_data = self.restclient('POST', 
                                    '/applications/%s/enable_enforce' % enforce_application_id)
        
    @ex(help='disable', arguments=[
        (['application_id'], {'help': 'Application ID to disable', 'action': 'store'})
    ],)
    def disable(self):
        disable_application_id = self.app.pargs.application_id

        self.app.log.debug('Parameter: disable_application_id = %s' % disable_application_id)
        restclient_data = self.restclient('POST', 
                                '/applications/%s/disable_enforce' % disable_application_id)
        