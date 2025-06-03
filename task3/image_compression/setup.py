from setuptools import setup, find_packages

setup(
    name="image_compression",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'numpy=1.26.4',
        'opencv-python>=4.5',
        'matplotlib>=3.10'
    ],
)