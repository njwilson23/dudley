#! /usr/bin/env python

import sys
import subprocess

class Device(object):

    fields = ["label:", "type:", "usage:", "is mounted:"]

    def __init__(self, path):
        self.path = path
        self.getinfo()
        return

    def __repr__(self):
        mnt = "*" if int(self.attr["is mounted:"]) else "_"
        s = "{0:12s}{1:16s}{2:6s}{3:10s}{4:>3s}".format(self.path,
                                            self.attr["label:"],
                                            self.attr["type:"],
                                            self.attr["usage:"],
                                            mnt)
        return s

    def __eq__(self, other):
        for k in self.attr:
            if other in (self.path, self.attr["label:"]):
                return True
        return False

    def getinfo(self):
        self.attr = {}
        info = subprocess.check_output(["udisks", "--show-info", self.path],
                                       universal_newlines=True)
        for line in filter(lambda s: s[2:4] != "  ", info.split("\n")):
            fld = line[:31].strip()
            if fld in self.fields:
                self.attr[fld] = line[31:].strip()

    def isdrive(self):
        return self.attr.get("usage:", "") == "filesystem"

    def mount(self):
        return subprocess.call(["udisks", "--mount", self.path])

    def unmount(self):
        return subprocess.call(["udisks", "--unmount", self.path])


def get_devices():
    dlist = []
    enumf = subprocess.check_output(["udisks", "--enumerate-device-files"],
                                    universal_newlines=True)
    for name in filter(lambda s: s.count("/") == 2, enumf.split("\n")):
        dev = Device(name)
        if dev.isdrive():
            dlist.append(dev)
    return dlist

def print_devices(devices):
    for dev in devices:
        print(dev)
    return

def main():

    devices = get_devices()

    if len(sys.argv) == 1 or sys.argv[1] == "list":
        print_devices(devices)
        sys.exit(0)
    else:
        cmd = sys.argv[1]

    if cmd in ("mount", "unmount"):
        if len(sys.argv) <= 2:
            raise UserError("Must provide a device name in order to mount")
        elif sys.argv[2] not in devices:
            raise UserError("Device \"{0}\" not found".format(sys.argv[2]))
        elif cmd == "mount":
            for dev in devices:
                if dev == sys.argv[2]:
                    ret = dev.mount()
        elif cmd == "unmount":
            for dev in devices:
                if dev == sys.argv[2]:
                    ret = dev.unmount()
                    if dev not in get_devices():
                        print("{0} unmounted".format(dev.attr["label:"]))

    else:
        print("dudley <list|mount|unmount> [device-id]")

if __name__ == "__main__":
    main()

class UserError(Exception):
    pass

