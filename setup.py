from setuptools import setup, find_packages


# Function to read the contents of the requirements file
def read_requirements():
    with open('requirements.txt', 'r') as req:
        # Exclude any comments or empty lines
        return [line.strip() for line in req if line.strip() and not line.startswith('#')]


# Call the function and store the requirements list
install_requires = read_requirements()

setup(
    name='gemini_investing_agent',
    version='0.0.1',
    packages=find_packages(exclude=[".env*", "sa.json"]),
    description='Agent For Investing via Alpaca',
    long_description_content_type='text/markdown',
    long_description=open('README.md').read(),
    author='Viacheslav Kovalevskyi',
    author_email='viacheslav@kovalevskyi.com',
    license='MIT',
    install_requires=install_requires
)