from setuptools import setup, find_packages
from platform import architecture, system

platform_system = system()
python_arch = architecture()[0]

requirements = []

if platform_system != 'Windows':
    requirements.append('pycairo; platform_system!="Windows"')
    requirements.append('python-igraph; platform_system!="Windows"')
else:
    if python_arch == '32bit':
        requirements.extend([
            # pycairo Windows 3.6
            'pycairo @ https://download.lfd.uci.edu/pythonlibs/r5uhg2lo/pycairo-1.18.0-cp36-cp36m-win32.whl ;python_version=="3.6" and platform_system=="Windows"',
            # pycairo Windows 3.7
            'pycairo @ https://download.lfd.uci.edu/pythonlibs/r5uhg2lo/pycairo-1.18.0-cp37-cp37m-win32.whl ;python_version>="3.7" and platform_system=="Windows"',
            # python-igraph Windows 3.6
            'python-igraph @ https://download.lfd.uci.edu/pythonlibs/r5uhg2lo/python_igraph-0.7.1.post6-cp36-cp36m-win32.whl ;python_version=="3.6" and platform_system=="Windows"',
            # python-igraph Windows 3.7
            'python-igraph @ https://download.lfd.uci.edu/pythonlibs/r5uhg2lo/python_igraph-0.7.1.post6-cp37-cp37m-win32.whl ;python_version>="3.7" and platform_system=="Windows"'
        ])
    else:
        requirements.extend([
            # pycairo Windows 3.6
            'pycairo @ https://download.lfd.uci.edu/pythonlibs/r5uhg2lo/pycairo-1.18.0-cp36-cp36m-win_amd64.whl ;python_version=="3.6" and platform_system=="Windows"',
            # pycairo Windows 3.7
            'pycairo @ https://download.lfd.uci.edu/pythonlibs/r5uhg2lo/pycairo-1.18.0-cp37-cp37m-win_amd64.whl ;python_version>="3.7" and platform_system=="Windows"',
            # python-igraph Windows 3.6
            'python-igraph @ https://download.lfd.uci.edu/pythonlibs/r5uhg2lo/python_igraph-0.7.1.post6-cp36-cp36m-win_amd64.whl ;python_version=="3.6" and platform_system=="Windows"',
            # python-igraph Windows 3.7
            'python-igraph @ https://download.lfd.uci.edu/pythonlibs/r5uhg2lo/python_igraph-0.7.1.post6-cp37-cp37m-win_amd64.whl ;python_version>="3.7" and platform_system=="Windows"'
        ])

setup(
    name='cspsolver',
    version='1.0',
    python_requires='>=3.6',
    packages=find_packages(),
    install_requires = requirements,
    extras_require={
        'dev': [
            'jedi',
            'mypy'
        ]
    }
)
