#!/usr/bin/env python3

# Copyright 2023 Clearpath Robotics
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

import os

from typing import Callable, List, Union

from pygments import formatters, highlight, lexers
from pygments.util import ClassNotFound

from simple_term_menu_vendor.simple_term_menu import TerminalMenu


__author__ = 'Roni Kreinin'
__email__ = 'rkreinin@clearpathrobotics.com'
__copyright__ = 'Copyright © 2023 Clearpath Robotics. All rights reserved.'
__license__ = 'Apache 2.0'


class MenuEntry():

    def __init__(self, entry: Union[str, Callable], function) -> None:
        self.function = function
        self.entry = entry

        if isinstance(entry, str):
            self.name = entry
        elif isinstance(entry, Callable):
            self.name = entry()

    def update(self):
        if isinstance(self.entry, Callable):
            self.name = self.entry()

    def select(self):
        self.function()


class Menu():
    menu_cursor = '> '
    menu_cursor_style = ('fg_yellow', 'bold')
    menu_style = ('bg_black', 'fg_yellow')
    menu = None

    def __init__(self, title: Union[str, Callable], menu_entries: List[MenuEntry]) -> None:
        self.title = title
        self.menu_entries = menu_entries
        self.menu_sel = 0
        self.menu = self.create_term_menu()
        self.menu_exit = False

    def update_title(self):
        if isinstance(self.title, str):
            self.name = self.title + '\nPress Q, Esc, or CTRL+C to go back.\n'
        elif isinstance(self.title, Callable):
            self.name = self.title() + '\nPress Q, Esc, or CTRL+C to go back.\n'

        max_len = max(len(line) for line in self.name.split('\n'))
        self.name += '-' * max_len

    def create_term_menu(self):
        menu_entries = []
        for e in self.menu_entries:
            e.update()
            menu_entries.append(e.name)

        self.update_title()

        return TerminalMenu(
            menu_entries,
            title=self.name,
            menu_cursor=self.menu_cursor,
            menu_cursor_style=self.menu_cursor_style,
            menu_highlight_style=self.menu_style,
            cycle_cursor=True,
            clear_screen=True,
            skip_empty_entries=True)

    def refresh_term_menu(self, increment=0):
        self.menu = self.create_term_menu()
        if self.menu_sel is not None:
            for i in range(0, self.menu_sel + increment):
                if self.menu_entries[i].name != '':
                    self.menu._view.increment_active_index()

    def reset_term_menu(self):
        self.menu = self.create_term_menu()
        self.menu_sel = 0

    def exit(self):  # noqa: A003
        self.menu_exit = True

    def show(self, reset=True):
        self.menu_exit = False
        if reset:
            self.reset_term_menu()
        while not self.menu_exit:
            self.menu_sel = self.menu.show()
            if self.menu_sel is None or self.menu_sel >= len(self.menu_entries):
                break
            else:
                self.menu_entries[self.menu_sel].select()
            self.refresh_term_menu()


class OptionsMenu(Menu):

    def __init__(self, title: Union[str, Callable], menu_entries: List[str], default_option=None) -> None:  # noqa: E501
        self.option = default_option
        self.menu_entries = []

        for e in menu_entries:
            self.menu_entries.append(MenuEntry(e, self.set_option))

        super().__init__(title, self.menu_entries)

        if default_option is not None:
            for i, e in enumerate(menu_entries):
                if e == str(default_option):
                    self.menu_sel = i
                    self.refresh_term_menu()

    def set_option(self):
        self.option = self.menu_entries[self.menu_sel].name
        self.exit()

    def show(self):
        super().show(reset=False)
        return self.option


class HelpMenu(Menu):
    # Help -- https://patorjk.com/software/taag/#p=display&v=0&f=Small
    title = """
  _  _     _
 | || |___| |_ __
 | __ / -_) | '_ \\
 |_||_\\___|_| .__/
            |_|
"""

    def __init__(self, text: str, display_help_title=True) -> None:
        if display_help_title:
            super().__init__(self.title + text, [])
        else:
            super().__init__(text, [])


class Prompt():

    def __init__(self, prompt: str, default_response=None, note=None, response_type=str) -> None:
        self.prompt = prompt
        self.default_response = default_response
        self.note = note
        self.response_type = response_type

    def show(self):
        response = None

        if self.note is not None:
            print(self.note)
            print('Press CTRL+C to return without an input.')
            max_len = 0
            for line in self.note.split('\n'):
                max_len = max(max_len, len(line))
            print('-' * max_len)

        try:
            response = input(self.prompt)
        except KeyboardInterrupt:
            return self.default_response

        try:
            self.response_type(response)
        except ValueError:
            if self.response_type == int and response == '':
                return self.default_response

            print('Invalid input [{0}]. {1} required.'.format(response, self.response_type))
            return self.show()

        if response == '':
            response = None

        return response


class PreviewMenu():

    def __init__(self, directories: List[str]) -> None:
        self.directories = directories
        self.menu = TerminalMenu(
                    self.list_files(),
                    preview_command=self.highlight_file,
                    preview_size=0.75)

    def show(self):
        self.menu.show()

    def list_files(self):
        files = []
        for directory in self.directories:
            for file in os.listdir(directory):
                if os.path.isfile(os.path.join(directory, file)):
                    files.append(os.path.join(directory, file))
        return files

    def highlight_file(self, filepath):
        try:
            lexer = lexers.get_lexer_for_filename(filepath, stripnl=False, stripall=False)
        except ClassNotFound:
            lexer = lexers.get_lexer_by_name('text', stripnl=False, stripall=False)
        formatter = formatters.TerminalFormatter(bg='dark')  # dark or light

        try:
            with open(filepath, 'r') as f:
                file_content = f.read()
        except PermissionError:
            file_content = 'Permission denied.\nPlease check file permissions'
        except FileNotFoundError:
            file_content = f'{filepath} was deleted'
        except Exception as err:
            file_content = f'Error reading {filepath}:\n{err}'

        highlighted_file_content = highlight(file_content, lexer, formatter)
        return highlighted_file_content


class ErrorPrompt(Menu):
    # Error -- https://patorjk.com/software/taag/#p=display&v=0&f=Small
    title = """
  ___
 | __|_ _ _ _ ___ _ _
 | _|| '_| '_/ _ \\ '_|
 |___|_| |_| \\___/_|

"""

    def __init__(self, text: str, display_help_title=True) -> None:
        if display_help_title:
            super().__init__(self.title + text, [])
        else:
            super().__init__(text, [])
