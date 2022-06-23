from setuptools import setup, find_packages

setup(name='Metadata-File-Searcher',
      version='1.0',
      description='Allows to filter the content of a folder by its metadata tags',
      author='Eric Canas',
      author_email='eric@ericcanas.com',
      url='https://github.com/Eric-Canas/JPEG-MetaTags-Filter',
      license='MIT',
      windows=[{"script": "main.py"}],
      packages=find_packages(),
      classifiers=['Programming Language :: Python :: 3.10',
                   'License :: OSI Approved :: MIT License',
                   'Operating System :: Windows :: Windows 10',
                   'Development Status :: Release',
                   'Environment :: GUI',
                   'Intended Audience :: End Users/Desktop',
                   'Topic :: Multimedia :: File Management'])
