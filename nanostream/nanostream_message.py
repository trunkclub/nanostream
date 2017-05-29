"""
Copyright (C) 2016 Zachary Ernst
zernst@trunkclub.com or zac.ernst@gmail.com

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import time


class NanoStreamMessage(object):
    """
    A class that contains the message payloads that are queued for
    each ``NanoStreamProcessor``. It holds the messages and lots
    of metadata used for logging, monitoring, etc.
    """

    def __init__(self, message_content):
        self.message_content = message_content
        self.history = []
        self.time_created = time.time()
        self.time_processed = None

    def add_history(self, message):
        """
        We maintain a list of all the previous ``NanoStreamMessage`` objects
        from the history of ``self`` in the attribute ``history``. This is
        done by copying the previous history from the previous message,
        deleting ``history`` from the previous message, and appending
        the previous message to ``self.history``.
        """

        self.history = message.history
        del message.history
        self.history.append(message)

    def __repr__(self):
        s = ': '.join([
            'NanoStreamMessage',
            str(self.time_created)])
        return s
