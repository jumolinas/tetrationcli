
from cement import App, TestApp, init_defaults
from cement.core.exc import CaughtSignal
from .core.exc import TetrationCLIError
from .controllers.base import Base
from .controllers.agents import Agents
from .controllers.swiches import Switches
from .controllers.scopes import Scopes
from .controllers.roles import Roles
from .controllers.users import Users
from .controllers.applications import Applications
from .controllers.vrfs import VRFs
from .controllers.inventory import Inventory



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
            'tabulate',
        ]

        # set the log handler
        log_handler = 'colorlog'

        # set the output handler
        output_handler = 'tabulate'

        # register handlers
        handlers = [
            Base,
            Agents,
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
