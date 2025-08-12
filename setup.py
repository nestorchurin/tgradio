"""
Setup script for Telegram Radio Bot
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="telegram-radio-bot",
    version="1.0.0",
    author="nestor_churin",
    description="Автоматичний радіо бот для Telegram з підтримкою музики, джинглів та реклами",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nestorchurin/tgradio",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Communications :: Chat",
        "Topic :: Multimedia :: Sound/Audio :: Players",
    ],
    python_requires=">=3.11",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.4",
            "pytest-asyncio>=0.21.1",
            "flake8>=6.1.0",
            "black>=23.12.1",
            "isort>=5.13.2",
            "mypy>=1.8.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "telegram-radio-bot=main:main",
        ],
    },
)
