#!/usr/bin/env python
"""QuTiP: The Quantum Toolbox in Python

QuTiP is open-source software for simulating the dynamics of closed and open
quantum systems. The QuTiP library depends on the excellent Numpy, Scipy, and
Cython numerical packages. In addition, graphical output is provided by
Matplotlib.  QuTiP aims to provide user-friendly and efficient numerical
simulations of a wide variety of quantum mechanical problems, including those
with Hamiltonians and/or collapse operators with arbitrary time-dependence,
commonly found in a wide range of physics applications. QuTiP is freely
available for use and/or modification on all common platforms. Being free of
any licensing fees, QuTiP is ideal for exploring quantum mechanics in research
as well as in the classroom.
"""

DOCLINES = __doc__.split('\n')

CLASSIFIERS = """\
Development Status :: 4 - Beta
Intended Audience :: Science/Research
License :: OSI Approved :: BSD License
Programming Language :: Python
Programming Language :: Python :: 3
Topic :: Scientific/Engineering
Operating System :: MacOS
Operating System :: POSIX
Operating System :: Unix
Operating System :: Microsoft :: Windows
"""

# import statements
import os
import sys
from setuptools import find_packages

# The following is required to get unit tests up and running.
# If the user doesn't have, then that's OK, we'll just skip unit tests.
try:
    from setuptools import setup, Extension
    EXTRA_KWARGS = {
        'setup_require': ['pytest-runner'],
        'tests_require': ['pytest']
    }
except:
    from distutils.core import setup
    from distutils.extension import Extension
    EXTRA_KWARGS = {}

try:
    import numpy as np
except ImportError as e:
    raise ImportError("numpy is required at installation") from e

#from Cython.Build import cythonize
#from Cython.Distutils import build_ext

# all information about QuTiP goes here
MAJOR = 0
MINOR = 0
MICRO = 1
ISRELEASED = False
VERSION = '%d.%d.%d' % (MAJOR, MINOR, MICRO)
REQUIRES = ['numpy (>=1.12)', 'scipy (>=1.0)', 'qutip (>=4.5)']
EXTRAS_REQUIRE = {'graphics': ['matplotlib(>=1.2.1)']}
INSTALL_REQUIRES = ['numpy>=1.12', 'scipy>=1.0', 'qutip>=4.5']
PACKAGES = find_packages(where="src")
PACKAGE_DIR = {'': 'src'}
PACKAGE_DATA = {}

# If we're missing numpy, exclude import directories until we can
# figure them out properly.
INCLUDE_DIRS = [np.get_include()] if np is not None else []
NAME = "qutip_qip"
AUTHOR = ("Alexander Pitchford, Paul D. Nation, Robert J. Johansson, "
          "Chris Granade, Arne Grimsmo, Nathan Shammah, Shahnawaz Ahmed, "
          "Neill Lambert, Eric Giguere, Boxi Li")
AUTHOR_EMAIL = ("alex.pitchford@gmail.com, nonhermitian@gmail.com, "
                "jrjohansson@gmail.com, cgranade@cgranade.com, "
                "arne.grimsmo@gmail.com, nathan.shammah@gmail.com, "
                "shahnawaz.ahmed95@gmail.com, nwlambert@gmail.com, "
                "eric.giguere@usherbrooke.ca, etamin1201@gmail.com")
LICENSE = "BSD"
DESCRIPTION = DOCLINES[0]
LONG_DESCRIPTION = "\n".join(DOCLINES[2:])
KEYWORDS = "quantum physics dynamics"
URL = "http://qutip.org"
CLASSIFIERS = [_f for _f in CLASSIFIERS.split('\n') if _f]
PLATFORMS = ["Linux", "Mac OSX", "Unix", "Windows"]


def git_short_hash():
    try:
        git_str = "+" + os.popen('git log -1 --format="%h"').read().strip()
    except:
        git_str = ""
    else:
        if git_str == '+': #fixes setuptools PEP issues with versioning
            git_str = ''
    return git_str

FULLVERSION = VERSION
if not ISRELEASED:
    FULLVERSION += '.dev'+str(MICRO)+git_short_hash()

# NumPy's distutils reads in versions differently than
# our fallback. To make sure that versions are added to
# egg-info correctly, we need to add FULLVERSION to
# EXTRA_KWARGS if NumPy wasn't imported correctly.
if np is None:
    EXTRA_KWARGS['version'] = FULLVERSION


def write_version_py(filename='src/qutip_qip/version.py'):
    cnt = """\
# THIS FILE IS GENERATED FROM QUTIP SETUP.PY
short_version = '%(version)s'
version = '%(fullversion)s'
release = %(isrelease)s
"""
    a = open(filename, 'w')
    try:
        a.write(cnt % {'version': VERSION, 'fullversion':
                FULLVERSION, 'isrelease': str(ISRELEASED)})
    finally:
        a.close()

# always rewrite _version
if os.path.exists('src/qutip_qip/version.py'):
    os.remove('src/qutip_qip/version.py')

write_version_py()

# Add Cython extensions here
cy_exts = []

# Extra link args
_link_flags = []

# If on Win and Python version >= 3.5 and not in MSYS2
# (i.e. Visual studio compile)
if (sys.platform == 'win32'
    and int(str(sys.version_info[0])+str(sys.version_info[1])) >= 35
    and os.environ.get('MSYSTEM') is None):
    _compiler_flags = ['/w', '/Ox']
# Everything else
else:
    _compiler_flags = ['-w', '-O3', '-funroll-loops']
    if sys.platform == 'darwin':
        # These are needed for compiling on OSX 10.14+
        _compiler_flags.append('-mmacosx-version-min=10.9')
        _link_flags.append('-mmacosx-version-min=10.9')

# Setup commands go here
setup(name = NAME,
      version = FULLVERSION,
      packages = PACKAGES,
      package_dir = PACKAGE_DIR,
      include_package_data=True,
      include_dirs = INCLUDE_DIRS,
      # headers = HEADERS,
      author = AUTHOR,
      author_email = AUTHOR_EMAIL,
      license = LICENSE,
      description = DESCRIPTION,
      long_description = LONG_DESCRIPTION,
      keywords = KEYWORDS,
      url = URL,
      classifiers = CLASSIFIERS,
      platforms = PLATFORMS,
      requires = REQUIRES,
      extras_require = EXTRAS_REQUIRE,
      package_data = PACKAGE_DATA,
      zip_safe = False,
      install_requires=INSTALL_REQUIRES,
      **EXTRA_KWARGS
)
_cite = """\
==============================================================================
Installation complete
Please cite QuTiP in your publication.
==============================================================================
For your convenience a bibtex reference can be easily generated using
`qutip.cite()`"""
print(_cite)