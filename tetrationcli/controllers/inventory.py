from cement import Controller, ex
import json

class Inventory(Controller):

    class Meta:
        label = 'inventory'
        stacked_type = 'nested'
        # stacked_on = 'agents'

    @ex(help='Create new filter',arguments=[
        (['scope'],{'help': 'Application Scope ID', 'action': 'store'}),
        (['name'],{'help': 'Filter Name', 'action': 'store'}),
        (['query'],{'help': 'Query in json format', 'action': 'store'}),
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
            scope_id = self.app.pargs.scope
            filter_name = self.app.pargs.name
            filter_query = json.loads(self.app.pargs.query)

            self.app.log.debug('Agent Inventory Scope: %s' % scope_id)
            self.app.log.debug('Agent Inventory Filter Name: %s' % filter_name)
            self.app.log.debug('Agent Inventory Filter Query: %s' % filter_query)
        except Exception as e:
            self.app.log.error(e)

    @ex(help='Create new profile', arguments=[
        (['root_scope'],{'help': 'Root Scope ID', 'action': 'store'}),
        (['name'],{'help': 'Profile Name', 'action': 'store'}),
        (['data_plane_disabled'],{'help': 'Data Plane Enabled?', 'action': 'store'}),
        (['enable_pid_lookup'],{'help': 'Enabled PID Lookup?', 'action': 'store'}),
        (['enforcement_disabled'],{'help': 'Enforcement Disabled?', 'action': 'store'}),
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
            root_scope_id = self.app.pargs.root_scope
            profile_data_plane_disabled = self.app.pargs.data_plane_disabled
            profile_name = self.app.pargs.name
            profile_enable_pid_lookup = self.app.pargs.enable_pid_lookup
            profile_enforcement_disabled = self.app.pargs.enforcement_disabled

            self.app.log.debug('Agent Profile Scope: %s' % root_scope_id)
            self.app.log.debug('Agent Profile Name: %s' % profile_name)
            self.app.log.debug('Agent Profile Data Plane Disabled: %s' % profile_data_plane_disabled)
            self.app.log.debug('Agent Profile Enabled PID Lookup: %s' % profile_enable_pid_lookup)
            self.app.log.debug('Agent Profile Enforcement Disabled: %s' % profile_enforcement_disabled)
        except Exception as e:
            self.app.log.error(e)

        
    @ex(help='Create new intent', arguments=[
        (['profile_id'],{'help': 'Root Scope ID', 'action': 'store'}),
        (['filter_id'],{'help': 'Profile Name', 'action': 'store'}),
    ])
    def create_intent(self):
        """
        {
        "inventory_config_profile_id": <>,
        "inventory_filter_id": <>
        }
        """
        try:
            root_scope_id = self.app.pargs.root_scope
            profile_data_plane_disabled = self.app.pargs.data_plane_disabled
            profile_name = self.app.pargs.name
            profile_enable_pid_lookup = self.app.pargs.enable_pid_lookup
            profile_enforcement_disabled = self.app.pargs.enforcement_disabled

            self.app.log.debug('Agent Profile Scope: %s' % root_scope_id)
            self.app.log.debug('Agent Profile Name: %s' % profile_name)
            self.app.log.debug('Agent Profile Data Plane Disabled: %s' % profile_data_plane_disabled)
            self.app.log.debug('Agent Profile Enabled PID Lookup: %s' % profile_enable_pid_lookup)
            self.app.log.debug('Agent Profile Enforcement Disabled: %s' % profile_enforcement_disabled)
        except Exception as e:
            self.app.log.error(e)

    @ex(help='Get all tags', arguments=[
        (['app_scope_name'],{'help': 'Application Scope name', 'action': 'store'}),
        (['ip'],{'help': 'IP to get the tags', 'action': 'store'}),
    ])
    def tags(self):
        tags_app_scope_name = self.app.pargs.app_scope_name
        tags_ip = self.app.pargs.ip

        self.app.log.debug('Inventory Tags: app_scope_name = %s' % tags_app_scope_name)
        self.app.log.debug('Inventory Tags: ip = %s' % tags_ip)

    @ex(help='Set tags', arguments=[
        (['app_scope_name'],{'help': 'Application Scope name', 'action': 'store'}),
        (['ip'],{'help': 'IP to get the tags', 'action': 'store'}),
        (['attributes'],{'help': 'Set the attribute tags', 'action': 'store'}),
    ])
    def set_tags(self):
        """
        {'ip': '10.1.1.1/24', 'attributes': {'datacenter': 'SJC', 'location': 'CA'}}
        """
        set_tags_app_scope_name = self.app.pargs.app_scope_name
        set_tags_ip = self.app.pargs.ip
        set_tags_attributes = json.loads(self.app.pargs.attributes)


        self.app.log.debug('Inventory Set Tags: app_scope_name = %s' % set_tags_app_scope_name)
        self.app.log.debug('Inventory Set Tags: ip = %s' % set_tags_ip)
        self.app.log.debug('Inventory Set Tags: attributes = %s' % set_tags_attributes)


