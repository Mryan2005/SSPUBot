from setuptools import find_packages, setup

setup(
    name="SSPUBot",
    version="0.2",
    author="Mryan2005",
    author_email="A2564011261@qq.com",
    description="It's a bot that can gather the notice and activity of school",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: Mozilla Public License Version 2.0"
    ],
    python_requires=">=3.11",
    url="forum.akiacg.com/u/SSPUBot",
    entry_points={
        'console_scripts': [
            'SSPUBot = SSPUBot.main:run'
        ],
        'commandType': [
            'normal = SSPUBot.main:run',
            'test = SSPUBot.main:run'
        ]
    },
)
