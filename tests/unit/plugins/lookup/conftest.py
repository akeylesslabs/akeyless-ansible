from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest


@pytest.fixture
def base_vars():
    return {
        'akeyless_api_url': 'http://myvault',
        'access_type': 'api_key',
    }
