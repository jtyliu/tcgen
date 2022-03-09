import setuptools
from tcgen._version import VERSION
import pathlib
import string


def fix(s):
    # Removes non-printable ASCII characters
    res = ''
    for ch in s:
        if ch in string.printable:
            res += ch
    return res


# Getting dependencies
def parse_requirements_file(path):
    with open(path) as fp:
        dependencies = (d.strip() for d in fp.read().split("\n") if d.strip())
        return [d for d in dependencies if not d.startswith("#")]

def long_description():
    with open("README.md") as fp:
        return fp.read()


setuptools.setup(
    name='cp-tcgen',
    version=VERSION,
    author='Joshua Liu',
    author_email='joshualiu@youarefantastic.com',
    description='Test case generator. Quickly design and generate test cases without all the bulk',
    long_description=long_description(),
    long_description_content_type="text/markdown",
    keywords='program competitive programming codeforces',
    include_package_data=True,
    install_requires=parse_requirements_file('requirements.txt'),
    packages=["tcgen"],
    license='MIT',
    url='https://github.com/JoshuaTianYangLiu/tcgen',
    scripts=['scripts/tcgen', 'scripts/genout'],
)
