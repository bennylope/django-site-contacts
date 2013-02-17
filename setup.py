from setuptools import setup
import os


setup(
    author="Ben Lopatin",
    author_email="ben.lopatin@wellfireinteractive.com",
    name='django-site-contacts',
    version='0.0.1',
    description='Contact form recipients management for Django sites',
    long_description=open(os.path.join(os.path.dirname(__file__),
        'README.rst')).read(),
    url='https://github.com/bennylope/django-site-contacts/',
    license='BSD License',
    platforms=['OS Independent'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    install_requires=[
        'Django',
    ],
    include_package_data=True,
    zip_safe=False
)
