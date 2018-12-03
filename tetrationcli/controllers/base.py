
from cement import Controller, ex
from cement.utils.version import get_version_banner
from ..core.version import get_version
import os, errno, json

VERSION_BANNER = """
Application to query Tetration Analytics from the command line %s
%s
""" % (get_version(), get_version_banner())


class Base(Controller):
    class Meta:
        label = 'base'

        # text displayed at the top of --help output
        description = 'Tetration Analytics CLI tool'

        # text displayed at the bottom of --help output
        epilog = 'Usage: tetrationcli command'

        # controller level arguments. ex: 'tetrationcli --version'
        arguments = [
            ### add a version banner
            ( [ '-v', '--version' ],
              { 'action'  : 'version',
                'version' : VERSION_BANNER } ),
        ]


    def _default(self):
        """Default action if no sub-command is passed."""

        self.app.args.print_help()

    @ex(help='Application setup')
    def setup(self):
        tet_cluster = input('Tetration Analytics cluster (eg: https://great.example.com/): ')
        tet_user = input('Tetration User Credentials: ')
        tet_pass = input('Tetration Password Credentials: ')

        self.app.log.debug('{0} - {1} - {2}'.format(tet_cluster, tet_user, tet_pass))

        if "https://" not in tet_cluster:
            self.app.log.error('Wrong cluster address to connect.')

        self.app.log.debug('Generating the configuration file')
        
        config_location = '~/.config/tetrationcli/'
        config_file = 'tetrationcli.conf'
        credentials_file = 'api_credentials.json'

        # Create the folder location
        if not os.path.exists(config_location):
            os.makedirs(config_location)

        # Create the configuration file
        with open(config_location+config_file, 'w') as config:
            config.write('[tetrationcli]')
            config.write('api_endpoint = %s' % tet_cluster)
            config.write('api_credentials = %s' % config_location+credentials_file)
            config.close()
        
        with open(config_location+credentials_file, 'w') as credentials:
            json_credentials = {
                'api_key': tet_user,
                'api_secret': tet_pass
            }
            credentials.write(json.dumps(json.loads(json_credentials)))
            credentials.close()
    
