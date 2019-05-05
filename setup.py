from setuptools import setup
from setuptools import find_packages

setup(
	name = "autonet",
	packages = find_packages(),
	version = "0.1.6",
	description = "Some tools of network automated operation for multiple vendors",
	long_description = open("README.md").read(),
	long_description_content_type = "text/markdown",
	author = "Cheng Zheng",
	author_email = "zc8131868@gmail.com",
	url = "https://github.com/zc8131868/Network-Operation",
	keywords = ["network", "automated", "operation"],
	license = "MIT",
	install_requires = [
		"pexpect",
		"IPy>=1.00",
		],
	python_requires = ">=3",
	classifiers = [
		"Development Status :: 3 - Alpha",
		"Intended Audience :: Developers",
		"License :: OSI Approved :: MIT License",
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3.5",
		"Programming Language :: Python :: 3.6",
		"Programming Language :: Python :: 3.7",
		],

	)
