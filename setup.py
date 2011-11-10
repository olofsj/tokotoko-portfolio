from setuptools import setup, find_packages

setup(
    name='tokotoko-portfolio',
    version='0.1',
    description='Django app for managing an online portfolio',
    long_description=open('README.md', 'r').read(),
    keywords='django',
    author='Olof Sjöbergh',
    author_email='olofsj at gmail com',
    url='https://github.com/olofsj/tokotoko-portfolio',
    license='BSD',
    package_dir={'portfolio': 'portfolio'},
    include_package_data=True,
    packages=find_packages(),
    zip_safe=False,
)

