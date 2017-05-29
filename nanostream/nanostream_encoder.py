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
import cPickle as pickle
import base64


def encode(something):
    """
    We encode all messages as base64-encoded pickle objects in case
    later on, we want to persist them or send them to another system.
    This is extraneous for now.
    """

    return base64.b64encode(pickle.dumps(something))

def decode(something):
    """
    Decodes from base-64 pickled object.
    """

    return pickle.loads(base64.b64decode(something))
