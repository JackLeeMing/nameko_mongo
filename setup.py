from setuptools import setup

setup(
    name='nameko_mongo_util',
    version='1.0.2',
    url='https://github.com/JackLeeMing/nameko_mongo.git',
    license='MIT',
    author='Jaque',
    author_email='1285879942@qq.com',
    packages=["nameko_mongo_util"],
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