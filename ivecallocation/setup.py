import setuptools
import os
from setuptools import setup

data_files = {}
start_dir = os.getcwd()
for package in ['allocation']:
    data_files['ivecallocation.' + package] = []
    os.chdir(os.path.join('ivecallocation', package))
    for data_dir in ('templates', 'static', 'migrations', 'fixtures'):
        data_files['ivecallocation.' + package].extend(
            [os.path.join(subdir,f) for (subdir, dirs, files) in os.walk(data_dir) for f in files]) 
    os.chdir(start_dir)

setup(name='django-ivecallocation',
    version='1.1.4',
    description='iVEC Allocation',
    long_description='Django iVEC Allocation web application',
    author='Centre for Comparative Genomics',
    author_email='web@ccg.murdoch.edu.au',
    packages=[
        'ivecallocation',
        'ivecallocation.allocation'
    ],
    package_data=data_files,
    zip_safe=False,
    install_requires=[
        'Mango-py==1.3.1-ccg1-3',
        'MarkupSafe==0.15',
        'South==0.7.3',
        'ccg-extras==0.1.5',
        'ccg-auth==0.3.2',
        'ccg-makoloader==0.2.4',
        'ccg-registration==0.8_alpha_1_ccg2',
        'wsgiref==0.1.2',
        'python-memcached==1.44',
        'Mako>=0.5.0',
        'django-extensions>=0.7.1',
        'psycopg2==2.0.8',
        'python-ldap==2.3.13',
        'egenix-mx-base'
    ]
)
