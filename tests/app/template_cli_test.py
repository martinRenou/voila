# tests programmatic config of template sytem
import pytest

import os

BASE_DIR = os.path.dirname(__file__)


@pytest.fixture
def voila_args_extra():
    path_test_template = os.path.abspath(os.path.join(BASE_DIR, '../test_template/share/jupyter/templates/voila/test_template/'))
    path_default = os.path.abspath(os.path.join(BASE_DIR, '../../share/jupyter/templates/voila/default'))
    return ['--template=None', '--VoilaTest.template_paths=[%r, %r]' % (path_test_template, path_default)]


@pytest.mark.gen_test
def test_template_test(http_client, base_url):
    response = yield http_client.fetch(base_url)
    assert response.code == 200
    assert 'test_template.css' in response.body.decode('utf-8')
