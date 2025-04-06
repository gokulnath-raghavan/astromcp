from setuptools import setup, find_packages

setup(
    name="astro_mcp",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.21.0",
        "pandas>=1.3.0",
        "pyswisseph>=2.10.0",
        "fastapi>=0.68.0",
        "uvicorn>=0.15.0",
        "pydantic>=1.8.0",
        "python-jose>=3.3.0",
        "passlib>=1.7.4",
        "python-multipart>=0.0.5",
        "streamlit>=1.0.0",
        "pytest>=6.2.5",
        "python-dotenv>=0.19.0"
    ],
    python_requires=">=3.8",
) 