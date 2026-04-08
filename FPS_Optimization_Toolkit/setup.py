from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="fps-optimization-toolkit",
    version="1.0.0",
    author="Your Name",
    description="Windows FPS Optimization Tool for Gaming",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.8",
    install_requires=[
        "wmi>=1.5.1",
        "psutil>=5.9.0",
        "pywin32>=306",
    ],
    entry_points={
        "console_scripts": [
            "fps-toolkit=fps_toolkit:main",
        ],
    },
)
