from _typeshed import Incomplete

class _SwigNonDynamicMeta(type):
    __setattr__: Incomplete

CAP_CHOWN: Incomplete
CAP_DAC_OVERRIDE: Incomplete
CAP_DAC_READ_SEARCH: Incomplete
CAP_FOWNER: Incomplete
CAP_FSETID: Incomplete
CAP_KILL: Incomplete
CAP_SETGID: Incomplete
CAP_SETUID: Incomplete
CAP_SETPCAP: Incomplete
CAP_LINUX_IMMUTABLE: Incomplete
CAP_NET_BIND_SERVICE: Incomplete
CAP_NET_BROADCAST: Incomplete
CAP_NET_ADMIN: Incomplete
CAP_NET_RAW: Incomplete
CAP_IPC_LOCK: Incomplete
CAP_IPC_OWNER: Incomplete
CAP_SYS_MODULE: Incomplete
CAP_SYS_RAWIO: Incomplete
CAP_SYS_CHROOT: Incomplete
CAP_SYS_PTRACE: Incomplete
CAP_SYS_PACCT: Incomplete
CAP_SYS_ADMIN: Incomplete
CAP_SYS_BOOT: Incomplete
CAP_SYS_NICE: Incomplete
CAP_SYS_RESOURCE: Incomplete
CAP_SYS_TIME: Incomplete
CAP_SYS_TTY_CONFIG: Incomplete
CAP_MKNOD: Incomplete
CAP_LEASE: Incomplete
CAP_AUDIT_WRITE: Incomplete
CAP_AUDIT_CONTROL: Incomplete
CAP_SETFCAP: Incomplete
CAP_MAC_OVERRIDE: Incomplete
CAP_MAC_ADMIN: Incomplete
CAP_SYSLOG: Incomplete
CAP_WAKE_ALARM: Incomplete
CAP_BLOCK_SUSPEND: Incomplete
CAP_AUDIT_READ: Incomplete
CAP_PERFMON: Incomplete
CAP_BPF: Incomplete
CAP_CHECKPOINT_RESTORE: Incomplete
CAP_LAST_CAP: Incomplete
CAPNG_DROP: Incomplete
CAPNG_ADD: Incomplete
CAPNG_EFFECTIVE: Incomplete
CAPNG_PERMITTED: Incomplete
CAPNG_INHERITABLE: Incomplete
CAPNG_BOUNDING_SET: Incomplete
CAPNG_AMBIENT: Incomplete
CAPNG_SELECT_CAPS: Incomplete
CAPNG_SELECT_BOUNDS: Incomplete
CAPNG_SELECT_BOTH: Incomplete
CAPNG_SELECT_AMBIENT: Incomplete
CAPNG_SELECT_ALL: Incomplete
CAPNG_FAIL: Incomplete
CAPNG_NONE: Incomplete
CAPNG_PARTIAL: Incomplete
CAPNG_FULL: Incomplete
CAPNG_PRINT_STDOUT: Incomplete
CAPNG_PRINT_BUFFER: Incomplete
CAPNG_NO_FLAG: Incomplete
CAPNG_DROP_SUPP_GRP: Incomplete
CAPNG_CLEAR_BOUNDING: Incomplete
CAPNG_INIT_SUPP_GRP: Incomplete
CAPNG_CLEAR_AMBIENT: Incomplete
CAPNG_UNSET_ROOTID: Incomplete
CAPNG_SUPPORTS_AMBIENT: Incomplete

def capng_clear(set): ...
def capng_fill(set): ...
def capng_setpid(pid): ...
def capng_get_caps_process(): ...
def capng_update(action, type, capability): ...
def capng_updatev(action, type, capability, capability1: int = 0, capability2: int = 0, capability3: int = 0, capability4: int = 0, capability5: int = 0, capability6: int = 0, capability7: int = 0, capability8: int = 0, capability9: int = 0, capability10: int = 0, capability11: int = 0, capability12: int = 0, capability13: int = 0, capability14: int = 0, capability15: int = 0, capability16: int = 0): ...
def capng_apply(set): ...
def capng_lock(): ...
def capng_change_id(uid, gid, flag): ...
def capng_get_rootid(): ...
def capng_set_rootid(rootid): ...
def capng_get_caps_fd(fd): ...
def capng_apply_caps_fd(fd): ...
def capng_have_capabilities(set): ...
def capng_have_permitted_capabilities(): ...
def capng_have_capability(which, capability): ...
def capng_print_caps_numeric(where, set): ...
def capng_print_caps_text(where, which): ...
def capng_name_to_capability(name): ...
def capng_capability_to_name(capability): ...
