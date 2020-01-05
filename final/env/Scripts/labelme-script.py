#!"c:\users\kmyko\desktop\computer vision\final\env\scripts\python.exe"
# EASY-INSTALL-ENTRY-SCRIPT: 'labelme==3.16.7','console_scripts','labelme'
__requires__ = 'labelme==3.16.7'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('labelme==3.16.7', 'console_scripts', 'labelme')()
    )
