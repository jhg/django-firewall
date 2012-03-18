from setuptools import setup

setup(
    name = "django-firewall",
    version = __import__("django_firewall").__version__,
    author = "Thomas Randle",
    author_email = "thomas@tasgn.com",
    description = "A Django reusable app to help with application access control",
    long_description = open("README.txt").read(),
    url = "http://github.com/Rundll/django-firewall",
    license = "BSD",
    packages = [
        "django_firewall",
    ],
    classifiers = [
        "Development Status :: 1 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Utilities",
        "Framework :: Django",
    ]
)