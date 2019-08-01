import sys 
from ansible.module_utils._text import to_text
from ansible.plugins.callback import CallbackBase
class CallbackModule(CallbackBase):
    """
    This callback module tells you how long your plays ran for.
    """
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'stdout'
    CALLBACK_NAME = 'callback_onfail'

    def __init__(self):

        # make sure the expected objects are present, calling the base's __init__
        super(CallbackModule, self).__init__()


        # this is only event we care about for display, when the play shows its summary stats; the rest are ignored by the base class
    def v2_runner_on_failed(self, result, ignore_errors=False):
        host = result._host.get_name()
        task = result._task.get_name()
        failed = result._result.get("failed")
        # sys.stdout.write(result)
        #self._display.display(to_text(task))
        self._display.display("%s | FAILED! => %s \nTASK NAME: '%s'" % (host, self._dump_results(result._result, indent=4), task))