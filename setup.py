from setuptools import setup

setup(
    name="networksdb",
    version="1.0.2",
    description="Official Python library for NetworksDB.io",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/networksdb/networksdb-python",
    author="NetworksDB",
    author_email="contact@networksdb.io",
    license="Apache License 2.0",
    packages=["networksdb"],
    install_requires=["requests", "attrdict"],
    include_package_data=True,
    zip_safe=False,
)
