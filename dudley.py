
import sys
import subprocess

def get_devices():
    dd = {}
    devices = subprocess.check_output(["udisks", "--enumerate-device-files"])
    for name in filter(lambda s: s.count("/") == 2, devices.split("\n")):
        info = subprocess.check_output(["udisks", "--show-info", name])
        if "filesystem" in info:
            dd[name] = filter(lambda s: s[2:4] != "  ", info.split("\n"))
    return dd

def print_devices(devices):
    for k in devices:
        print k,
        for s in devices[k]:
            if "label" in s:
                print s[8:].strip(),
            if "type" in s:
                print s[7:].strip(),
        print
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
        print_devices(get_devices())
        sys.exit(0)

    if cmd == "list":
        print_devices(get_devices())

    elif cmd == "mount":
        if len(sys.argv) > 2:
            mount_device(sys.argv[2])
        else:
            raise UserError("Must provide a device name in order to mount")

    elif cmd == "unmount":
        if len(sys.argv) > 2:
            unmount_device(sys.argv[2])
        else:
            raise UserError("Must provide a device name in order to mount")

if __name__ == "__main__":
    main()

class UserError(Exception):
    pass

