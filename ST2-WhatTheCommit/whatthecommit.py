import sublime
import sublime_plugin
import os
import urllib2


class WhatTheCommitCommand(sublime_plugin.TextCommand):
    """Random GIT commit messages from http://whatthecommit.com/"""
    def run(self, edit):
        msg = self.get_msg()

        if msg:
            foldername, filename = os.path.split(self.view.file_name())
            self.view.window().run_command('exec', {'cmd': ['git', 'commit', '-am', msg], 'working_dir': foldername})
            sublime.status_message('Commit with message: ' + msg)

    def get_msg(self):
        req = urllib2.Request('http://whatthecommit.com/index.txt')

        try:
            resp = urllib2.urlopen(req)
            return resp.read().strip()
        except:
            return False

    def is_enabled(self):
        return self.view.file_name() and len(self.view.file_name()) > 0
