from distutils.core import setup
from setuptools import find_packages

with open("README.md", "r") as f:
  long_description = f.read()

setup(name='event_time_format',  # 包名
      version='1.0.3',  # 版本号
      description='event time format',
      long_description=long_description,
      author='errord',
      author_email='errord@gmail.com',
      url='https://github.com/errord/EventTimeFormat',
      project_urls={
        "Source": "https://github.com/errord/EventTimeFormat",
      },
      install_requires=[
        'arrow>=1.1.0',
        'requests>=2.20.1',
        'numpy>=1.21.0',
        'pandas>=1.3.3',
        'tensorflow>=2.5.1',
        'bs4>=0.0.2'
      ],
      license='BSD License',
      packages=find_packages(),
      platforms=["all"],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Topic :: Software Development :: Libraries'
      ],
      )

