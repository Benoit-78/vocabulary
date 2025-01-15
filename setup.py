from setuptools import setup, find_packages

setup(
    name='vocabulary',
    version='0.1.0',
    author='ben',
    author_email='delormebenoit211@gmail.com',
    description='Improve your expression level in any foreign language',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        'numpy',
        'pandas',
    ],
    extras_require={
        'dev': [
            'pytest',
            'flake8',
            'black',
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: linux',
    ],
    python_requires='>=3.9',
)
