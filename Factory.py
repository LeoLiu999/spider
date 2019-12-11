# -*- coding: utf-8 -*-

import Site

class Factory:

    def parseContent(self, siteName, params):
        instance = self.getInstance(siteName)
        if instance is not None:
            return self.run(instance, params)
        else:
            return None

    def run(self, siteObject, params):
        return siteObject.parseContent(params)

    def getInstance(self, siteName):

        if siteName == 'shuquge':
            return Site.ShuqugeSite()
        else:
            return None
