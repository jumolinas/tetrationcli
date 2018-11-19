from cement import Controller, ex
import json

class Inventory(Controller):

    class Meta:
        label = 'inventory'
        stacked_type = 'nested'
        # stacked_on = 'agents'

    @ex(help='Create new filter',arguments=[
        (['-scope'],
            {'help': 'Application Scope ID', 'action': 'store', 'dest': 'scope'}),
        (['-name'],
            {'help': 'Filter Name', 'action': 'store', 'dest': 'name'}),
        (['-query'],
            {'help': 'Query in json format', 'action': 'store', 'dest': 'query'}),
    ])
    def create_filter(self):
        """
        Create an inventory
        {
        "app_scope_id": <app_scope_id>,
        "name": "sensor_config_inventory_filter",
        "query": {
            "type": "eq",
            "field": "ip",
            "value": <sensor_interface_ip>
        }
        """
        try:
            data = {
                'scope_id': self.app.pargs.scope,
                'filter_name': self.app.pargs.name,
                'filter_query': json.loads(self.app.pargs.query)
            }
            

            self.app.log.debug('Agent Inventory Scope: %s' % data['scope_id'])
            self.app.log.debug('Agent Inventory Filter Name: %s' % data['filter_name'])
            self.app.log.debug('Agent Inventory Filter Query: %s' % data['filter_query'])
            
            self.app.log.error('FEATURE NOT IMPLEMENTED YET, OPEN A ISSUE')

        except Exception as e:
            self.app.log.error(e)

    @ex(help='Create new profile', arguments=[
        (['-root'],
            {'help': 'Root Scope ID', 'action': 'store', 'dest': 'root_scope'}),
        (['-name'],
            {'help': 'Profile Name', 'action': 'store', 'dest': 'name'}),
        (['-dpd'],
            {'help': 'Data Plane Enabled', 'action': 'store_true', 'dest': 'data_plane_disabled'}),
        (['-epl'],
            {'help': 'Enabled PID Lookup', 'action': 'store_true', 'dest': 'enable_pid_lookup'}),
        (['-ed'],
            {'help': 'Enforcement Disabled?', 'action': 'store_true', 'dest': 'enforcement_disabled'}),
    ])
    def create_profile(self):
        """
        {
        "root_app_scope_id": <root_app_scope_id>,
        "data_plane_disabled": True,
        "name": "sensor_config_profile_1",
        "enable_pid_lookup": True,
        "enforcement_disabled": False
        }
        """
        try:
            data = {
                'root_scope_id': self.app.pargs.root_scope,
                'profile_data_plane_disabled': self.app.pargs.data_plane_disabled,
                'profile_name': self.app.pargs.name,
                'profile_enable_pid_lookup': self.app.pargs.enable_pid_lookup,
                'profile_enforcement_disabled': self.app.pargs.enforcement_disabled
            }
            

            self.app.log.debug('Agent Profile Scope: %s' % data['root_scope_id'])
            self.app.log.debug('Agent Profile Name: %s' % data['profile_name'])
            self.app.log.debug('Agent Profile Data Plane Disabled: %s' % data['profile_data_plane_disabled'])
            self.app.log.debug('Agent Profile Enabled PID Lookup: %s' % data['profile_enable_pid_lookup'])
            self.app.log.debug('Agent Profile Enforcement Disabled: %s' % data['profile_enforcement_disabled'])

            self.app.log.error('FEATURE NOT IMPLEMENTED YET, OPEN A ISSUE')

        except Exception as e:
            self.app.log.error(e)

        
    @ex(help='Create new intent', arguments=[
        (['-profile'],
            {'help': 'Profile ID', 'action': 'store', 'dest': 'profile_id'}),
        (['-filter'],
            {'help': 'Filter ID', 'action': 'store', 'dest': 'filter_id'}),
    ])
    def create_intent(self):
        """
        {
        "inventory_config_profile_id": <>,
        "inventory_filter_id": <>
        }
        """
        try:
            data = {
                'profile_id': self.app.pargs.profile_id,
                'filter_id': self.app.pargs.filter_id
            }

            self.app.log.debug('Inventory Profile ID: %s' % data['profile_id'])
            self.app.log.debug('Inventory Filter ID: %s' % data['filter_id'])
            
            self.app.log.error('FEATURE NOT IMPLEMENTED YET, OPEN A ISSUE')

        except Exception as e:
            self.app.log.error(e)

    @ex(help='Get all tags', arguments=[
        (['-scope'],
            {'help': 'Application Scope name', 'action': 'store', 'dest': 'app_scope_name'}),
        (['-ip'],
            {'help': 'IP to get the tags', 'action': 'store', 'dest': 'ip'}),
    ])
    def tags(self):
        data = {
            'tags_app_scope_name': self.app.pargs.app_scope_name,
            'tags_ip': self.app.pargs.ip     
        }
        

        self.app.log.debug('Inventory Tags: app_scope_name = %s' % data['tags_app_scope_name'])
        self.app.log.debug('Inventory Tags: ip = %s' % data['tags_ip'])

        self.app.log.error('FEATURE NOT IMPLEMENTED YET, OPEN A ISSUE')


    @ex(help='Set tags', arguments=[
        (['-scope'],
            {'help': 'Application Scope name', 'action': 'store', 'dest': 'app_scope_name'}),
        (['-ip'],
            {'help': 'IP to get the tags', 'action': 'store', 'dest': 'ip'}),
        (['-attributes'],
            {'help': 'Set the attribute tags', 'action': 'store', 'dest': 'attributes'}),
    ])
    def set_tags(self):
        """
        {
            'ip': '10.1.1.1/24',
            'attributes': 
            {
                'datacenter': 'SJC', 
                'location': 'CA'
            }
        }
        """
        data = {
            'set_tags_app_scope_name': self.app.pargs.app_scope_name,
            'set_tags_ip': self.app.pargs.ip,
            'set_tags_attributes': json.loads(self.app.pargs.attributes)
        }

        self.app.log.debug('Inventory Set Tags: app_scope_name = %s' % data['set_tags_app_scope_name'])
        self.app.log.debug('Inventory Set Tags: ip = %s' % data['set_tags_ip'])
        self.app.log.debug('Inventory Set Tags: attributes = %s' % data['set_tags_attributes'])

        self.app.log.error('FEATURE NOT IMPLEMENTED YET, OPEN A ISSUE')
