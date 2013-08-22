# Dudley USB mounter

Dudley is a simple wrapper around udisks that mounts USB filesystems.


## Usage

List available filesystems with

    dudley list

Mount or unmount a filesystem with

    dudley [un]mount <device-id>

where the `device-id` is either the device path or device label given above.
In the background, these actions simply subprocess and parse the output from the
relevent _udisks_ command.

