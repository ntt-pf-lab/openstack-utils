from setuptools import setup, find_packages
import sys, os

version = '0.0.2'

setup(name='OpenStackUtil',
      version=version,
      description="Utilities Script for OpenStack",
      long_description="""\
- logging middleware for OpenStack""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Nachi Ueno',
      author_email='ueno.nachi@lab.ntt.co.jp',
      url='https://github.com/ntt-pf-lab/openstack-api-logging',
      license='Apache License',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
