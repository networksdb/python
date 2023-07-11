from setuptools import setup

setup(
    name="networksdb",
    version="2.0.0",
    descriptin="Official Python library for NetworksDB.io",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://networksdb.io",
    author="NetworksDB",
    author_email="contact@networksdb.io",
    license="Apache License 2.0",
    packages=["networksdb"],
    install_requires=["requests"],
    include_package_data=True,
    zip_safe=False,
)
