from setuptools import setup, find_packages

setup(
    author="Kek",
    name="tcgen",
    packages=find_packages(exclude=["examples"]),
    entry_points='''
        [console_scripts]
        tcgen=tcgen.cli:cli
    ''',
)