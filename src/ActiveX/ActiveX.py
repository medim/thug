#!/usr/bin/env python
#
# ActiveX.py
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA  02111-1307  USA

import os
import new
import logging
from .CLSID import CLSID

log = logging.getLogger("Thug")

class _ActiveXObject:
    shockwave_flash = { 'shockwaveflash.shockwaveflash'    : '10', 
                        'shockwaveflash.shockwaveflash.9'  : '9' ,
                        'shockwaveflash.shockwaveflash.10' : '10' }

    def __init__(self, window, cls, type = 'name'):
        self.funcattrs = dict()
        self._window   = window
        object         = None
        methods        = dict()
        self.shockwave = log.ThugVulnModules.shockwave_flash.split('.')[0]

        if type == 'id':
            if len(cls) > 5 and cls[:6].lower() == 'clsid:':
                cls = cls[6:].upper()

            if cls.startswith('{') and cls.endswith('}'):
                cls = cls[1:-1]
        
        if type == 'name':
            cls = cls.lower()

        # Shockwave Flash
        if cls in self.shockwave_flash and not self.shockwave in (self.shockwave_flash[cls], ):
            log.warning("Unknown ActiveX Object: %s" % (cls, ))
            raise TypeError()

        _cls = cls

        # JavaPlugin
        if cls.lower().startswith('javaplugin'): 
            if not cls.endswith(log.ThugVulnModules.javaplugin):
                log.warning("Unknown ActiveX Object: %s" % (cls, ))
                raise TypeError()
            else:
                _cls = 'javaplugin'

        # JavaWebStart
        if cls.lower().startswith('javawebstart.isinstalled'):
            if not cls.endswith(log.ThugVulnModules.javawebstart_isinstalled):
                log.warning("Unknown ActiveX Object: %s" % (cls, ))
                raise TypeError()
            else:
                _cls = 'javawebstart.isinstalled'

        for c in CLSID:
            if _cls in c[type]:
                object = c
                break

        if not object:
            log.warning("Unknown ActiveX Object: %s" % (cls, ))
            #return None
            raise TypeError()

        log.warning("ActiveXObject: %s" % (cls, ))

        for method_name, method in c['methods'].items():
            _method = new.instancemethod(method, self, _ActiveXObject)
            setattr(self, method_name, _method)
            methods[method] = _method

        for attr_name, attr_value in c['attrs'].items():
            setattr(self, attr_name, attr_value)

        for attr_name, attr_value in c['funcattrs'].items():
            self.funcattrs[attr_name] = methods[attr_value]

    def __setattr__(self, name, value):
        self.__dict__[name] = value
            
        if name in self.funcattrs:
            self.funcattrs[name](value)

    def __getattribute__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]

        log.warning("Unknown ActiveX Object attribute: %s" % (name, ))


def register_object(s, clsid):
    funcattrs = dict()
    methods   = dict()
    object    = None

    if not clsid.startswith('clsid:'):
        log.warning("Unknown ActiveX object: %s" % (clsid, ))
        return None

    clsid = clsid[6:].upper()
    if clsid.startswith('{') and clsid.endswith('}'):
        clsid = clsid[1:-1]

    for c in CLSID:
        if clsid in c['id']:
            object = c
            break

    if object is None:
        log.warning("Unknown ActiveX object: %s" % (clsid, ))
        #return None
        raise TypeError()

    for method_name, method in c['methods'].items():
        _method = new.instancemethod(method, s, s.__class__)
        setattr(s, method_name, _method)
        methods[method] = _method

    for attr_name, attr_value in c['attrs'].items():
        setattr(s, attr_name, attr_value)

    # PLEASE REVIEW ME!
    for attr_name, attr_value in c['funcattrs'].items():
        if 'funcattrs' not in s.__dict__:
            s.__dict__['funcattrs'] = dict()

        s.__dict__['funcattrs'][attr_name] = methods[attr_value]
