#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 18:42:05 2019

@author: BongoKnight


The MIT License (MIT)

Copyright (c) 2014 Peter Goldsborough

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

import json
from collections import OrderedDict
import os
from stat import ST_SIZE, ST_MTIME
from copy import deepcopy
from datetime import datetime

class JSONPropertiesFileError(Exception):
    pass


class JSONPropertiesFile(object):
    def __init__(self, file_path, default={}):
        self.file_path = file_path
        self._default_properties = default
        self._validate_file_path(file_path)

    def _validate_file_path(self, file_path):
        if not file_path.endswith(".json"):
            raise JSONPropertiesFileError(f"Must be a JSON file: {file_path}")
        if not os.path.exists(file_path):
            self.set(self._default_properties)

    def set(self, properties):
        new_properties = deepcopy(self._default_properties)
        new_properties.update(properties)
        with open(self.file_path, 'w') as file:
            json.dump(new_properties, file, indent=4)


    def get(self):
        properties = deepcopy(self._default_properties)
        with open(self.file_path) as file:
            properties.update(json.load(file, object_pairs_hook=OrderedDict))
        return properties

    def get_file_info(self):
        st = os.stat(self.file_path)
        res = {
            'size':st[ST_SIZE],
            'size_str':str(round(st[ST_SIZE]/1000,2)) + ' KB',
            'last_mod': datetime.fromtimestamp(st[ST_MTIME]).strftime("%Y-%m-%d")
         }
        return res