
from cement import Controller, ex
from cement.utils.version import get_version_banner
from ..core.version import get_version
from pathlib import Path
import os, errno, json, shutil

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
        tet_user = input('Tetration API Key: ')
        tet_pass = input('Tetration API Secret: ')

        self.app.log.debug('{0} - {1} - {2}'.format(tet_cluster, tet_user, tet_pass))

        if "https://" not in tet_cluster:
            self.app.log.error('Wrong cluster address to connect.')

        self.app.log.debug('Generating the configuration file')
        
        home = str(Path.home())
        config_location = home+'/.config/tetrationcli/'
        config_file = 'tetrationcli.conf'
        credentials_file = 'api_credentials.json'

        # Create the folder location
        if not os.path.exists(config_location):
            os.makedirs(config_location)

        # Create the configuration file
        with open(config_location+config_file, 'w') as config:
            config.write('[tetrationcli]\n')
            config.write('api_endpoint = {0}\n'.format(tet_cluster))
            config.write('api_credentials = {0}\n'.format(config_location+credentials_file))
            config.close()
        
        # Create the app_credentials.json file
        with open(config_location+credentials_file, 'w') as credentials:
            app_credentials = {
                'api_key': tet_user, 
                'api_secret': tet_pass
            }
            json.dump(app_credentials, credentials,indent=4, sort_keys=True)
            credentials.close()
        
        self.app.log.info('Configuration files set in {0}'.format(config_location))

    @ex(help='Clear the configuration')
    def clear(self):
        home = str(Path.home())
        config_location = home + '/.config/tetrationcli'
        delete_it = input('This operation will delete the folder {0}. Are you sure? [y/N] '
                    .format(config_location))

        if "y" in str(delete_it).lower() or "yes" in str(delete_it).lower():
            try:
                self.app.log.debug('Deleting config folder {0}'.format(config_location))
                shutil.rmtree(config_location)
                self.app.log.info('Deleted configuration')
            except FileNotFoundError:
                self.app.log.info('Configuration not present, already deleted or not setup')
        else:
            self.app.log.debug('Nothing to delete: {0}'.format(delete_it))
        

    
