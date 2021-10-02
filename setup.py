#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import io
import sys

# Attempt to import setuptools
try:
	print("Importing 'setuptools' ")
	import setuptools
except ImportError:
	print("Error - 'setuptools' is not installed. Install it by executing: 'pip install setuptools' and re-execute this script\nAborting..")
	sys.exit(1)

# README.md
print("Reading 'README.md' file")
with io.open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Package Version
print("Setting package version")
temp_ver = os.environ.get("LOCAL_BUILD_VERSION", "1.0")
devStatus = "4 - Beta"  # For build statuses see: https://pypi.python.org/pypi?%3Aaction=list_classifiers
pkg_version = f"{temp_ver}.dev0"
if "JENKINS_BUILD_VERSION" in os.environ and "JENKINS_BUILD_BRANCH" in os.environ:
	print("This is Jenkins-CI build:")
	print(f"JENKINS_BUILD_VERSION = {os.environ['JENKINS_BUILD_VERSION']}")
	print(f"JENKINS_BUILD_BRANCH = {os.environ['JENKINS_BUILD_BRANCH']}")
	print(f"JENKINS_PKG_DEV_STATUS = {os.environ['JENKINS_PKG_DEV_STATUS']}")
	temp_ver = os.environ.get('JENKINS_BUILD_VERSION', pkg_version)  # For releases should be:  'Development Status :: 5 - Production/Stable'
	devStatus = os.environ.get('JENKINS_PKG_DEV_STATUS', devStatus)

print('')
print('Package Version Details:')
print(f"Package version: {pkg_version}")
print(f"Package development status: {devStatus}")

setuptools.setup(
     name='davis8988-hello',  
     version=pkg_version,
     author="David Yair",
     author_email="Davismarsel@gmai.com",
     description="Awesome modules & libs",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/Davis8988/pip-pkg-davis8988-hello.git",
	 python_requires='>=3.6,<4',
	 packages=setuptools.find_packages(where="src"),
	 package_dir={"": "src"},
	 license='MIT',
	 license_file = 'LICENSE.txt',
	 install_requires=[
		"pip>=1.1"
	 ],
     classifiers=[
		 "Development Status :: {}".format(devStatus),
         "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )