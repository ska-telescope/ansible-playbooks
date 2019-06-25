from __future__ import absolute_import
from ansible.plugins.callback import CallbackBase
import json

class CallbackModule(CallbackBase):

    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'stdout'
    CALLBACK_NAME = 'json'

    def __init__(self):
        self.tasks = {}

    def dump_result(self, result):
        print(json.dumps(dict(name=self.tasks[result._task._uuid],result=result._result)))

    def v2_playbook_on_task_start(self, task, is_conditional):
        self.tasks[task._uuid] = task.name

    v2_runner_on_ok = dump_result
    v2_runner_on_failed = dump_result
