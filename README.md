# Simple USB filesystem mount utility

**dudley** is a 100-line wrapper around _udisks_ that mounts USB filesystems.


## Usage

List available filesystems with

    dudley list

Mount or unmount a filesystem with

    dudley [un]mount <device-id>

where the `device-id` is either the device path or device label given by `list`.

In the background, these actions simply subprocess and parse the output from the
appropriate _udisks_ command.

