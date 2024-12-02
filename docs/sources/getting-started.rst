===============
Getting Started
===============

This is a `PyPI package <https://pypi.org/project/fsrapiclient/>`_, and the source is on `GitHub <https://github.com/sr-murthy/fsrapiclient>`_. Support for the package on Python versions and OSs is summarised in the table below.

======================= ========= ========= ========= =========
\                       *Py 3.10* *Py 3.11* *Py 3.12* *Py 3.13*
======================= ========= ========= ========= =========
*Linux*                 ✅        ✅        ✅        ✅
*Windows*               ✅        ✅        ✅        ✅
*macOS (Intel + Apple)* ✅        ✅        ✅        ✅
======================= ========= ========= ========= =========

It should also be possible to use it on older versions of Python, although this isn't part of CI testing.

.. _getting-started.installation:

Installation
============

A standard :program:`pip` install (with the :code:`-U` "upgrade" option to get the latest version) is sufficient:

.. code:: python

   pip install -U fsrapiclient

This will install `requests <https://requests.readthedocs.io/en/latest/>`_ (and its sub-dependencies), as this is currently the only top-level dependency.

If you are interested in contributing please start with the :doc:`contributing guidelines <contributing>`, otherwise you can jump to the :doc:`usage guide <sources/usage>`, or the :doc:`API reference <sources/api-reference>`.
