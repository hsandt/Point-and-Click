from distutils.core import setup
setup(name='GETA',
      version='0.1',
      package_dir = {'geta': 'source'},
      packages = ['geta'],
      package_data = {'geta' :['*/*.py']}
      )