#!/usr/bin/env python

import tarfile
import xmlrpclib
import optparse
import StringIO
import sys


class Object(object):
    """Represents an XVA metadata object, for example a VM, VBD, VDI, SR,
        VIF or Network.

       Fields can be accessed directly (e.g. print x.name_label) and modified
       in-place (e.g. x.name_label="new name")."""
    def __init__(self, cls, id, snapshot):
        self._cls = cls
        self._id = id
        self._snapshot = snapshot

    def marshal(self):
        return {"class": self._cls, "id": self._id, "snapshot": self._snapshot}

    def __getattribute__(self, name):
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            return self._snapshot[name]

    def __str__(self):
        name = self._snapshot["uuid"]
        if "name_label" in self._snapshot:
            name = name + ", name_label=" + self._snapshot["name_label"]
        return "%s/%s=%s" % (self._cls, self._id, name)


class MarshallingError(Exception):
    """Raised whenever we fail to regenerate the XVA metadata."""

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "MarshallingError: " + self.message


class XVA(object):
    """Represents an XVA archive.

       Metadata objects can be listed, modified and then the whole archive can
       be saved to a fresh file. All disk blocks will be copied from the old
       archive to the new."""
    def __init__(self, input, ova):
        self._input = input
        self._version = ova["version"]
        self._objects = map(lambda x: Object(x["class"],
                            x["id"],
                            x["snapshot"]),
                            ova["objects"])

    def list(self):
        return self._objects

    def version(self):
        return self._version

    def set_version(self, k, v):
        self._version[k] = v

    def save(self, fileobj):
        # Reconstruct the ova.xml from Objects
        ova_txt = xmlrpclib.dumps(({
            "version": self._version,
            "objects": map(lambda x: x.marshal(), self._objects)
            },))
        prefix = "<params>\n<param>\n"
        suffix = "</param>\n</params>\n"
        if not(ova_txt.startswith(prefix)) or not(ova_txt.endswith(suffix)):
            raise MarshallingError("xmlrpclib produced an unexpected prefix "
                                   "or suffix")
        ova_txt = ova_txt[len(prefix):(len(ova_txt)-len(suffix))]

        # Write the new ova.xml
        output = tarfile.TarFile(mode='w', fileobj=fileobj)
        tarinfo = tarfile.TarInfo("ova.xml")
        tarinfo.size = len(ova_txt)
        output.addfile(tarinfo, StringIO.StringIO(ova_txt))
        # Stream the contents of the input, copying to the output
        for name in self._input.getnames():
            if name == "ova.xml":
                continue
            member = self._input.getmember(name)
            output.addfile(member, self._input.extractfile(member))
        output.close()


def extract_xva(name):
    t = tarfile.open(name=name)
    ova_txt = t.extractfile("ova.xml").read()
    return t, ova_txt


def open_xva(name):
    t, ova_txt = extract_xva(name)
    ova = xmlrpclib.loads("<params><param>" +
                          ova_txt +
                          "</param></params>")[0][0]
    return XVA(t, ova)
