#!/usr/bin/env python
# note: addr after call of strncpy is 400657
# and addr after call of strstr is 40063B

import nose
import logging
l = logging.getLogger("angr_tests")

try:
    # pylint: disable=W0611,F0401
    import standard_logging
    import angr_debug
except ImportError:
    pass

import angr

# load the tests
import os
test_location = str(os.path.dirname(os.path.realpath(__file__)))
strstr_and_strncpy_amd64 = None

def setup_module():
    setup_amd64()

def setup_amd64():
    global strstr_and_strncpy_amd64
    strstr_and_strncpy_amd64 = angr.Project(test_location + "blob/x86_64/strstr_and_strncpy", load_libs=True, default_analysis_mode='symbolic', use_sim_procedures=True, exclude_sim_procedures=['strncpy','strstr'])

def test_amd64():
    explorer = angr.surveyors.Explorer(strstr_and_strncpy_amd64, max_repeats=50, find=[0x400657]).run()
    s = explorer.found[0].last_run.initial_state
    result = s.mem_value(s.reg_value(16), 15).any_str()
    nose.tools.assert_equals(result, 'hi th hi there\x00')

if __name__ == "__main__":
    setup_amd64()
    test_amd64()