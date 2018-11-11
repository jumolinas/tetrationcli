
from tetrationcli.main import TetrationCLITest

def test_tetrationcli(tmp):
    with TetrationCLITest() as app:
        res = app.run()
        print(res)
        raise Exception

def test_command1(tmp):
    argv = ['command1']
    with TetrationCLITest(argv=argv) as app:
        app.run()
