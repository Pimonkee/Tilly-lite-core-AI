"""
Tilly AI - Setup Configuration
"""
from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# Read requirements
requirements = []
try:
    with open('requirements.txt') as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
except FileNotFoundError:
    pass

setup(
    name="tilly-ai",
    version="1.0.0",
    author="Tilly AI Contributors",
    author_email="support@tilly-ai.example",
    description="An empathetic AI companion focused on mental wellness",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Pimonkee/Tilly-lite-core-AI",
    project_urls={
        "Bug Tracker": "https://github.com/Pimonkee/Tilly-lite-core-AI/issues",
        "Documentation": "https://github.com/Pimonkee/Tilly-lite-core-AI/blob/main/README.md",
        "Source Code": "https://github.com/Pimonkee/Tilly-lite-core-AI",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Healthcare Industry",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Human Machine Interfaces",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-asyncio>=0.21.1",
            "pytest-cov>=4.1.0",
            "black>=23.12.1",
            "flake8>=6.1.0",
            "mypy>=1.7.1",
            "isort>=5.13.2",
        ],
        "ocr": [
            "pytesseract>=0.3.10",
            "Pillow>=10.1.0",
            "chromadb>=0.4.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "tilly=tilly.api.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.json", "*.yaml", "*.yml"],
    },
)
