from cement import Controller, ex
import json

class Agents(Controller):

    class Meta:
        label = 'agents'
        stacked_type = 'nested'
        stacked_on = 'base'

    @ex(help='list agents')
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
        self.app.render(data, 'sensors_list.jinja2')
    
    @ex(help='delete', arguments=[
        (
            ['uuid'], 
            {'help': 'Delete Sensor','action': 'store'}
        )
    ],) 
    def delete(self):
        """
        /openapi/v1/sensors/{uuid}
        """
        uuid_to_delete = self.app.pargs.uuid
        self.app.log.debug("Deleting Sensor UUID: %s" % uuid_to_delete)
        restclient = self.app.tetpyclient
        response = restclient.delete('/sensors/%s' % uuid_to_delete)
        self.app.log.debug('Deleting Sensor: status_Code=%s' % response.status_code)
        self.app.log.debug('Deleting Sensor: %s' % response.content.decode("utf-8"))
