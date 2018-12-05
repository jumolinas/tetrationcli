from cement import ex
from .tet_controller import TetController
import json, time

class Agents(TetController):

    class Meta:
        label = 'agents'
        stacked_type = 'nested'
        stacked_on = 'base'
        help= 'Interact with Software Sensors in Tetration Cluster'

    @ex(help='list agents', arguments=[
            (['-columns'],
                {'help': 'Show more columns','action': 'store', 'dest': 'columns'}),
    ],)
    def list(self):
        """
        List all the agents registered in Tetration Appliance

        Options:
            list - Show the simple view
                UUID | HostName | Agent Type
            list all - Show all columns
        """
        columns = self.app.pargs.columns
        response = self.tetration().get('/sensors')
        self.app.log.debug('{0} - {1}'.format(response.status_code,
                                                response.content.decode('utf-8')))

        data = json.loads(response.content.decode("utf-8"))

        self.app.log.debug('data returned: %s' % data)

        if columns:
            headers = []
            data_list = []
        else:
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
        uuid =  self.app.pargs.uuid

        self.app.log.debug("Deleting Sensor UUID: %s" % uuid)
        response = self.tetration().delete('/sensors/%s' % uuid)
        self.app.log.debug('{0} - {1}'.format(response.status_code,
                                                response.content.decode('utf-8')))
        if response.status_code == 204:
            self.app.log.info('Sensor %s deleted' % uuid)
        else:
            self.app.log.error('{0}: Sensor ID {1} - {2}'.format(response.status_code
                                                , uuid
                                                , response.content.decode('utf8')))
