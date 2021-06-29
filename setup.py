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
HERE = pathlib.Path(__file__).parent
requirements_path = HERE / 'requirements.txt'
assert requirements_path.is_file()
with open(requirements_path) as f:
    # Windows doesn't want to read files properly for some reason
    install_requires = list(filter(lambda x: len(x) > 0, map(lambda x: fix(x).strip(), f.readlines())))

README = (HERE / "README.md").read_text()

setuptools.setup(
    name='cp-tcgen',
    version=VERSION,
    author='Joshua Liu',
    author_email='joshualiu@youarefantastic.com',
    description='Test case generator. Quickly design and generate test cases without all the bulk',
    long_description=README,
    keywords='program competitive programming codeforces',
    include_package_data=True,
    install_requires=install_requires,
    packages=["tcgen"],
    license='MIT',
    url='https://github.com/JoshuaTianYangLiu/tcgen',
    scripts=['scripts/tcgen', 'scripts/genout'],
)
