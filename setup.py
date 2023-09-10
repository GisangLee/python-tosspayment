import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='python-tosspayments',
    version='0.0.7',
    description='Toss Payments SDK for python',
    author='jsonlee',
    author_email='dudegs.py@gmail.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/GisangLee/python-tosspayment',
    license="MIT",
    install_requires=["requests"],
    keywords=['toss', 'toss payment', 'payment'],
    python_requires='>=3.8',
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
)