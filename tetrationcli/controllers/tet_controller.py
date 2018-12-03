from cement import Controller, ex
from tetpyclient import RestClient
import urllib3

class TetController(Controller):
    
    def tetration(self):
        self.app.log.info('Creating Tetration Session')
        try:
            api_endpoint = self.app.config.get('tetrationcli', 'api_endpoint')
            if '<UI_VIP_OR_DNS_FOR_TETRATION_DASHBOARD>' in api_endpoint or not api_endpoint:
                raise ValueError('Tetration End Point not set: Check the config file')
            http = urllib3.PoolManager()
            http.request('GET', api_endpoint)

            api_credentials_file = self.app.config.get('tetrationcli', 'api_credentials')
            
            self.app.log.info('session to Tetration Cluster %s established' % api_endpoint)

            return RestClient(api_endpoint,
                                credentials_file=api_credentials_file,
                                verify=False)
        except Exception as e:
            self.app.log.error(str(e))