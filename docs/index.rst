============
fsrapiclient
============

A lightweight Python client library and package for the UK `Financial Services Register (FS Register) <https://register.fca.org.uk/s/>`_ `RESTful API <https://register.fca.org.uk/Developer/s/>`_.

The FS Register is a **public** database of all firms, individuals, funds, and other entities, that are either currently, or have been previously, authorised and/or regulated by the UK `Financial Conduct Authority (FCA) <https://www.fca.org.uk>`__ and/or the `Prudential Regulation Authority (PRA) <http://bankofengland.co.uk/pra>`__.

.. note::

   The FS Register API is free to use but accessing it, including via this library, requires
   `registration <https://register.fca.org.uk/Developer/ShAPI_LoginPage?ec=302&startURL=%2FDeveloper%2Fs%2F#>`_. Registration involves a free sign up with an email, which is used as the API username in requests, and basic personal information. Once registered an API key is available from your registration profile - the API key can be used in request headers to programmatically make requests via any suitable language and library of choice.

To learn more about the FS Register API structure please consult the `official documentation <https://register.fca.org.uk/Developer/s/>`_, or start :doc:`here <sources/fs-register-api>`.

To get started with this package you can start :doc:`here <sources/getting-started>`.

If you're interested in contributing please consult the :doc:`contributing guidelines <sources/contributing>`.

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   sources/fs-register-api
   sources/getting-started
   sources/usage
   sources/contributing
   sources/api-reference

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
