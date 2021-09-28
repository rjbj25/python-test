from distutils.core import setup
setup(name='python-test',
      version='1.0',
      description='Python Test',
      author='Ramiro Balmaceda',
      author_email='info@rbalmaceda.com',
      url='www.rbalmaceda.com',
      install_requires=[
        'et-xmlfile==1.1.0',
        'greenlet==1.1.1',
        'numpy==1.21.2',
        'openpyxl==3.0.9',
        'pandas==1.3.3',
        'python-dateutil==2.8.2',
        'pytz==2021.1',
        'six==1.16.0',
        'SQLAlchemy==1.4.25',
        ],
     )