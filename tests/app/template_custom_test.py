# tests programmatic config of template sytem
import pytest

import os

BASE_DIR = os.path.dirname(__file__)


@pytest.fixture
def voila_args_extra():
    return ['--template=None']


@pytest.fixture
def voila_config():
    def config(app):
        path_test_template = os.path.abspath(os.path.join(BASE_DIR, '../test_template/share/jupyter/templates/voila/test_template'))
        path_default = os.path.abspath(os.path.join(BASE_DIR, '../../share/jupyter/templates/voila/default'))
        app.template_paths = [path_test_template, path_default]

    return config


@pytest.mark.gen_test
def test_template(http_client, base_url):
    response = yield http_client.fetch(base_url)
    assert response.code == 200
    assert 'test_template.css' in response.body.decode('utf-8')
    assert 'Hi Voila' in response.body.decode('utf-8')
