from setuptools import setup, find_packages

setup(
    name="acfo",
    version="1.0.0",
    packages=["acfo"],
    install_requires=find_packages(),
    author="Douglas Vinícios dos Santos Queiroz",
    author_email="dev.queiroz05@gmail.com",
    description="Adaptive Code Flow Optimizer for Python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/dev-queiroz/acfo",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)