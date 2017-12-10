from setuptools import setup

setup(name='postfix-filter',
      version='0.1',
      description='Postfix domain filter',
      url='https://github.com/rmakhambetov/postfix-filter-loop',
      author='Roman Makhambetov',
      author_email='rmakhambetov@yandex.ru',
      license='MIT',
      install_requires=[
          'pythonwhois',
          'tldextract',
      ],
      zip_safe=False)