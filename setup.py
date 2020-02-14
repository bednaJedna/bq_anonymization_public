from sys import platform

from setuptools import find_packages, setup

if platform.startswith("win32"):
    setup(
        packages=find_packages(),
        install_requires=[
            "behave",
            "pyhamcrest",
            "google-cloud-bigquery",
            "google",
            "protobuf",
            # on windows comment out pandas and install it manually from here:
            # https://www.lfd.uci.edu/~gohlke/pythonlibs/#pandas
            # "pandas",
            "openpyxl",
            "tqdm",
            "allure-behave",
        ],
    )

elif platform.startswith("linux"):
    setup(
        packages=find_packages(),
        install_requires=[
            "behave",
            "pyhamcrest",
            "google-cloud-bigquery",
            "google",
            "protobuf",
            "pandas",
            "openpyxl",
            "tqdm",
            "allure-behave",
        ],
    )

else:
    raise OSError(
        f"This setup works for 'linux' and 'win32' platforms only.\nYour platform is {platform}"
    )
