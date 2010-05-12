
try:
    from setuptools import setup
except ImportError:
    from distutils import setup

setup(
      name='mvfs',
      version='0.1.0',
      description='Virtual Multi-version File System',
      author='Andrei Savu',
      author_email='contact@andreisavu.ro',
      url='http://github.com/andreisavu/python-mvfs',
      packages=['mvfs']
)

