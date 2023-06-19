from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in hrdemo/__init__.py
from hrdemo import __version__ as version

setup(
	name="hrdemo",
	version=version,
	description="hr",
	author="hr",
	author_email="hr",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
