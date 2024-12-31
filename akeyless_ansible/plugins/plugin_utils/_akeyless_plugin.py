from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible.plugins import AnsiblePlugin
from ansible.utils.display import Display


display = Display()


class AkeylessPlugin(AnsiblePlugin):

    def __init__(self):
        super(AkeylessPlugin, self).__init__()

    def warn(self, msg: str):
        display.warning(msg)

    def debug(self, msg: str):
        display.debug(msg)