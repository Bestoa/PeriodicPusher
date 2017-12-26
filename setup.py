from setuptools import setup, find_packages
import PeriodicPusher

setup(
    name = PeriodicPusher.__NAME__,
    version = PeriodicPusher.__VERSION__,
    author = PeriodicPusher.__AUTHOR__,
    author_email = 'bestoapache@gmail.com',
    license = 'AGPL',
    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires = [ 'requests', 'instapush' ],
)

