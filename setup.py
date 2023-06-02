import setuptools

setuptools.setup(
    name="prostate-nomograms",
    version="0.0.4",
    author="Maxence Larose",
    author_email="maxence.larose.1@ulaval.ca",
    description="Prediction tools based on existing prostate cancer nomograms.",
    long_description=open('README.md', "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/MaxenceLarose/prostate-nomograms",
    license="Apache License 2.0",
    keywords='cancer medical nomogram prediction prostate python3',
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "lxml",
        "numpy",
        "openpyxl",
        "pandas",
        "requests",
        "scikit-learn",
        "scikit-survival",
        "scipy"
    ],
)
