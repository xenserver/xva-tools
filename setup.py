from setuptools import setup, find_packages

setup(
    name="pyxva",
    version="0.0dev",
    description="Python library/tools to produce XVA files",
    author="Robert Breker, Rob Dobson, Mate Lakat",
    author_email=', '.join([
        "robert.breker@citrix.com",
        "rob.dobson@citrix.com",
        "mate.lakat@citrix.com"]),
    url="http://unspecified.yet",
    packages=find_packages(),
    install_requires=[],
    tests_require=[
        "nose"
    ],
    test_suite='nose.collector',
    entry_points={
        'console_scripts': [
            'mkxva = pyxva.cmd.mkxva:main',
            'xva-update = pyxva.cmd.xvaupdate:main',
        ]
    },
)
