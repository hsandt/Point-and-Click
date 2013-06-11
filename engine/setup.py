from distutils.core import setup
setup(name='pace',
      version='1.0',
      # package_dir={'': 'source'},
      # packages=['adventure', 'exception', 'helper', 'state', 'tests', 'view']
      packages = ['pace'],
      package_dir = {'pace': 'source'},
      package_data = {'pace' :['*/*.py']}
      )