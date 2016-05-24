import os
from setuptools import setup

#README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-modelcopier',
    version='0.1',
    packages=['modelcopier'],
    include_package_data=True,
    license='BSD License',  # example license
    description='Utility to copy tables using model fetches and saves',
    #long_description=README,
    url='https://github.com/sgithens/django-modelcopier',
    author='Steven Githens',
    author_email='sgithens@iu.edu',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License', # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
