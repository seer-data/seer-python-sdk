import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='seer_python_sdk',
    version='0.1',
    author="Adam Peaston",
    author_email="adam.peaston@seerdata.com.au",
    description="Seer python SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/seer-data/seer-python-sdk.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Private :: Seer public API",
        "Operating System :: OS Independent",
    ],
)
