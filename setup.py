import setuptools

requirements = [
    'Click>=6.0',
    'boto3>=1.3.1'
]

setuptools.setup(
    name="cfn-tools",
    version="0.1.4",
    url="https://github.com/boroivanov/cfn-tools",

    author="Borislav Ivanov",
    author_email="borogl@gmail.com",

    description="Tools for AWS CloudFormation",
    long_description=open('README.rst').read(),

    packages=[
        'cfntools',
    ],
    package_dir={'cfntools':
                 'cfntools'},
    entry_points={
        'console_scripts': [
            'cfn-tools=cfntools.cli:main'
        ]
    },

    install_requires=requirements,
    license="MIT license",

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
)
