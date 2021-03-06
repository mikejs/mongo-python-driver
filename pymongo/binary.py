# Copyright 2009 10gen, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Representation of binary data to be stored in or retrieved from Mongo.

This is necessary because we want to store normal strings as the Mongo string
type. We need to wrap binary so we can tell the difference between what should
be considered binary and what should be considered a string.
"""

import types


class Binary(str):
    """Binary data stored in or retrieved from Mongo.
    """

    def __new__(cls, data, subtype=2):
        """Initialize a new binary object.

        `subtype` is a binary subtype for this data. For more information on
        subtypes, see the Mongo wiki_.

        .. _wiki: %s

        Raises TypeError if `data` is not an instance of str or `subtype` is
        not an instance of int. Raises ValueError if `subtype` not in [0, 256).

        :Parameters:
          - `data`: the binary data to represent
          - `subtype` (optional): the binary subtype to use
        """ % "http://www.mongodb.org/display/DOCS/BSON#BSON-noteondatabinary"
        if not isinstance(data, types.StringType):
            raise TypeError("data must be an instance of str")
        if not isinstance(subtype, types.IntType):
            raise TypeError("subtype must be an instance of int")
        if subtype >= 256 or subtype < 0:
            raise ValueError("subtype must be contained in [0, 256)")
        self = str.__new__(cls, data)
        self.__subtype = subtype
        return self

    def subtype(self):
        """Get the subtype of this binary data.
        """
        return self.__subtype
    subtype = property(subtype)

    def __eq__(self, other):
        if isinstance(other, Binary):
            return (self.__subtype, str(self)) == (other.__subtype, str(other))
        return NotImplemented

    def __repr__(self):
        return "Binary(%s, %s)" % (str.__repr__(self), self.__subtype)
