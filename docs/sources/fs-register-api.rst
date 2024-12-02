=================================
Understanding the FS Register API
=================================

The package functionality reflects the current version (``V0.1``) of the FS Register API. There is `API documentation <https://register.fca.org.uk/Developer/s/>`__ but access requires `registration <https://register.fca.org.uk/Developer/ShAPI_LoginPage?ec=302&startURL=%2FDeveloper%2Fs%2F#>`_.

The base URL for all API requests is:

.. code:: shell

   https://register.fca.org.uk/services/V0.1

.. _fs-register-api.resources-and-request-types:

Resources and Request Types
===========================

There are three main categories of resource about which information can be requested from the register via API endpoints:

- **firms** - authorised and/or regulated firms (either current or past), or providing regulated products or services
- **individuals** - individuals associated with the type of firms described above, either current or past
- **funds** - investment funds or collective investment schemes (CIS),including subfunds of funds

There is also a **common search** API endpoint that allows a search for any of these resources by a name substring and a corresponding type specification (firm, individual, or fund).

.. _fs-register-api.request-headers:

Request Headers
---------------

The FS Register API is read-only - all requests must use ``GET``, and include headers containing the API username and key:

.. code:: shell

   ACCEPT: application/json
   X-AUTH-EMAIL: <signup email / API username>
   X-AUTH-KEY: <API key>

.. _fs-register-api.rate-limiting:

Rate Limiting
-------------

According to the `API documentation <https://register.fca.org.uk/Developer/s/>`__ **rate limiting** is applied to set a **maximum of 50 requests per 10 seconds per user**, and **breaches** lead to `(HTTP 429) errors <https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429>`__ and **requests being blocked for 1 minute**.

.. warning::

   Please use the API and this library responsibly, and do not make excessive requests or use it in an otherwise inappropriate way.

.. _fs-register-api.firm-requests:

Firm Requests
-------------

Firms are identified by unique firm reference numbers (FRN). The following is a table summarising firm-specific API endpoints:

+-----------------------------------+------------------------+---------+
| API endpoint                      | Parameters             | Request |
|                                   |                        | Method  |
+===================================+========================+=========+
| ``/V0.1/Firm/{FRN}``              | FRN (str)              | GET     |
+-----------------------------------+------------------------+---------+
| ``/V0.1/Firm/{FRN}/Address``      | FRN (str)              | GET     |
+-----------------------------------+------------------------+---------+
| ``/V0.1/Firm/{FRN}/AR``           | FRN (str)              | GET     |
+-----------------------------------+------------------------+---------+
| ``/V0.1/Firm/{FRN}/CF``           | FRN (str)              | GET     |
+-----------------------------------+------------------------+---------+
| ``/V0.1                           | FRN (str)              | GET     |
| /Firm/{FRN}/DisciplinaryHistory`` |                        |         |
+-----------------------------------+------------------------+---------+
| ``/V0.1/Firm/{FRN}/Exclusions``   | FRN (str)              | GET     |
+-----------------------------------+------------------------+---------+
| ``/V0.1/Firm/{FRN}/Individuals``  | FRN (str)              | GET     |
+-----------------------------------+------------------------+---------+
| ``/V0.1/Firm/{FRN}/Names``        | FRN (str)              | GET     |
+-----------------------------------+------------------------+---------+
| ``/V0.1/Firm/{FRN}/Passports``    | FRN (str)              | GET     |
+-----------------------------------+------------------------+---------+
| ``/V0.1/Firm/{FRN}                | FRN (str), Country     | GET     |
| /Passports/{Country}/Permission`` | (str)                  |         |
+-----------------------------------+------------------------+---------+
| ``/V0.1/Firm/{FRN}/Permissions``  | FRN (str)              | GET     |
+-----------------------------------+------------------------+---------+
| ``/V0.1/Firm/{FRN}/Regulators``   | FRN (str)              | GET     |
+-----------------------------------+------------------------+---------+
| ``/V0.1/Firm/{FRN}/Requirements`` | FRN (str)              | GET     |
+-----------------------------------+------------------------+---------+
| ``/V0.1/Firm/{FRN}/Requir         | FRN (str), Requirement | GET     |
| ements/{ReqRef}/InvestmentTypes`` | Reference (str)        |         |
+-----------------------------------+------------------------+---------+
| ``/V0.1/Firm/{FRN}/Waiver``       | FRN (str)              | GET     |
+-----------------------------------+------------------------+---------+

