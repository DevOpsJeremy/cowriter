"""
Setup script for Cowriter application.
For Windows compatibility and easier installation.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

# Read requirements
requirements_path = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_path.exists():
    requirements = requirements_path.read_text(encoding="utf-8").strip().split('\n')
    requirements = [req.strip() for req in requirements if req.strip() and not req.startswith('#')]

setup(
    name="cowriter",
    version="1.0.0",
    author="DevOpsJeremy",
    author_email="devopsjeremy@example.com",
    description="A modern Python desktop GUI application built with tkinter and Sun Valley theme.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DevOpsJeremy/cowriter",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Desktop Environment",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "cowriter=src.__main__:main",
        ],
        "gui_scripts": [
            "cowriter-gui=src.__main__:main",
        ],
    },
    include_package_data=True,
    package_data={
        "src": ["assets/*"],
    },
)
