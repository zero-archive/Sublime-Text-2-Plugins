import sublime
import sublime_plugin
import time
import htmlentitydefs
import re
import base64
from cgi import escape
from hashlib import md5
from dateutil.parser import parse
from datetime import datetime


class ConvertCharsToHtmlCommand(sublime_plugin.TextCommand):
    """Convert Chars into XML/HTML Entities"""
    def run(self, edit):
        for region in self.view.sel():
            if not region.empty():
                self.view.replace(edit, region, escape(self.view.substr(region), True))


class ConvertHtmlToCharsCommand(sublime_plugin.TextCommand):
    """Convert XML/HTML Entities into Chars"""
    def run(self, edit):
        for region in self.view.sel():
            if not region.empty():
                text = re.sub('&(%s);' % '|'.join(htmlentitydefs.name2codepoint),
                    lambda m: unichr(htmlentitydefs.name2codepoint[m.group(1)]), self.view.substr(region))
                self.view.replace(edit, region, text)


class ConvertCamelUnderscoresCommand(sublime_plugin.TextCommand):
    """Convert CamelCase to under_scores and vice versa"""
    def run(self, edit):
        for region in self.view.sel():
            if not region.empty():
                text = self.view.substr(region)
                text = self.toCamelCase(text) if '_' in text else self.toUnderscores(text)
                self.view.replace(edit, region, text)

    def toUnderscores(self, name):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    def toCamelCase(self, name):
        return ''.join(map(lambda x: x.capitalize(), name.split('_')))


class ConvertToUnicodeNotationCommand(sublime_plugin.TextCommand):
    """Convert string to Unicode notation"""
    def run(self, edit):
        pattern = re.compile(r'\s+')

        for region in self.view.sel():
            if not region.empty():
                text = ''
                for c in self.view.substr(region):
                    if not re.match(pattern, c) and (c < 0x20 or c > 0x7e):
                        text += '\\u{0:04X}'.format(ord(c))
                    else:
                        text += c

                self.view.replace(edit, region, text)


class ConvertFromUnicodeNotationCommand(sublime_plugin.TextCommand):
    """Convert string from Unicode notation"""
    def run(self, edit):
        pattern = re.compile(r'(\\u)([0-9a-fA-F]{2,4})')

        for region in self.view.sel():
            if not region.empty():
                text = re.sub(pattern, lambda m: unichr(int(m.group(2), 16)), self.view.substr(region))
                self.view.replace(edit, region, text)


class ConvertToBase64Command(sublime_plugin.TextCommand):
    """Encode string with base64"""
    def run(self, edit):
        for region in self.view.sel():
            if not region.empty():
                self.view.replace(edit, region, base64.b64encode(self.view.substr(region).encode('utf-8')))


class ConvertFromBase64Command(sublime_plugin.TextCommand):
    """Decode string with base64"""
    def run(self, edit):
        for region in self.view.sel():
            if not region.empty():
                try:
                    text = base64.b64decode(self.view.substr(region).encode('ascii', 'ignore'))
                    self.view.replace(edit, region, text.decode('utf-8'))
                except:
                    pass


class ConvertMd5Command(sublime_plugin.TextCommand):
    """Calculate MD5 hash"""
    def run(self, edit):
        for region in self.view.sel():
            if not region.empty():
                hash = md5(self.view.substr(region)).hexdigest()
                self.view.replace(edit, region, hash)


class ConvertTimeFormatCommand(sublime_plugin.TextCommand):
    """This will allow you to convert epoch to human readable date and vice versa"""
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    def run(self, edit):
        for region in self.view.sel():
            if not region.empty():
                text = self.view.substr(region)

                result = self.from_unix(text) if text.isdigit() else self.to_unix(text)

                if result:
                    self.view.replace(edit, region, result)
                else:
                    sublime.status_message('Convert error.')

    def from_unix(self, timestamp):
        sublime.status_message('Convert from epoch to human readable date.')
        return datetime.fromtimestamp(int(timestamp)).strftime(self.DATE_FORMAT)

    def to_unix(self, timestr):
        sublime.status_message('Convert from human readable date to epoch.')
        try:
            return parse(timestr).strftime('%s')
        except:
            return False


class InsertTimeStamp(sublime_plugin.TextCommand):
    """This will allow you to insert timestamp to current position"""
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    def run(self, edit):
        for region in self.view.sel():
            self.view.insert(edit, region.begin(), time.strftime(self.DATE_FORMAT))
