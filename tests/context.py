'''Put the compiler/ folder on the path for the tests to see.'''

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../compiler')))