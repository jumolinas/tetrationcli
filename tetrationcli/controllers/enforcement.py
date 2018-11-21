from cement import Controller, ex
import json

class Enforcement(Controller):
    
    class Meta:
        label = 'enforcement'
        stacked_type = 'nested'
    
    @ex(help='list enforcement for agent', arguments=[
        (['-aid'],
            {'help': 'Agent UUID', 'action': 'store', 'dest': 'agent_uuid'}),
    ])
    def list(self):
        """
        GET /openapi/v1/enforcement/agents/{aid}/network_policy_config
        """
        agent_uuid = self.app.pargs.agent_uuid
        restclient = self.app.tetpyclient
        response = restclient.get('/enforcement/agents/{0}/network_policy_config'.format(agent_uuid))

        self.app.log.debug('{0} {1}'.format(response.status_code, response.content))
        data = json.loads(response.content.decode('utf-8'))
        

        self.app.render(data, 'enforcement_list.jinja2')

    @ex(help='Policy Statistics', arguments=[
        (['-aid'],
            {'help': 'Application id', 'action': 'store', 'dest': 'agent_uuid'}),
        (['-cid'],
            {'help': 'Concrete Policy UUID', 'action': 'store', 'dest': 'policy_uuid'}),
        (['-start'],
            {'help': 'Start time for statistics in epoch time', 'action': 'store', 'dest': 'start'}),
        (['-end'],
            {'help': 'End time for statistics in epoch time', 'action': 'store', 'dest': 'end'}),
        (['-aggregate'],
            {'help': 'An integer specifies number of seconds. Strings may be passed such as “minute”, “hour”, and “day”.',
            'action': 'store', 'dest': 'aggregate'})
    ])
    def statistics(self):
        """
        GET /openapi/v1/enforcement/agents/{aid}/concrete_policies/{cid}/stats?t0=<t0>&t1=<t1>&td=<td>
        """
        agent_uuid = self.app.pargs.agent_uuid
        policy_uuid = self.app.pargs.policy_uuid
        stats_start = self.app.pargs.start
        stats_end = self.app.pargs.end
        stats_agg = self.app.pargs.aggregate

        self.app.log.debug('Agent ID={0}, Policy ID={1}, Start={2}, End={3}, Aggregate={4}'
                            .format(agent_uuid, policy_uuid, stats_start, stats_end, stats_agg))
        
        restclient = self.app.tetpyclient
        response = restclient.get('/enforcement/agents/{0}/concrete_policies/{1}/stats?t0={2}&t1={3}&td={4}'
                            .format(agent_uuid, policy_uuid, stats_start, stats_end, stats_agg))

        self.app.log.debug('{0} {1}'.format(response.status_code, response.content.decode('utf-8')))
        data = {
            'results': response.content.decode('utf-8'),
        }
        
        self.app.render(data,'enforcement_stats.jinja2')
        self.app.log.error('FEATURE NOT IMPLEMENTED YET, OPEN A ISSUE')


