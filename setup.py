
# Attempt to import setuptools
import sys
try:
	print("Importing 'setuptools' ")
	import setuptools
except ImportError:
	print("Error - 'setuptools' is not installed. Install it by executing: 'pip install setuptools' and re-execute this script\nAborting..")
	sys.exit(1)
	

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
     name='davis8988-hello',  
     version='1.0.0',
     scripts=['davis8988-hello'] ,
     author="David Yair",
     author_email="Davismarsel@gmail.com",
     description="Extensions & Libs",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/Davis8988/pip-pkg-davis8988-hello.git",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )