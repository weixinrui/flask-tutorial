from setuptools import setup
from setuptools import find_packages

setup(
    name = "flaskr",
    version = "1.0.0",
    description="The basic blog app built in the Flask tutorial.",
    author="weixinrui",
    author_email="weixinruiyuanban@gmail.com",
    packages = find_packages(),
    install_requires = ["flask"]
)