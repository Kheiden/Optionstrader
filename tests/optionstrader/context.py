import os
import sys
#sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
print(path)
import optionstrader
