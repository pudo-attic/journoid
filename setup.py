from setuptools import setup, find_packages

setup(
    name='journoid',
    version='0.1',
    description="A journalist android.",
    long_description='',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
        ],
    keywords='data email journalism ddj',
    author='Friedrich Lindenberg',
    author_email='friedrich@pudo.org',
    url='http://pudo.org',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=[],
    include_package_data=False,
    zip_safe=False,
    install_requires=[],
    tests_require=[],
    entry_points=\
    """ """,
)
