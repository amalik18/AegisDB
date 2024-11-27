from setuptools import setup, find_packages

# Read the contents of your README file
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='aegis_db',
    version='0.0.1',
    author='Ali Malik',
    author_email='ali_malik96@example.com',
    description='A NoSQL database that supports fully homomorphic encryption.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/amalik18/homomorphic_nosql_database',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'concrete',
        'numpy',
        'pygraphviz',
    ],
    entry_points={
        'console_scripts': [
            # 'main=aegis_db.main:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.12.3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Database',
        'Topic :: Security :: Cryptography',
    ],
    python_requires='>=3.10',
)
