from setuptools import setup


setup(
    name='flask-filerev',
    version='0.1.0',
    description='Flask-FileRev',
    author='Boris Raicheff',
    author_email='b@raicheff.com',
    url='https://github.com/raicheff/flask-filerev',
    install_requires=['flask', 'pyyaml'],
    py_modules=['flask_filerev'],
)