## `twisted/names/common.py` で以下のメソッドを定義，書き換え 

class ResolverBase:
    def getHostByName(self, name, timeout=None, effort=10):
        # XXX - respect timeout
        return self.lookupAllRecords(name, timeout
            ).addCallback(self._cbRecords, name, effort
            )
    
    # defined by paul
    # IResolverSimple
    def getHostByNameV4(self, name, timeout=None, effort=10):
        # XXX - respect timeout
        return self.lookupAddress(name, timeout
            ).addCallback(self._cbRecords, name, effort
            )
    
    # defined by paul
    # IResolverSimple
    def getHostByNameV6Address(self, name, timeout=None, effort=10):
        # XXX - respect timeout
        return self.lookupIPV6Address(name, timeout
            ).addCallback(self._cbRecords, name, effort
            )
    
    # defined by paul
    # IResolverSimple
    def getHostByName6(self, name, timeout=None, effort=10):
        # XXX - respect timeout
        return self.lookupAddress6(name, timeout
            ).addCallback(self._cbRecords, name, effort
            )
