from setuptools import setup, find_packages
import os

version = '0.1'

install_requires = [
    'manuel',
    'mock',
    'plone.app.testing',
    'raptus.article.core>=2.0b8',
    'setuptools',
    'unittest2',
],

setup(name='raptus.article.configuration',
      version=version,
      description="Placeful configuration for Raptus Article",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "MANUAL.txt")).read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='Plone Raptus Article',
      author='Nejc Zupan, NiteoWeb Ltd.',
      author_email='nejc.zupan@gmail.com',
      url='http://svn.plone.org/svn/collective/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['raptus', 'raptus.article'],
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
