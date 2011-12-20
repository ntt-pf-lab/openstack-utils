=================================
OpenStack Utilities Package
=================================

How to install
--------------------------------
easy_install OpenStackUtil-0.0.1dev-py2.7.egg

- Set paste.ini for eash project

[pipeline:openstackapi11]
pipeline = debuglog faultwrap noauth ratelimit extensions osapiapp11

[filter:debuglog]
MAX_RESPONSE_LEN = 500
paste.filter_factory = openstackutil.logger.nova:DebugLogger.factory

How to build package
---------------------------------
python setup.py bdist_egg

