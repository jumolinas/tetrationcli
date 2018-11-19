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
    
    @ex(help='list applications', arguments=[
            (
                ['-all'],
                    {'help': 'Show more columns', 'action': 'store_true', 'dest': 'all'}
            )
    ])
    def list(self):
        """
        Return the list of all the applications
        """
        data = {
            'all' : self.app.pargs.all,
            'restclient_data': self.restclient('GET','/applications')
        }

        self.app.render(data, 'applications_list.jinja2')

    @ex(help='create')
    def create(self):
        """

        """
        pass
    
    @ex(help='delete')
    def remove(self):
        pass

    @ex(help='update', arguments=[
            (['-application'], 
                {'help': 'Application ID','action': 'store', 'dest': 'application_id'}),
            (['-name'], 
                {'help': 'Application Updated Name','action': 'store', 'dest': 'name'}),
            (['-description'], 
                {'help': 'Application Updated Description','action': 'store', 'dest': 'description'}),
            (['-primary'], 
                {'help': 'Application Updated Primary?','action': 'store', 'dest': 'primary'}),
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
        (['-application'], 
            {'help': 'Application ID for details', 'action': 'store', 'dest': 'application_id'})
    ],)
    def details(self):
        """
        """
        data = {
            'details_application_id': self.app.pargs.application_id
        }

        self.app.log.debug('Parameter: details_application_id = %s' % data['details_application_id'])
        data['restclient_data'] = self.restclient('GET', '/applications/%s/details' % data['details_application_id'])
        self.app.render(data, 'applications_details_list.jinja2')

    @ex(help='delete', arguments=[
        (['-application'], 
            {'help': 'Application ID to delete', 'action': 'store', 'dest': 'application_id'})
    ],)
    def delete(self):
        data = {
            'delete_application_id': self.app.pargs.application_id
        }

        self.app.log.debug('Parameter: enforce_application_id = %s' % data['delete_application_id'])
        restclient_data = self.restclient('DELETE', 
                                '/applications/%s/enable_enforce' % data['delete_application_id'])


    @ex(help='enforce', arguments=[
        (['-application'], 
            {'help': 'Application ID to enforce', 'action': 'store', 'dest': 'application_id'})
    ],)
    def enforce(self):
        data = {
            'enforce_application_id': self.app.pargs.application_id
        }

        self.app.log.debug('Parameter: enforce_application_id = %s' % data['enforce_application_id'])
        restclient_data = self.restclient('POST', 
                                    '/applications/%s/enable_enforce' % data['enforce_application_id'])
        
    @ex(help='disable', arguments=[
        (['-application'], 
            {'help': 'Application ID to disable', 'action': 'store', 'dest': 'application_id'})
    ],)
    def disable(self):
        data = {
            'disable_application_id': self.app.pargs.application_id
        }

        self.app.log.debug('Parameter: disable_application_id = %s' % data['disable_application_id'])
        restclient_data = self.restclient('POST', 
                                '/applications/%s/disable_enforce' % data['disable_application_id'])
        