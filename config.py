import locale
import os
import sys

DEBUG = True
WTF_CSRF_ENABLED = True
SECRET_KEY = 'this_is_my_secret_key'


# Log directory to store command outputs
COMMAND_OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(os.path.normcase(__file__))), 'output')

print(sys.stdout.encoding)
print(sys.stdout.isatty())
print(locale.getpreferredencoding())
print(sys.getfilesystemencoding())
print(os.environ["PYTHONIOENCODING"])
print(chr(246), chr(9786), chr(9787))
