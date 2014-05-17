# GTK+ 3 Dark Window Theme Variant Setter Plugin for Sublime Text 2/3
#
# Copyright (C) 2014 Philipp Emanuel Weidmann <pew@worldwidemann.com>
#
# Nemo vir est qui mundum non reddat meliorem.
#
# Released under the terms of the MIT License (http://opensource.org/licenses/MIT)

import sublime, sublime_plugin
import subprocess
import re

class GTKDarkThemeVariantSetter(sublime_plugin.EventListener):
	def get_output_matches(self, arguments, pattern):
		# The superior subprocess.check_output was introduced in Python 2.7
		# and thus is not supported by Sublime Text 2
		output = subprocess.Popen(arguments, stdout=subprocess.PIPE).communicate()[0]
		return re.findall(pattern, output.decode("utf-8"))

	def get_sublime_pids(self):
		# This relies on Sublime Text's program name being either "sublime" or "sublime_text".
		# Edit the parameters if the name is different on your system
		return self.get_output_matches(["pidof", "sublime", "sublime_text"], "\d+")

	def get_window_ids(self):
		return self.get_output_matches(["xprop", "-root", "_NET_CLIENT_LIST"], "0x[0-9a-f]+")

	def get_pid_from_window_id(self, window_id):
		return self.get_output_matches(["xprop", "-id", window_id, "_NET_WM_PID"], "\d+")[0]

	def set_dark_theme(self, window_id):
		subprocess.call(["xprop", "-id", window_id, "-f", "_GTK_THEME_VARIANT", "8u",
		                 "-set", "_GTK_THEME_VARIANT", "dark"])

	# Unfortunately, on_new is not sufficient for the purposes of this plugin
	# because on_new hooks are usually invoked before the window is created
	def on_activated(self, view):
		sublime_pids = self.get_sublime_pids()
		for window_id in self.get_window_ids():
			if self.get_pid_from_window_id(window_id) in sublime_pids:
				self.set_dark_theme(window_id)
