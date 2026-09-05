#
# iwinfo
# 
project('iwinfo', ['c'],
  version: files('src/version.txt'),
  meson_version: '>=1.10.0',
  default_options: [
    'c_std=c23',
    'warning_level=3',
    'b_pie=true',
    'prefix=/usr',
    'mandir=share/man',
    ],
)

#
## Configs
#

#
# Install dirs - reused below for both build targets and data/config installs
# so every install_dir is consistent and respects cross-distro overrides.
#
d_etc = get_option('sysconfdir')
d_lib = get_option('libdir')
d_bin = get_option('bindir')
d_man = get_option('mandir')
d_share = get_option('datadir')

cpu_level = get_option('cpu_level')
if cpu_level == 'x86-64-v3'
  cpu_cflags = ['-march=x86-64-v3', '-mtune=generic']
else
  cpu_cflags = ['-march=x86-64', '-mtune=generic']
endif

optimized = false
if get_option('optimization') not in ['0', 'g']
  optimized = true
endif

my_cflags = [
  ## General
  '-D_GNU_SOURCE',
  '-pipe',                              # Speeds up compilation
  '-fno-plt',                           # Optimization for shared library calls
  '-Wmissing-prototypes',               # Warn for global function missing prototype decl
  '-fvisibility=hidden',                # Only exported symbols in shared lib sym table
  ## Memory Protections
  '-fstack-protector-strong',           # Protect function calls with stack canaries
  '-fstack-clash-protection',           # Prevents stack-clash exploits
  '-ftrivial-auto-var-init=zero',       # Eliminate uninitialized stack memory leaks
  '-fzero-call-used-regs=used-gpr',     # Wipe general registers before returning
  ## Control Flow & Runtime Integrity
  '-mshstk',                            # Intel Shadow Stack protection
  '-fcf-protection',                    # Control-flow enforcement
  ## Aggressive Diagnostic Hardening
  '-Wshadow',                           # Warn if local variable/decl shadows another
  '-Wconversion',                       # Warn about type conversions that may alter value
  '-Wformat=2',                         # Warn about format/args mismatch printf, scanf etc
  '-Werror=format-security',            # Also warn about insecure printf format strings
] + cpu_cflags

buildtype = get_option('buildtype')

if optimized
  my_cflags += ['-D_FORTIFY_SOURCE=3']
endif

if get_option('analyzer')
  my_cflags += ['-fanalyzer']
endif

#
# link-time hardening
#
my_ldflags = [
  '-Wl,--as-needed',                    # Limit shared to 'as needed'
  '-Wl,-z,relro',                       # Mark relocation tables read-only
  '-Wl,-z,now',                         # Force immediate binding (Full RELRO)
  '-Wl,-z,noexecstack',                 # Strictly enforce non-executable stack
  '-Wl,-z,pack-relative-relocs',        # Optimize layout with DT_RELR packing
  '-Wl,-z,defs',                        # Catch unresolved symbols at link time, not at runtime
]

#
# Apply cflags/ldflags
#
add_project_arguments(my_cflags, language: 'c')
add_project_link_arguments(my_ldflags, language: 'c')

#
## Dependenceis
#
cc = meson.get_compiler('c')
dep_cap = cc.find_library('cap-ng', required: true)

#
# Python needs these
#
py_mod = import('python')
py = py_mod.find_installation(pure: false)
src_root = meson.project_source_root()
py_dep = py.dependency(embed: true)

inc_dir = []
lib_sources = []

subdir('src/iwinfo')
subdir('src/iwinfo_mod')

#
# Executables
#
# Install must: 
#
#   /usr/bin/setcap cap_chown,cap_dac_override=ep /usr/bin/iwinfo
#
# We do this in pacman's iwinfo.install post_install/post_upgrade
#

iwinfo = executable('iwinfo',
  sources: [
    'src/iwinfo/iwinfo.c',
    ],
  dependencies: [dep_cap],
  c_args: my_cflags,
  link_args: my_ldflags,
  install: true,
  install_dir: d_bin
)

configure_file(
  input: 'src/iwinfo_mod/apps/iwinfo-app.py',
  output: 'iwinfo-app',
  copy: true,
  install_dir: d_lib / 'iwinfo',
  install_mode: 'rwxr-xr-x'
)

#
## Unit Test Executables
#

# ------------------
## Install
#
s_docs = 'src/data/docs'
s_man = 'src/data/man'
s_license = 'src/data/license'
s_etc = 'etc'

manual = 'iwinfo.pdf'

# docs 

install_data(
  [ 
    'README.rst',
    s_docs / manual,
  ],
  install_dir: d_share / 'iwinfo',
  install_tag: 'docs'
)

# license 

install_data(
  [
    s_license / 'License-gpl-2.0.txt',
    s_license / 'License.rst',
  ],
  install_tag: 'license',
  install_dir: d_share / 'licenses/iwinfo',
)

# /etc/iwinfo

install_data(
  [
    s_etc / 'known-hosts.toml.sample',
  ],
  install_tag: 'config',
  install_dir: d_etc / 'iwinfo',
)


