# This file is part of curtin. See LICENSE file for copyright and license info.

import shlex
import os

from curtin import util
from curtin.log import logged_call, LOG

try:
    shlex_quote = shlex.quote
except AttributeError:
    # python2.7 uses pipes.quote
    import pipes
    shlex_quote = pipes.quote


def compose_udev_equality(key, value):
    """Return a udev comparison clause, like `ACTION=="add"`."""
    assert key == key.upper()
    return '%s=="%s"' % (key, value)


def compose_udev_attr_equality(attribute, value):
    """Return a udev attribute comparison clause, like `ATTR{type}=="1"`."""
    assert attribute == attribute.lower()
    return 'ATTR{%s}=="%s"' % (attribute, value)


def compose_udev_setting(key, value):
    """Return a udev assignment clause, like `NAME="eth0"`."""
    assert key == key.upper()
    return '%s="%s"' % (key, value)


def generate_udev_rule(interface, mac):
    """Return a udev rule to set the name of network interface with `mac`.

    The rule ends up as a single line looking something like:

    SUBSYSTEM=="net", ACTION=="add", DRIVERS=="?*",
    ATTR{address}="ff:ee:dd:cc:bb:aa", NAME="eth0"
    """
    rule = ', '.join([
        compose_udev_equality('SUBSYSTEM', 'net'),
        compose_udev_equality('ACTION', 'add'),
        compose_udev_equality('DRIVERS', '?*'),
        compose_udev_attr_equality('address', mac),
        compose_udev_setting('NAME', interface),
        ])
    return '%s\n' % rule


@logged_call()
def udevadm_settle(exists=None, timeout=None):
    settle_cmd = ["udevadm", "settle"]
    if exists:
        # skip the settle if the requested path already exists
        if os.path.exists(exists):
            return
        settle_cmd.extend(['--exit-if-exists=%s' % exists])
    if timeout:
        settle_cmd.extend(['--timeout=%s' % timeout])

    util.subp(settle_cmd)


def udevadm_trigger(devices):
    if devices is None:
        devices = []
    util.subp(['udevadm', 'trigger'] + list(devices))
    udevadm_settle()


def udevadm_info(path=None):
    """ Return a dictionary populated by properties of the device specified
        in the `path` variable via querying udev 'property' database.

    :params: path: path to device, either /dev or /sys
    :returns: dictionary of key=value pairs as exported from the udev database
    :raises: ValueError path is None, ProcessExecutionError on exec error.
    """
    if not path:
        raise ValueError('Invalid path: "%s"' % path)

    info_cmd = ['udevadm', 'info', '--query=property', '--export', path]
    output, _ = util.subp(info_cmd, capture=True)

    # strip for trailing empty line
    info = {}
    for line in output.splitlines():
        if not line:
            continue
        # maxsplit=1 gives us key and remaininng part of line is value
        # py2.7 on Trusty doesn't have keyword, pass as argument
        key, value = line.split('=', 1)
        if not value:
            value = None
        if value:
            # preserve spaces in values to match udev database
            try:
                parsed = shlex.split(value)
            except ValueError:
                # strip the leading/ending single tick from udev output before
                # escaping the value to prevent their inclusion in the result.
                trimmed_value = value[1:-1]
                try:
                    quoted = shlex_quote(trimmed_value)
                    LOG.debug('udevadm_info: quoting shell-escape chars '
                              'in %s=%s -> %s', key, value, quoted)
                    parsed = shlex.split(quoted)
                except ValueError:
                    escaped_value = (
                        trimmed_value.replace("'", "_").replace('"', "_"))
                    LOG.debug('udevadm_info: replacing shell-escape chars '
                              'in %s=%s -> %s', key, value, escaped_value)
                    parsed = shlex.split(escaped_value)
            if ' ' not in value:
                info[key] = parsed[0]
            else:
                # special case some known entries with spaces, e.g. ID_SERIAL
                # and DEVLINKS, see tests/unittests/test_udev.py
                if key == "DEVLINKS":
                    info[key] = shlex.split(parsed[0])
                elif key == 'ID_SERIAL':
                    info[key] = parsed[0]
                else:
                    info[key] = parsed

    return info


def udev_all_block_device_properties():
    import pyudev
    props = []
    c = pyudev.context()
    for device in c.list_devices(subsystem='block'):
        props.append(dict(device.properties))
    return props


# vi: ts=4 expandtab syntax=python