.. note::

   The abbreviations “CF” and “AR” refer to “controlled functions” and “appointed representatives” respectively.

.. _fs-register-api.individual-requests:

Individual Requests
-------------------

Individuals associated with firms are identified by unique individual reference numbers (IRN). and the following is a table summarising individual-specific API endpoints.

+-------------------------------------------------+------------+----------------+
| API endpoint                                    | Parameters | Request Method |
+=================================================+============+================+
| ``/V0.1/Individuals/{IRN}``                     | IRN (str)  | GET            |
+-------------------------------------------------+------------+----------------+
| ``/V0.1/Individuals/{IRN}/CF``                  | IRN (str)  | GET            |
+-------------------------------------------------+------------+----------------+
| ``/V0.1/Individuals/{IRN}/DisciplinaryHistory`` | IRN (str)  | GET            |
+-------------------------------------------------+------------+----------------+

.. note::

   The abbreviation “CF” refers to “controlled functions”.

.. _fs-register-api.fund-requests:

Fund Requests
-------------

Funds are identified by unique product reference numbers (PRN). The following is a table summarising fund-specific API endpoints:

=========================== ========== ==============
API endpoint                Parameters Request Method
=========================== ========== ==============
``/V0.1/CIS/{PRN}``         PRN (str)  GET
``/V0.1/CIS/{PRN}/Names``   PRN (str)  GET
``/V0.1/CIS/{PRN}/Subfund`` PRN (str)  GET
=========================== ========== ==============

.. _fs-register-api.common-search-requests:

Common Search Requests
----------------------

The common search API endpoint has the following request structure:

.. code:: http

   GET https://register.fca.org.uk/services/V0.1/CommonSearch?q=query&type=type HTTP/1.1

where ``query`` is a value of the parameter ``'q'`` and should be substring of the name of a firm, individual or fund, of interest, and ``type`` is the value of the parameter ``'type'`` and should be one of ``'firm'``, ``'individual'``, ``'fund'``. For example, here are a few valid common search requests.

* Common search for Barclays Bank Plc (FRN #122702):

.. code:: http

   GET https://register.fca.org.uk/services/V0.1/CommonSearch?q=Barclays+Bank+plc&type=firm HTTP/1.1

* Common search for Hastings Insurance Services Limited (FRN #311492)

.. code:: http
   
   GET https://register.fca.org.uk/services/V0.1/CommonSearch?q=hastings+insurance+services&type=firm HTTP/1.1

* Common search for all Natwest-related firms:

.. code:: http
   
   GET https://register.fca.org.uk/services/V0.1/CommonSearch?q=Natwest&type=firm HTTP/1.1

* Common search for a specific individual, Mark Carney (IRN #MXC29012):

.. code:: http
   
   GET https://register.fca.org.uk/services/V0.1/CommonSearch?q=mark+carney&type=individual HTTP/1.1

* Common search for a generic individual name "John Smith", with multiple results:

.. code:: http
   
   GET https://register.fca.org.uk/services/V0.1/CommonSearch?q=John+Smith&type=individual HTTP/1.1

* Common search for a specific fund, Jupiter Asia Pacific Income (PRN #635641):

.. code:: http
   
   GET https://register.fca.org.uk/services/V0.1/CommonSearch?q=jupiter+asia+pacific+income&type=fund HTTP/1.1

* Common search for a specific fund, abrdn Multi-Asset Fund (PRN #637980):

.. code:: http
   
   GET https://register.fca.org.uk/services/V0.1/CommonSearch?q=abrdn+multi-asset+fund&type=fund HTTP/1.1
