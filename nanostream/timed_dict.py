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

import threading
import time


class TimedDict(dict):
    """
    A dictionary whose keys time out; sends events when keys time out.
    """
    def __init__(self, timeout=10, check_interval=1, timeout_call=None):
        self.timeout = timeout
        self.check_interval = check_interval
        self.base_dict = {}
        self.time_dict = {}
        self.timeout_call = timeout_call
        self.check_thread = threading.Thread(target=self.check_loop)
        self.check_thread.start()
 
    def check_loop(self):
        while 1:
            current_time = time.time()
            for key, value in self.base_dict.iteritems():
                created_time = self.time_dict[key]
                if current_time - created_time > self.timeout:
                    del self.base_dict[key]
                    del self.time_dict[key]
                    if self.timeout_call is not None:
                        self.timeout_call(key, value)
                    break
            time.sleep(self.check_interval)

    def __setitem__(self, key, value):
        current_time = time.time()
        self.base_dict[key] = value
        self.time_dict[key] = current_time

    def __getitem__(self, key):
        return self.base_dict[key]


if __name__ == '__main__':
    def callback(x, y):
        print 'callback with', x, y

    d = TimedDict(timeout_call=callback)
    d['foo'] = 'bar'
    
