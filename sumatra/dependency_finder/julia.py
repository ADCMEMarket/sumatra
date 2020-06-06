"""


:copyright: Copyright 2006-2015 by the Sumatra team, see doc/authors.txt
:license: BSD 2-clause, see LICENSE for details.
"""
from __future__ import unicode_literals

import os
import re
import subprocess
from sumatra.dependency_finder import core


class Dependency(core.BaseDependency):
    """
    Contains information about a Matlab toolbox.
    """
    module = 'julia'
    
    def __init__(self, module_name, path, version='unknown', diff='', source=None):
        super(Dependency, self).__init__(module_name, path, version, diff, source)


def find_dependencies_julia(file):
    s = set([])
    def helper(file):
        if file in s:
            return 
        s.add(file)
        with open(file, 'r') as io:
            cnt = io.read()
            files = re.findall('include\("(.*?)"\)', cnt)
            for f in files:
                f = os.path.abspath(f)
                helper(f)
    helper(os.path.abspath(file))
    ret = list(s)
    return ret 


def find_dependencies(filename, executable):
    dep_files = find_dependencies_julia(filename)
    list_deps = []
    for path in dep_files:
        if os.name == 'posix':
            list_data = path.split('/')
        else:
            list_data = path.split('\\')
        list_deps.append(Dependency(list_data[-2], path.split('\n')[0]))
    list_deps = core.find_versions(list_deps, [core.find_versions_from_versioncontrol])
    return list_deps
