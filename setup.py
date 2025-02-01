from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Spatial Autocorrelation Processing'

setup(
    name="spacunhas",
    version=VERSION,
    author="Ahmad Fauzy",
    author_email="ahmadfauzyarif@gmail.com",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/spacunhas",
    license="MIT",
    packages=find_packages(),
    install_requires=['scipy', 'obspy', 'pandas', 'numpy', 'matplotlib'],
    keywords=['geophysics', 'dispersioncurve', 'spac'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Geophysicists",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent", 
    ],
    python_requires='>=3.10',  
)

