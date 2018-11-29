from cement import Controller, ex
import json, time

class Agents(Controller):

    class Meta:
        label = 'agents'
        stacked_type = 'nested'
        stacked_on = 'base'

    @ex(help='list agents', arguments=[
            (['--all', '-a'], 
                {'help': 'Application ID','action': 'store_true', 'dest': 'all'}),
    ],)
    def list(self):
        """
        List all the agents registered in Tetration Appliance

        Options:
            list - Show the simple view 
                UUID | HostName | Agent Type
            list all - Show all columns 
        """
        restclient = self.app.tetpyclient
        response = restclient.get('/sensors')
        self.app.log.debug('command returned: %s' % response.status_code)
        data = {}
        data = json.loads(response.content.decode("utf-8"))
        
        self.app.log.debug('data returned: %s' % data)
        headers = ['UUID', 'Host Name', 'Agent Type', 'Last Check-in']
        data_list = [[x['uuid'],
                    x['host_name'],
                    x['agent_type'],
                    time.strftime('%Y-%m-%d %H:%M:%S', 
                        time.localtime(x['last_config_fetch_at']))]
                                            for x in data['results'] ]
        
        self.app.render(data_list, headers=headers)
    
    @ex(help='delete', arguments=[
        (
            ['-uuid'], 
                {'help': 'Delete Sensor','action': 'store', 'dest': 'uuid'}
        )
    ],) 
    def delete(self):
        """
        /openapi/v1/sensors/{uuid}
        """
        data = {
            'uuid_to_delete': self.app.pargs.uuid
        }

        self.app.log.debug("Deleting Sensor UUID: %s" % data['uuid_to_delete'])
        restclient = self.app.tetpyclient
        response = restclient.delete('/sensors/%s' % data['uuid_to_delete'])
        self.app.log.debug('Deleting Sensor: status_Code=%s' % response.status_code)
        self.app.log.debug('Deleting Sensor: %s' % response.content.decode("utf-8"))
        if response.status_code == 204:
            self.app.log.info('Sensor %s deleted' % data['uuid_to_delete'])
        else:
            self.app.log.error('{0}: Sensor ID {1} - {2}'.format(response.status_code
                                                , data['uuid_to_delete']
                                                , response.content.decode('utf8')))
