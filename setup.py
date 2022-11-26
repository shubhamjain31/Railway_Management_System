import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()
# with open(os.path.join(here, 'CHANGES.txt')) as f:
#     CHANGES = f.read()

requires = [
    'setuptools',
    'pyramid',
    'plaster_pastedeploy',
    'pyramid-ipython',
    'pyramid_jinja2',
    'sqlalchemy',
    'psycopg2-binary',
    'pyramid_tm',
    'transaction',
    'zope.sqlalchemy',
    'pyramid_debugtoolbar',
    'pyramid_exclog',
    'cryptacular',
    'waitress',
    'bcrypt',
    'wtforms',
    'python-slugify'
]

tests_require = [
    'WebTest',
    'pytest',
    'pytest-cov',
]

setup(
    name='core',
    version='0.0',
    description='core',
    long_description=README + '\n\n',
    # long_description=README + '\n\n' + CHANGES,
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Pyramid',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    author='',
    author_email='',
    url='',
    keywords='web pyramid pylons',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    extras_require={
        'testing': tests_require,
    },
    install_requires=requires,
    entry_points={
        'paste.app_factory': [
            'main = core:main',
        ],
        'console_scripts': [
            'initdb = core.scripts.initializedb:main',
        ],
    },
)   