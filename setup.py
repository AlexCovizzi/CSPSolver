from setuptools import setup, find_packages
from platform import architecture

python_arch = platform.architecture()[0]

requirements_32 = [
    # pycairo
    'pycairo; platform_system!="Windows"',
    # pycairo Windows 3.5
    'pycairo @ https://download.lfd.uci.edu/pythonlibs/r5uhg2lo/pycairo-1.18.0-cp35-cp35m-win32.whl ;python_version=="3.5" and platform_system=="Windows"',
    # pycairo Windows 3.6
    'pycairo @ https://download.lfd.uci.edu/pythonlibs/r5uhg2lo/pycairo-1.18.0-cp36-cp36m-win32.whl ;python_version=="3.6" and platform_system=="Windows"',
    # pycairo Windows 3.7
    'pycairo @ https://download.lfd.uci.edu/pythonlibs/r5uhg2lo/pycairo-1.18.0-cp37-cp37m-win32.whl ;python_version>="3.7" and platform_system=="Windows"',
    # python-igraph
    'python-igraph; platform_system!="Windows"',
    # python-igraph Windows 3.5
    'python-igraph @ https://download.lfd.uci.edu/pythonlibs/r5uhg2lo/python_igraph-0.7.1.post6-cp35-cp35m-win32.whl ;python_version=="3.5" and platform_system=="Windows"',
    # python-igraph Windows 3.6
    'python-igraph @ https://download.lfd.uci.edu/pythonlibs/r5uhg2lo/python_igraph-0.7.1.post6-cp36-cp36m-win32.whl ;python_version=="3.6" and platform_system=="Windows"',
    # python-igraph Windows 3.7
    'python-igraph @ https://download.lfd.uci.edu/pythonlibs/r5uhg2lo/python_igraph-0.7.1.post6-cp37-cp37m-win32.whl ;python_version>="3.7" and platform_system=="Windows"'
]

requirements_64 = [
    # pycairo
    'pycairo; platform_system!="Windows"',
    # pycairo Windows 3.5
    'pycairo @ https://download.lfd.uci.edu/pythonlibs/r5uhg2lo/pycairo-1.18.0-cp35-cp35m-win_amd64.whl ;python_version=="3.5" and platform_system=="Windows"',
    # pycairo Windows 3.6
    'pycairo @ https://download.lfd.uci.edu/pythonlibs/r5uhg2lo/pycairo-1.18.0-cp36-cp36m-win_amd64.whl ;python_version=="3.6" and platform_system=="Windows"',
    # pycairo Windows 3.7
    'pycairo @ https://download.lfd.uci.edu/pythonlibs/r5uhg2lo/pycairo-1.18.0-cp37-cp37m-win_amd64.whl ;python_version>="3.7" and platform_system=="Windows"',
    # python-igraph
    'python-igraph; platform_system!="Windows"',
    # python-igraph Windows 3.5
    'python-igraph @ https://download.lfd.uci.edu/pythonlibs/r5uhg2lo/python_igraph-0.7.1.post6-cp35-cp35m-win_amd64.whl ;python_version=="3.5" and platform_system=="Windows"',
    # python-igraph Windows 3.6
    'python-igraph @ https://download.lfd.uci.edu/pythonlibs/r5uhg2lo/python_igraph-0.7.1.post6-cp36-cp36m-win_amd64.whl ;python_version=="3.6" and platform_system=="Windows"',
    # python-igraph Windows 3.7
    'python-igraph @ https://download.lfd.uci.edu/pythonlibs/r5uhg2lo/python_igraph-0.7.1.post6-cp37-cp37m-win_amd64.whl ;python_version>="3.7" and platform_system=="Windows"'
]

setup(
    name='cspsolver',
    version='1.0',
    python_requires='>=3.5',
    packages=find_packages(),
    install_requires = requirements_32 if python_arch=="32bit" else requirements_64,
    extras_require={
        'dev': [
            'jedi',
            'mypy'
        ]
    }
)
