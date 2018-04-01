#
# appmgr_default.py
#
# This script implements the logic of Application Manager.
#     
# Copyright (c) 2005-2006 Nokia Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import sys
import e32
import appuifw
import os

if e32.s60_version_info>=(3,0):
    PYTHON_PATH = '\\python'
    APPMGR_PATH = 'c:\\private\\F0201512'
    LIB_PATH = '\\sys\\bin'
    APPS_PATH = '\\sys\\bin'
else:
    PYTHON_PATH = '\\system\\apps\\python'
    APPMGR_PATH = '\\system\\apps\\appmgr'
    LIB_PATH = '\\system\\libs'
    APPS_PATH = '\\system\\apps'

PYTHON_EXTS = ['.py', '.pyc', '.pyo', '.pyd']
PYTHON_LIB_EXTS = ['.pyc', '.pyo', '.pyd']

def python_drive():
    if e32.s60_version_info>=(3,0):
        return "C:"
    for drive in [str(x) for x in e32.drive_list()]:
        if os.path.isfile(os.path.join(drive, PYTHON_PATH, 'python.app')):
            return drive
    raise AssertionError, "Python not found"

def do_copy(src, dst_dir):
    dst = os.path.join(dst_dir, os.path.split(src)[1])
    if not os.path.isdir(dst_dir):
        os.mkdir(dst_dir)
    e32.file_copy(unicode(dst), unicode(src))

def script_install(filename):
    do_copy(filename, os.path.join(python_drive(), PYTHON_PATH, 'my'))

def lib_install(filename):
    file_root = os.path.splitext(os.path.split(filename)[1])[0]
    matching_lib_names = [file_root+x for x in PYTHON_EXTS]
    for p in sys.path[1:]:
        for n in matching_lib_names:
            matching_name = os.path.join(p, n)
            if os.path.exists(matching_name):
                if appuifw.query(u'Replace existing\n'+unicode(n),'query'):
                    os.remove(matching_name)
                else:
                    return
    do_copy(filename, os.path.join(python_drive(), LIB_PATH))

def standalone_install(filename):
    def reverse(L):
        L.reverse()
        return L
    def atoi(s):
        # Little-endian conversion from a 4-char string to an int.
        sum = 0L
        for x in reverse([x for x in s[0:4]]):
            sum = (sum << 8) + ord(x)
        return sum
    def itoa(x):
        # Little-endian conversion from an int to a 4-character string.
        L=[chr(x>>24), chr((x>>16)&0xff), chr((x>>8)&0xff), chr(x&0xff)]
        L.reverse()
        return ''.join(L)

    try:
        offset = int(file(os.path.join(python_drive(), APPMGR_PATH,
                                       'uid_offset_in_app')).read(), 16)
    except:
        offset = None

    app_rootname = os.path.splitext(os.path.split(filename)[1])[0]
    app_dir = os.path.join(python_drive(), APPS_PATH, app_rootname)                       

    #
    # read the UID from the script file
    #
    script = file(filename, 'r').read()
    uidpos = script.find('SYMBIANUID=')
    if uidpos == -1:
        uid_text = appuifw.query(u'Give UID', 'text', u'0xXXXXXXXX')
        if not uid_text == None:
            uid = int(uid_text, 16)
        else:
            appuifw.note(u"Installation cancelled", "info")
            return
    else:
        uidpos = uidpos+len('SYMBIANUID=')
        while uidpos+10 < len(script) and script[uidpos].isspace():
            uidpos = uidpos+1
        if uidpos == len(script):
            appuifw.note(u"UID not found", "error")
            return
        else:
            uid = int(script[uidpos:uidpos+10], 16)

    #
    # copy the script to application's directory as default.py
    #
    if not os.path.isdir(app_dir):
        os.mkdir(app_dir)
    e32.file_copy(unicode(os.path.join(app_dir, 'default.py')),
                  unicode(filename))

    #
    # copy the template .app file to application directory with proper name
    # and set the UID and checksum fields suitably
    #
    template_dotapp = file(os.path.join(python_drive(), APPMGR_PATH, 'pyapp_template.tmp'))
    dotapp_name = app_rootname + '.app'
    dotapp = file(os.path.join(app_dir, dotapp_name), 'w')
    appbuf = template_dotapp.read()
    csum = atoi(appbuf[24:28])
    crc1 = itoa(e32._uidcrc_app(uid))
    crc2 = itoa(( uid + csum ) & 0xffffffffL)
    if offset:
        temp = appbuf[0:8] + itoa(uid) + crc1 + appbuf[16:24] + crc2 +\
               appbuf[28:offset] + itoa(uid) + appbuf[(offset+4):]
    else:
        temp = appbuf[0:8] + itoa(uid) + crc1 + appbuf[16:24] + crc2 + appbuf[28:]
    dotapp.write(temp)

    #
    # copy the template .rsc file to application directory with proper name
    #
    rsc_name = app_rootname + '.rsc'
    e32.file_copy(unicode(os.path.join(app_dir, app_rootname + '.rsc')),
                  unicode(os.path.join(python_drive(), APPMGR_PATH, 'pyrsc_template.tmp')))

def exit_wait():
    appuifw.note(u"Please wait", "info")
    
def run(params):
    filename = params[1]
    appuifw.app.title = unicode(os.path.split(filename)[1])
    ext = os.path.splitext(filename)[1].lower()
    if ext in PYTHON_EXTS:
        source_path = os.path.splitdrive(filename)[1].lower()
        # It's safe to exit if we have been started from the Messaging
        # app, but not if we have been started from e.g. the web
        # browser, since then the whole browser would exit. The
        # default is to not exit the app, since that's safer.
        should_exit=source_path.startswith('\\system\\mail')
        if ext in PYTHON_LIB_EXTS:
            actions = [lambda: lib_install(filename)]
            menu = [u"Python lib module"]
        else:
            actions = [lambda: script_install(filename),
                       lambda: standalone_install(filename),
                       lambda: lib_install(filename)]
            menu = [u"Python script",
                    u"py2app",
                    u"Python lib module"]

        index = appuifw.popup_menu(menu, u"Install as")
        try:
            if not index == None:
                appuifw.app.exit_key_handler = exit_wait
                e32.ao_yield()
                actions[index]()
                appuifw.note(u"Installation complete", "info")
        finally:
            appuifw.app.exit_key_handler = None
            if should_exit:
                appuifw.app.set_exit()

if __name__ == '__main__':
    try:
        run(sys.argv)
    except:
        try:
            import logger
        except:
            appuifw.note(u"Failed", "error")
        else:
            logger.print_exception_trace('c:\\appmgr.log')
            appuifw.note(u"Failed -- see appmgr.log", "error")
