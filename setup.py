from setuptools import setup

requires=[
	'simplejson',
	'pymysql',
	'ConfigParser',
	'redis',
	'sqlalchemy'
]


setup(name='ContactBookApp',
      version='1.0',
      description='',
      url='',
      author='Raghvendra',
      author_email='',
      license='',
      # packages=find_pakages(),
      install_requires=requires,
      zip_safe=False)