#!/usr/bin/env python
#
# Navigator.py
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


import PyV8
import os
import httplib2
import urlparse
import hashlib
import logging
import socket
from .Plugin import Plugin

class AboutBlank(httplib2.HttpLib2Error): 
    pass

log = logging.getLogger("Thug")

class Plugins(list):
    def __init__(self):
        list.__init__(self)

    @property
    def length(self):
        return len(self)


class Navigator(PyV8.JSClass):
    def __init__(self, personality, window = None):
        self.personality = log.ThugOpts.Personality[personality]
        self.plugins     = Plugins()  # An array of the plugins installed in the browser
        self._window     = window
        self._mimeTypes = { 'application/pdf':
                                    {
                                        'description'   : 'Adobe Acrobat Plug-In',
                                        'suffixes'      : 'pdf',
                                        'type'          : 'application/pdf',
                                        'enabledPlugin' : Plugin({'name'        : 'Adobe Acrobat %s' % (log.ThugVulnModules.acropdf_pdf, ),
                                                                  'version'     : '%s' % (log.ThugVulnModules.acropdf_pdf, ),
                                                                  'description' : 'Adobe Acrobat Plug-In'
                                                                  }),
                                        'enabled'       : True,
                                    },

                            'application/x-shockwave-flash':
                                    {
                                        'description'   : 'Shockwave Flash',
                                        'suffixes'      : 'swf',
                                        'type'          : 'application/x-shockwave-flash',
                                        'enabledPlugin' : Plugin({'name'        : 'Shockwave Flash %s' % (log.ThugVulnModules.shockwave_flash, ),
                                                                  'version'     : '%s' % (log.ThugVulnModules.shockwave_flash, ),
                                                                  'description' : 'Shockwave Flash %s' % (log.ThugVulnModules.shockwave_flash, ),
                                                                  }),
                                        'enabled'       : True,
                                    },

                            'application/x-ms-wmz':
                                    {   
                                        'description'   : 'Windows Media Player',
                                        'suffixes'      : 'wmz',
                                        'type'          : 'application/x-ms-wmz',
                                        'enabledPlugin' : Plugin({'name'        : 'Windows Media Player 7',
                                                                  'version'     : '7',
                                                                  'description' : 'Windows Media Player 7',
                                                                  }), 
                                        'enabled'       : True,
                                    },  

                            }  
   
        for p in self._mimeTypes.values():
            self.plugins.append(p['enabledPlugin'])

    @property
    def window(self):
        return self._window

    @property
    def appCodeName(self):
        """
            The internal "code" name of the current browser
        """
        return self.personality['appCodeName']

    @property
    def appName(self):
        """
            The official name of the browser
        """
        return self.personality['appName']

    @property
    def appVersion(self):
        """
            The version of the browser as a string
        """
        return self.personality['appVersion']

    @property
    def userAgent(self):
        """
            The user agent string for the current browser
        """
        return self.personality['userAgent']

    @property
    def buildId(self):
        """
            The build identifier of the browser (e.g. "2006090803")
        """
        return ""               

    @property
    def cookieEnabled(self):
        """
            A boolean indicating whether cookies are enabled
        """
        return True

    @property
    def language(self):
        """
            A string representing the language version of the browser
        """
        return "en"

    @property
    def mimeTypes(self):
        """
            A list of the MIME types supported by the browser
        """
        return self._mimeTypes 

    @property
    def onLine(self):
        """
            A boolean indicating whether the browser is working online
        """
        return True

    @property
    def oscpu(self):
        """
            A string that represents the current operating system
        """
        return ""

    @property
    def platform(self):
        """
            A string representing the platform of the browser
        """
        return self.personality['platform']

    @property
    def product(self):
        """
            The product name of the current browser (e.g. "Gecko")
        """
        return ""

    @property
    def productSub(self):
        """
            The build number of the current browser (e.g. "20060909")
        """
        return ""

    @property
    def securityPolicy(self):
        """
            An empty string. In Netscape 4.7x, returns "US & CA domestic policy" or "Export policy".
        """
        return ""

    @property
    def vendor(self):
        """
            The vendor name of the current browser (e.g. "Netscape6")
        """
        return ""

    @property 
    def vendorSub(self):
        """
            The vendor name of the current browser (e.g. "Netscape6")
        """
        return ""

    @property
    def appMinorVersion(self):
        return self.personality['appMinorVersion']

    @property
    def browserLanguage(self):
        return "en"

    @property
    def cpuClass(self):
        return "x86"

    @property
    def systemLanguage(self):
        return "en"

    @property
    def userLanguage(self):
        return "en"

    # Indicates whether the host browser is Java-enabled or not.
    def javaEnabled(self, *arg):
        return True

    # Lets code check to see if the document at a given URI is
    # available without using the network.
    def mozIsLocallyAvailable(self, *arg):
        return False

    # Sets a user preference.
    # self method is only available to privileged code, and you
    # should use XPCOM Preferences API instead.
    def preference(self, *arg):
        pass

    # Allows web sites to register themselves as a possible handler
    # for a given MIME type.
    def registerContentHandler(self, *arg):
        pass

    # New in Firefox 3
    # Allows web sites to register themselves as a possible handler
    # for a given protocol.
    def registerProtocolHandler(self, *arg):
        pass

    # Obsolete
    # Returns false. JavaScript taint/untaint functions removed in
    # JavaScript 1.2[1]
    def taintEnabled(self, *arg):
        return False

    def fetch(self, url, redirect_type = None):
        response = dict()
        content  = ''

        if url == 'about:blank':
            #return response, content
            raise AboutBlank

        h = httplib2.Http('/tmp/thug-cache-%s' % (os.getuid(), ),
                          proxy_info = log.ThugOpts.proxy_info,
                          timeout    = 10,
                          disable_ssl_certificate_validation = True)

        headers = {
            'Cache-Control'   : 'no-cache',
            'Accept-Language' : 'en-US',
            'Accept'          : '*/*',
            'User-Agent'      :  self.userAgent
        }

        if self._window.url not in ('about:blank', ):
            headers['Referer'] = self._window.url
        
        if self._window.doc.cookie:
            headers['Cookie'] = self._window.doc.cookie

        _url = urlparse.urlparse(url)

        handler = getattr(log.SchemeHandler, 'handle_%s' % (_url.scheme, ), None)
        if handler:
            handler(self._window, url)
            return

        if not _url.netloc:
            msg = "[Navigator URL Translation] %s --> " % (url, )
            url = urlparse.urljoin(self._window.url, url)
            msg = "%s %s" % (msg, url)
            log.warning(msg)

        if redirect_type:
            log.ThugLogging.add_behavior_warn(("[%s redirection] %s -> %s" % (redirect_type, 
                                                                              self._window.url, 
                                                                              url, )))

        mime_base = log.baseDir

        try:
            response, content = h.request(url, redirections = 1024, headers = headers)
            if 'content-type' in response:
                mime_base = os.path.join(mime_base, response['content-type'])
        except socket.timeout:
            log.warning("Timeout reached while fetching %s" % (url, ))
            log.ThugLogging.log_redirect(response)
            raise
        except socket.error as e:
            log.warning("Socket error [%s]: %s" % (url, e.strerror))
            log.ThugLogging.log_redirect(response)
            raise
        except httplib2.ServerNotFoundError as e:
            log.warning("ServerNotFoundError: %s" % (e, ))
            log.ThugLogging.log_redirect(response)
            raise

        log.ThugLogging.add_behavior_warn("[HTTP] URL: %s (Status: %s, Referrer: %s)" % (response['content-location'] if 'content-location' in headers else url,
                                                                                         response['status'],
                                                                                         headers['Referer'] if 'Referer' in headers else 'None'))
        log.ThugLogging.log_redirect(response)

        if response.status == 404:
            log.warning("FileNotFoundError: %s" % (url, ))
            return response, content

        md5 = hashlib.md5()
        md5.update(content)
        filename = md5.hexdigest()

        try:
            os.makedirs(mime_base)
        except:
            pass

        with open(os.path.join(mime_base, filename), 'wb') as fd:
            fd.write(content)

        log.ThugLogging.log_file(content, url)
        return response, content

