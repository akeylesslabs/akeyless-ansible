from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import json
from unittest import mock

import pytest



@pytest.fixture
def fixture_loader():
    def _loader(name, parse='json'):
        here = os.path.dirname(os.path.realpath(__file__))
        fixture = os.path.join(here, 'fixtures', name)

        if parse == 'path':
            return fixture

        with open(fixture, 'r') as f:
            if parse == 'json':
                d = json.load(f)
            elif parse == 'lines':
                d = f.readlines()
            elif parse == 'raw':
                d = f.read()
            else:
                raise ValueError("Unknown value '%s' for parse" % parse)

        return d

    return _loader


@pytest.fixture
def mock_api_client():
    mock_client = mock.Mock()
    with mock.patch('plugins.module_utils._akeyless_helper.AkeylessHelper.create_api_client', return_value=mock_client):
        yield mock_client

@pytest.fixture
def mock_create_api_client():
    with mock.patch('plugins.module_utils._akeyless_helper.AkeylessHelper.create_api_client', autospec=True) as mock_client:
        yield mock_client