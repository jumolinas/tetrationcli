
from cement import App, TestApp, init_defaults
from cement.core.exc import CaughtSignal
from .core.exc import TetrationCLIError
from .controllers.base import Base
from .controllers.agents import Agents
from .controllers.agents_inventory import Inventory
from .controllers.swiches import Switches
from .controllers.scopes import Scopes
from .controllers.roles import Roles
from .controllers.users import Users
from .controllers.applications import Applications
from .controllers.vrfs import VRFs
from .controllers.inventory import Inventory

from tetpyclient import RestClient
import urllib3

def extend_tetpyclient(app):
    app.log.info('creating tetration session')
    try:
        api_endpoint = app.config.get('tetrationcli', 'api_endpoint')
        if '<UI_VIP_OR_DNS_FOR_TETRATION_DASHBOARD>' in api_endpoint or not api_endpoint:
            raise ValueError('Tetration End Point not set: Check the config file')
        http = urllib3.PoolManager()
        http.request('GET', api_endpoint)

        api_credentials_file = app.config.get('tetrationcli', 'api_credentials')
        
        app.log.info('session to Tetration Cluster %s' % api_endpoint)

        app.extend('tetpyclient', RestClient(api_endpoint,
                                    credentials_file=api_credentials_file,
                                    verify=False))
    except Exception as e:
        app.log.error(str(e))


# configuration defaults
CONFIG = init_defaults('tetrationcli')
CONFIG['tetrationcli']['api_endpoint'] = 'https://<UI_VIP_OR_DNS_FOR_TETRATION_DASHBOARD>'
CONFIG['tetrationcli']['api_credentials'] = '~/.config/tetrationcli/api_credentials.json'

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

        # set the log handler
        log_handler = 'colorlog'

        # set the output handler
        output_handler = 'jinja2'

        # register handlers
        handlers = [
            Base,
            Agents,
            Inventory,
            Switches,
            Scopes,
            Roles,
            Users,
            Applications,
            VRFs,
            Inventory,
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
