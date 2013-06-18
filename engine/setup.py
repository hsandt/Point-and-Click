from distutils.core import setup
setup(name='GETA',
      version='1.0',
      package_dir = {'geta': 'source'},
      packages = ['geta'],
      package_data = {'geta' :['*/*.py']}
      )