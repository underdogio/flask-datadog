from setuptools import setup

setup(
    name='Flask-DogStatsD',
    version='0.1.0',
    url='https://github.com/50onRed/flask-dogstatsd.git',
    license='BSD',
    author='50onRed',
    author_email='dev@50onred.com',
    description='Access to dogstatsd in your app.',
    py_modules=['flask_dogstatsd'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=['Flask', 'datadog'],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
