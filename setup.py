from setuptools import setup

setup(
    name='cspsolver',
    version='1.0',
    python_requires='>=3.6',
    install_requires=[
        'pycairo; platform_system=="Linux"',
        'pycairo @ https://download.lfd.uci.edu/pythonlibs/r5uhg2lo/pycairo-1.18.0-cp36-cp36m-win_amd64.whl ;python_version<"3.7" and platform_system=="Windows" and platform_machine=="AMD64"',
        'pycairo @ https://download.lfd.uci.edu/pythonlibs/r5uhg2lo/pycairo-1.18.0-cp37-cp37m-win_amd64.whl ;python_version>="3.7" and platform_system=="Windows" and platform_machine=="AMD64"',
        'pycairo @ https://download.lfd.uci.edu/pythonlibs/r5uhg2lo/pycairo-1.18.0-cp36-cp36m-win32.whl ;python_version<"3.7" and platform_system=="Windows" and platform_machine=="x86_64"',
        'pycairo @ https://download.lfd.uci.edu/pythonlibs/r5uhg2lo/pycairo-1.18.0-cp37-cp37m-win32.whl ;python_version>="3.7" and platform_system=="Windows" and platform_machine=="x86_64"',
        'python-igraph; platform_system=="Linux"',
        'python-igraph @ https://download.lfd.uci.edu/pythonlibs/r5uhg2lo/python_igraph-0.7.1.post6-cp36-cp36m-win_amd64.whl ;python_version<"3.7" and platform_system=="Windows" and platform_machine=="AMD64"',
        'python-igraph @ https://download.lfd.uci.edu/pythonlibs/r5uhg2lo/python_igraph-0.7.1.post6-cp37-cp37m-win_amd64.whl ;python_version>="3.7" and platform_system=="Windows" and platform_machine=="AMD64"',
        'python-igraph @ https://download.lfd.uci.edu/pythonlibs/r5uhg2lo/python_igraph-0.7.1.post6-cp36-cp36m-win32.whl ;python_version<"3.7" and platform_system=="Windows" and platform_machine=="x86_64"',
        'python-igraph @ https://download.lfd.uci.edu/pythonlibs/r5uhg2lo/python_igraph-0.7.1.post6-cp37-cp37m-win32.whl ;python_version>="3.7" and platform_system=="Windows" and platform_machine=="x86_64"'
    ],
    extras_require={
        'dev': [
            'jedi',
            'mypy'
        ]
    }
)