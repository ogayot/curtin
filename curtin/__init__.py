# This file is part of curtin. See LICENSE file for copyright and license info.

# This constant is made available so a caller can read it
# it must be kept the same as that used in helpers/common:get_carryover_params
KERNEL_CMDLINE_COPY_TO_INSTALL_SEP = "---"

# The 'FEATURES' variable is provided so that users of curtin
# can determine which features are supported.  Each entry should have
# a consistent meaning.
FEATURES = [
    # curtin supports creating swapfiles on btrfs, if possible
    'BTRFS_SWAPFILE',
    # curtin can apply centos networking via centos_apply_network_config
    'CENTOS_APPLY_NETWORK_CONFIG',
    # curtin can configure centos storage devices and boot devices
    'CENTOS_CURTHOOK_SUPPORT',
    # install supports the 'network' config version 1
    'NETWORK_CONFIG_V1',
    # reporter supports 'webhook' type
    'REPORTING_EVENTS_WEBHOOK',
    # has storage-config schema validation
    'STORAGE_CONFIG_SCHEMA',
    # install supports the 'storage' config version 1
    'STORAGE_CONFIG_V1',
    # install supports the 'storage' config version 1 for DD images
    'STORAGE_CONFIG_V1_DD',
    # has separate 'preserve' and 'wipe' config options
    'STORAGE_CONFIG_SEPARATE_PRESERVE_AND_WIPE'
    # subcommand 'system-install' is present
    'SUBCOMMAND_SYSTEM_INSTALL',
    # subcommand 'system-upgrade' is present
    'SUBCOMMAND_SYSTEM_UPGRADE',
    # supports new format of apt configuration
    'APT_CONFIG_V1',
    # has version module
    'HAS_VERSION_MODULE',
    # uefi_reoder has fallback support if BootCurrent is missing
    'UEFI_REORDER_FALLBACK_SUPPORT',
    # fstabs by default are output with passno = 1 if not nodev
    'FSTAB_DEFAULT_FSCK_ON_BLK'
]

__version__ = "22.1"

# vi: ts=4 expandtab syntax=python
