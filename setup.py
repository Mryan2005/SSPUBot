from setuptools import find_packages, setup

setup(
    name="SSPU Bot",
    version="0.1",
    author="Mryan2005",
    author_email="A2564011261@qq.com",
    description="It's a bot that can gather the notice and activity of school",
    packages=["package_name"],
    install_requires=[
        "seleniumwire",
        "pickle",
        "selenium",
        "urllib"
    ],
    package=find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: Mozilla Public License Version 2.0"
    ],
    python_requires=">=3.11",
    url="forum.akiacg.com/u/SSPUBot"
)
