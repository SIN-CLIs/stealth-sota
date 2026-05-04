from setuptools import setup, find_packages

setup(
    name="stealth-sota",
    version="1.0.0",
    packages=find_packages(),
    install_requires=["psutil"],
    extras_require={
        "all": ["psutil", "prometheus_client", "stealth-axiom"],
        "test": ["pytest>=8.0", "stealth-axiom"],
    },
    python_requires=">=3.10",
)
