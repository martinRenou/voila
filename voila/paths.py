#############################################################################
# Copyright (c) 2018, Voila Contributors                                    #
#                                                                           #
# Distributed under the terms of the BSD 3-Clause License.                  #
#                                                                           #
# The full license is in the file LICENSE, distributed with this software.  #
#############################################################################

import os
import json

from jupyter_core.paths import jupyter_path


ROOT = os.path.dirname(__file__)
STATIC_ROOT = os.path.join(ROOT, 'static')
# if the directory above us contains the following paths, it means we are installed in dev mode (pip install -e .)
DEV_MODE = os.path.exists(os.path.join(ROOT, '../setup.py')) and os.path.exists(os.path.join(ROOT, '../share'))

notebook_path_regex = r'(.*\.ipynb)'


def collect_paths(app_names, template_name='default', subdir=None, include_root_paths=True, prune=True, root_dirs=None):
    """
    Voila supports custom templates for rendering notebooks.
    For a specified template name, `collect_paths` can be used to collects
        - template paths
        - resources paths (by using the subdir arg)

    by looking in the standard Jupyter data directories:
    $PREFIX/share/jupyter/templates/<app_name>/<template_name>[/subdir]
    with different prefix values (user directory, sys prefix, and then system prefix) which
    allows users to override templates locally.
    The function will recursively load the base templates upon which the specified template
    may be based.
    """
    # We look at the usual jupyter locations, and for development purposes also
    # relative to the package directory (first entry, meaning with highest precedence)
    if root_dirs is None:
        root_dirs = []
        if DEV_MODE:
            root_dirs.append(os.path.abspath(os.path.join(ROOT, '..', 'share', 'jupyter', 'templates')))
        root_dirs.extend(jupyter_path('templates'))

    found_at_least_one = False
    paths = []
    full_paths = []  # only used for error reporting

    for root_dir in root_dirs:
        if include_root_paths:
            # we include root_dir for when we want to be very explicit, e.g.
            # {% extends 'nbconvert/classic/base.html' %}
            paths.append(root_dir)
        for app_name in app_names:
            app_dir = os.path.join(root_dir, app_name)
            if include_root_paths:
                # we include app_dir for when we want to be explicit, but less than root_dir, e.g.
                # {% extends 'classic/base.html' %}
                paths.append(app_dir)
            full_paths.append(app_dir)

            template_dir = os.path.join(app_dir, template_name)
            if os.path.exists(template_dir):
                # if we are intested in a subdirectory instead
                if subdir:
                    paths.append(os.path.join(template_dir, subdir))
                else:
                    paths.append(template_dir)

                found_at_least_one = True
                conf_file = os.path.join(template_dir, 'conf.json')
                if os.path.exists(conf_file):
                    with open(conf_file) as f:
                        conf = json.load(f)
                else:
                    conf = {}

                # For templates that are not named 'default', we assume the default base_template is 'default'
                # that means that even the default template could have a base_template when explicitly given.
                if template_name != 'default' or 'base_template' in conf:
                    new_template_name = conf.get('base_template', 'default')
                    # recursively call, but not include the root_path to avoid duplicate paths
                    base_paths = collect_paths(
                        app_names,
                        template_name=new_template_name,
                        subdir=subdir,
                        include_root_paths=False,
                        root_dirs=root_dirs,
                    )
                    paths.extend(base_paths)

    if not found_at_least_one:
        paths = "\n\t".join(full_paths)
        raise ValueError(
            'No template sub-directory with name %r found in the following paths:\n\t%s' % (template_name, paths)
        )
    return paths
