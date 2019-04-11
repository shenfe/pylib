# coding: utf8

from __future__ import print_function

import io
import os
import sys
import re
import subprocess

import setuptools
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext


NAME = 'libpy'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

REQ_FILES = [
    'requirements.txt',
]

CPP_LIBS = ['libcpp']


def read(name, lines=False, encoding='utf8'):
    with io.open(os.path.join(BASE_DIR, name), 'r', encoding=encoding) as f:
        content = f.read().strip()
        if lines:
            content = content.split('\n')
            reqs = []
            for line in content:
                line = line.split('#')[0].strip()
                if not len(line):
                    continue
                reqs.append(line)
            content = reqs
        return content


def find_version():
    version_file = '%s/__init__.py' % NAME
    version_match = re.search(r'''^__version__ = ['"]([^'"]*)['"]''',
                              read(version_file), re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('version string not found')


def get_requirements():
    reqs = []
    for f in REQ_FILES:
        reqs.extend(read(f, True))
    return reqs


def package_files(directory, f=None):
    if isinstance(directory, (list, tuple)):
        l = [package_files(d, f=f) for d in directory]
        return [item for sublist in l for item in sublist]
    directory = os.path.join(BASE_DIR, directory)
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            if callable(f):
                if f(filename):
                    paths.append(os.path.join('..', path, filename))
                continue
            if isinstance(f, str):
                if re.match(f, filename):
                    paths.append(os.path.join('..', path, filename))
                continue
            paths.append(os.path.join('..', path, filename))
    return paths


def get_cpp_files(src_dir):
    src_files = os.listdir(src_dir)
    src_cc = [os.path.join(src_dir, x) for x in src_files if x.endswith('.cc')]
    return src_cc


class get_pybind_include(object):
    '''
    Helper class to determine the pybind11 include path

    The purpose of this class is to postpone importing pybind11
    until it is actually installed, so that the ``get_include()``
    method can be invoked.
    '''
    def __init__(self, user=False):
        try:
            import pybind11
        except ImportError:
            if subprocess.call([sys.executable, '-m', 'pip', 'install', 'pybind11']):
                raise RuntimeError('pybind11 install failed.')

        self.user = user

    def __str__(self):
        import pybind11
        return pybind11.get_include(self.user)


# As of Python 3.6, CCompiler has a `has_flag` method.
# cf http://bugs.python.org/issue26689
def has_flag(compiler, flags):
    '''
    Return a boolean indicating whether a flag name is supported on
    the specified compiler.
    '''
    import tempfile
    with tempfile.NamedTemporaryFile('w', suffix='.cpp') as f:
        f.write('int main (int argc, char **argv) { return 0; }')
        try:
            compiler.compile([f.name], extra_postargs=flags)
        except setuptools.distutils.errors.CompileError:
            return False
    return True


def cpp_flag(compiler):
    '''
    Return the -std=c++[0x/11/14] compiler flag.
    The c++14 is preferred over c++0x/11 (when it is available).
    '''
    standards = ['-std=c++14', '-std=c++11', '-std=c++0x']
    for standard in standards:
        if has_flag(compiler, [standard]):
            return standard
    raise RuntimeError(
        'Unsupported compiler -- at least C++0x support '
        'is needed!'
    )


class BuildExt(build_ext):
    '''
    A custom build extension for adding compiler-specific options.
    '''
    c_opts = {
        'msvc': ['/EHsc'],
        'unix': [],
    }

    def build_extensions(self):
        if sys.platform == 'darwin':
            all_flags = ['-stdlib=libc++', '-mmacosx-version-min=10.7']
            if has_flag(self.compiler, [all_flags[0]]):
                self.c_opts['unix'] += [all_flags[0]]
            elif has_flag(self.compiler, all_flags):
                self.c_opts['unix'] += all_flags
            else:
                raise RuntimeError(
                    'libc++ is needed! Failed to compile with {} and {}.'.
                    format(' '.join(all_flags), all_flags[0])
                )
        ct = self.compiler.compiler_type
        opts = self.c_opts.get(ct, [])
        extra_link_args = []

        if ct == 'unix':
            opts.append('-DVERSION_INFO="%s"' % self.distribution.get_version())
            opts.append(cpp_flag(self.compiler))
            if has_flag(self.compiler, ['-fvisibility=hidden']):
                opts.append('-fvisibility=hidden')
        elif ct == 'msvc':
            opts.append(
                '/DVERSION_INFO=\\"%s\\"' % self.distribution.get_version()
            )
        for ext in self.extensions:
            ext.extra_compile_args = opts
            ext.extra_link_args = extra_link_args
        build_ext.build_extensions(self)


def create_ext(ext_name):
    lib_name = os.path.split(ext_name.rstrip('/'))[1]
    return Extension(
        lib_name,
        ['%s/lib_pybind.cc' % ext_name] + get_cpp_files('%s/src' % ext_name),
        include_dirs=[
            # Path to pybind11 headers
            get_pybind_include(),
            get_pybind_include(user=True),
            # Path to cpp lib source code
            '%s/src' % ext_name,
        ],
        language='c++',
        extra_compile_args=['-O3 -funroll-loops -pthread -march=native'],
    )


setup(
    name=NAME,
    version=find_version(),
    description='a python library',
    url='https://github.com/shenfe/pylib',
    author='shenke',
    license='BSD',

    install_requires=get_requirements(),

    # package_dir={NAME: NAME},
    package_data={NAME: ['*'] + package_files(['%s/util' % NAME])},
    packages=[NAME],

    cmdclass={'build_ext': BuildExt},
    ext_modules=[create_ext(name) for name in CPP_LIBS],

    entry_points={'console_scripts': ['%s = %s.main:main' % (NAME, NAME)]},
)
