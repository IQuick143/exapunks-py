from setuptools import find_packages, setup
import codecs

with codecs.open('README.md', 'r', 'utf-8') as f:
	readme = f.read()

setup(
	name='exapunks',
	url='https://github.com/IQuick143/exapunks-py',
	author='IQuick143',
	author_email='IQuick143cz@gmail.com',
	license="MIT",
	description='A library for manipulating exapunks savefiles and redshift projects',
	long_description=readme,
	long_description_content_type="text/markdown",
	keywords='exapunks redshift',
	packages=find_packages("exapunks"),
	install_requires=["construct"]
)
