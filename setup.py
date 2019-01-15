from setuptools import setup

setup(
    name='nameko_mongo',
    version='1.0.0',
    url='git@git.thunics.org:pytools/nameko-mongo_util.git',
    license='Apache License, Version 2.0',
    author='lijk',
    author_email='ljk19901@gmail.com',
    packages=["nameko_mongo"],
    package_data={'':['*.*']},
    install_requires=[
        "nameko",
        "tornado",
        "pymongo",
    ],
    description='Redis dependency for nameko services',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.4',
    ],
)