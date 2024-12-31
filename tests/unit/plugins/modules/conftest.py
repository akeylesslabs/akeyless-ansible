from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from unittest.mock import patch

import pytest
from ansible.module_utils import basic

from tests.unit.plugins.modules.test_modules_utils import exit_json, fail_json


@pytest.fixture
def mock_module_helper():
    with patch.multiple(basic.AnsibleModule, exit_json=exit_json, fail_json=fail_json) as mock_helpers:
        yield mock_helpers