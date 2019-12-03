""" setup for custom-sed """
#!/usr/bin/env python

from setuptools import setup, find_packages


def reqs_from_file(filename):
    """ Read the setup requirements from a requirements file """
    with open(filename) as f:
        lineiter = (line.rstrip() for line in f if not line.startswith("#"))
        return list(filter(None, lineiter))


setup(
    name='custom_sed',
    version='0.0.1',
    description='Tool for automatically applying changes to a directory of files',
    author='Hugh Brown',
    author_email='hughdbrown@yahoo.com',

    # Required packages
    install_requires=reqs_from_file('requirements.txt'),
    # tests_require=reqs_from_file('test-requirements.txt'),

    # Main packages
    packages=find_packages(),
    zip_safe=False,

    entry_points={
        'console_scripts': [
            # Python modifiers
            'autopylint=src.autopylint:main',
            'absolute_import=src.apps.absolute_import:main',
            'constant_array=src.apps.constant-array:main',
            'documented_as_of=src.apps.documented_as_of:main',
            'inject_import=src.apps.inject_import:main',
            'key_value_item=src.apps.key_value_item:main',
            'next=src.apps.next:main',
            'role_helper=src.apps.role_helper:main',
        ],
    },
)