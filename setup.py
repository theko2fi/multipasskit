from setuptools import setup, find_packages

setup(
    name='multipasskit',
    version='0.1.0',
    description='A multipass kit containing both an API to remotely manage multipass host and a multipass SDK',
    long_description=open("README.md").read(),
    author='Kenneth KOFFI',
    url='https://github.com/theko2fi/multipasskit',
    packages=find_packages(include=["multipasskit", "multipasskit.*"]),
    install_requires=[
        # Add other dependencies here
    ],
    extras_require={
        "sdk": ["dependency1>=1.0", "dependency2>=2.0"],  # Dependencies for Library SDK
        "api": ["dependency3>=3.0", "dependency4>=4.0"],  # Dependencies for Library API
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.7',
    include_package_data=True,
    project_urls={
        'Documentation': 'https://github.com/theko2fi/multipasskit/wiki',
        'Source': 'https://github.com/theko2fi/multipasskit',
        'Tracker': 'https://github.com/theko2fi/multipasskit/issues',
        'LinkedIn': 'https://www.linkedin.com/in/kenneth-koffi-6b1218178',
    },
)