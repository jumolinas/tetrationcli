
from cement import App, TestApp, init_defaults
from cement.core.exc import CaughtSignal
from .core.exc import TetrationCLIError
from .controllers.base import Base
from .controllers.sensors import Sensors
from .controllers.swiches import Switches
from .controllers.scopes import Scopes
from .controllers.roles import Roles
from .controllers.users import Users
from .controllers.applications import Applications
from .controllers.vrfs import VRFs

import os
from cement.utils import fs
from tetpyclient import RestClient

def extend_tetpyclient(app):
    app.log.info('creating tetration session')

    api_credentials_file = app.config.get('tetrationcli', 'api_credentials')
    api_endpoint = app.config.get('tetrationcli', 'api_endpoint')

    api_credentials_file = fs.abspath(api_credentials_file)
    
    api_credentials_dir = os.path.dirname(api_credentials_file)
    if not os.path.exists(api_credentials_dir):
        app.log.error('api_credentials file not present in: %s' % api_credentials_file)
    else:
        app.log.info('api_credentials file is: %s' % api_credentials_file)

    app.log.info('session to Tetration Cluster %s' % api_endpoint)

    app.extend('tetpyclient', RestClient(api_endpoint,
                                credentials_file=api_credentials_file,
                                verify=False))


# configuration defaults
CONFIG = init_defaults('tetrationcli')
# CONFIG['tetrationcli']['api_endpoint'] = 'https://<UI_VIP_OR_DNS_FOR_TETRATION_DASHBOARD>'
CONFIG['tetrationcli']['api_endpoint'] = 'https://bdsol-ta01.cisco.com'
CONFIG['tetrationcli']['api_credentials'] = '~/.tetrationcli/api_credentials.json'

class TetrationCLI(App):
    """Tetration Command Line Interaction primary application."""

    class Meta:
        label = 'tetrationcli'

        # configuration defaults
        config_defaults = CONFIG

        # call sys.exit() on close
        close_on_exit = True

        # load additional framework extensions
        extensions = [
            'yaml',
            'colorlog',
            'jinja2',
        ]

        hooks = [
            ('post_setup', extend_tetpyclient)
        ]

        # configuration handler
        config_handler = 'yaml'

        # configuration file suffix
        config_file_suffix = '.yml'

        # set the log handler
        log_handler = 'colorlog'

        # set the output handler
        output_handler = 'jinja2'

        # register handlers
        handlers = [
            Base,
            Sensors,
            Switches,
            Scopes,
            Roles,
            Users,
            Applications,
            VRFs,
        ]


class TetrationCLITest(TestApp,TetrationCLI):
    """A sub-class of TetrationCLI that is better suited for testing."""

    class Meta:
        label = 'tetrationcli'


def main():
    with TetrationCLI() as app:
        try:
            app.run()

        except AssertionError as e:
            print('AssertionError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except TetrationCLIError:
            print('TetrationCLIError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except CaughtSignal as e:
            # Default Cement signals are SIGINT and SIGTERM, exit 0 (non-error)
            print('\n%s' % e)
            app.exit_code = 0


if __name__ == '__main__':
    main()
