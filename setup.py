from setuptools import setup, find_packages

setup(
    name="requirements_generation",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "streamlit",
        "openai",
        "pandas",
        "xlsxwriter",
        "streamlit-image-coordinates",
        "sys",
        "IO",
        "subprocess",
        "streamlit-image-zoom",
        "Pillow",
        "json",
        "streamlit-drawable-canvas",
        "matplotlib", 
        "networkx",
        "graphviz",
    ],
    entry_points={
        "console_scripts": [
            "run-requirements-app=main:main",
        ],
    },
)