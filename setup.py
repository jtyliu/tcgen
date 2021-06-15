import setuptools
from tcgen._version import VERSION

setuptools.setup(
    name='tcgen',
    version=VERSION,
    author='Joshua Liu',
    author_email='joshualiu@youarefantastic.com',
    description='Test case generator. Quickly design and generate test cases without all the bulk',
    keywords='program competitive programming codeforces',
    include_package_data=True,
    packages=setuptools.find_packages(),
    license='MIT',
    url='https://github.com/JoshuaTianYangLiu/tcgen',
    scripts=['scripts/tcgen'],
)
