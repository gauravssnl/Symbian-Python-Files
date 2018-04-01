"""Series 60 interface for launching Web browsers."""
# Note - when prompted by the python installer, select "Python Lib Module"
#
# GPL Licensed
#
# Nick Burch - v0.03 (14/03/2006)

import os
import e32

# Where to find apprun
apprun = 'z:\\system\\programs\\apprun.exe'
# Drives to check
drives = [ 'c:', 'z:' ]
# Where the browsers live
browsers = {}
browsers['nokia'] = '\\System\\Apps\\Browser\\Browser.app'
browsers['opera'] = '\\System\\Apps\\Opera\\Opera.app'
# What order to look for browsers in
search_order = [ 'nokia', 'opera' ]

def _find_browser_and_path():
	"""Finds the path to a browser"""
	for browser in search_order:
		for drive in drives:
			path = drive + browsers[browser]
			if os.path.exists(path):
				return (browser,path)
	raise RuntimeError('No Web Browser Found')

def open(url):
	"""Opens the webbrowser to the supplied URL"""
	(browser,path) = _find_browser_and_path()
	apprun_arg = path + ' "' + url + '"'
	print "Starting '%s'" % apprun_arg
	e32.start_exe(apprun,apprun_arg, 1)

def open_new(url):
	"""Opens the webbrowser to the supplied URL, and returns straight away"""
	(browser,path) = _find_browser_and_path()
	e32.start_exe(apprun,path + ' ' + url)

def which_browser():
	"""Returns the name of the browser that will be used to open URLs"""
	(browser,path) = _find_browser_and_path()
	return browser
