import sys
import os
import subprocess
import StringIO

def get_devices():
    stdout = subprocess.check_output(["udisks", "--enumerate-device-files"])
    lns = stdout.split("\n")

    devices = {}
    k = None
    for line in lns:
        if line.count("/") == 2:
            k = line
            devices[k] = []
        elif k is not None:
            devices[k].append(line)
    return devices

def print_devices(devices):
    for k in devices:
        if True in ("by-uuid" in a for a in devices[k]):
            print(k)
            for s in devices[k]:
                if "by-id" in s:
                    print("\t" + s)
    return

def mount_device(name):
    if name in get_devices():
        subprocess.call(["udisks", "--mount", name])
    else:
        raise UserError("Device name {0} nonexistent".format(name))

def unmount_device(name):
    if name in get_devices():
        subprocess.call(["udisks", "--unmount", name])
    else:
        raise UserError("Device name {0} nonexistent".format(name))

def main():
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
    else:
        devices = get_devices()
        print_devices(devices)
        sys.exit(0)

    if cmd == "list":
        print_devices(get_devices())

    elif cmd == "mount":
        if len(sys.argv) > 2:
            devname = sys.argv[2]
            mount_device(devname)
        else:
            raise UserError("Must provide a device name in order to mount")

    elif cmd == "unmount":
        if len(sys.argv) > 2:
            devname = sys.argv[2]
            unmount_device(devname)
        else:
            raise UserError("Must provide a device name in order to mount")

if __name__ == "__main__":
    main()

class UserError(Exception):
    pass

