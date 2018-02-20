
#!/usr/bin/env python

#
#
# Copyright 2018 Roberto Sierra
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

"""A library that provides a Python interface to the Tienda Mobil API"""

__author__       = 'Roberto Sierra'
__email__        = 'roberto@ideadigital.com.ar'
__copyright__    = 'Copyright (c) 2018'
__license__      = 'Apache License 2.0'
__version__      = '0.1'
__url__          = 'https://github.com/r-sierra/python-tiendamobil'
__description__  = 'A Python wrapper around the Tienda Mobil API'

from .error import TiendaMobilError         # noqa
from .models import (                       # noqa
    Order,
    OrderPreview,
    OrderItem,
    Customer                                # noqa
)

from .api import Api                        # noqa
