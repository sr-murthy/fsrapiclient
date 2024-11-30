<div align="center">
  
[![CI](https://github.com/sr-murthy/fsrapiclient/actions/workflows/ci.yml/badge.svg)](https://github.com/sr-murthy/fsrapiclient/actions/workflows/ci.yml)
[![CodeQL](https://github.com/sr-murthy/fsrapiclient/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/sr-murthy/fsrapiclient/actions/workflows/codeql-analysis.yml)
[![codecov](https://codecov.io/github/sr-murthy/fsrapiclient/graph/badge.svg?token=F41VZIHT2K)](https://codecov.io/github/sr-murthy/fsrapiclient)
[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm-project.org)
[![License: MPL
2.0](https://img.shields.io/badge/License-MPL_2.0-brightgreen.svg)](https://opensource.org/licenses/MPL-2.0)

</div>

# fsrapiclient

A lightweight Python client library for the [UK Financial Services Register (FS Register)](https://register.fca.org.uk/s/) [RESTful API](https://register.fca.org.uk/Developer/s/).

The FS Register is a **public** database of all firms, individuals and other entities that are currently, or have been previously, authorised by the [UK Financial Conduct Authority (FCA)](https://www.fca.org.uk) and/or the [Prudential Regulatory Authority (PRA)](http://bankofengland.co.uk/pra).

**NOTE #1:** The FS Register API is free to use but accessing it, including via this library, requires [registration](https://register.fca.org.uk/Developer/ShAPI_LoginPage?ec=302&startURL=%2FDeveloper%2Fs%2F#). Registration involves signing up with an email, which is used as the API username in requests, and some personal information. Once registered an API key is available from your registration profile - the API key can be used in request headers to programmatically make requests via any suitable language and library of choice.

**NOTE #2:** The author has no current or previous affiliation with either the FCA or PRA.

# The FS Register API

The `fsrapiclient` functionality reflects the structure and properties of the current FS Register API (V0.1). There are three main categories of resource about which information can be requested from the register via API endpoints:

* **firms** - authorised firms (either currently or previously authorised)
* **individuals** - individuals associated or affiliated with authorised firms, either currently or previously
* **funds** - funds or collective investment schemes (CIS), including subfunds of funds

There is also a **common search** API endpoint that allows a search for any of these resources by name or namelike-substring and a corresponding type specification (firm, individual, or fund).

These are described in a bit more detail below.

## Firms

Firms are identified by unique firm reference numbers (FRN). The following is a table summarising firm-specific API endpoints:

| API endpoint                                             | Parameters                             |
|----------------------------------------------------------|----------------------------------------|
| `/V0.1/Firm/{FRN}`                                       | FRN (str)                              |
| `/V0.1/Firm/{FRN}/Address`                               | FRN (str)                              |
| `/V0.1/Firm/{FRN}/AR`                                    | FRN (str)                              |
| `/V0.1/Firm/{FRN}/CF`                                    | FRN (str)                              |
| `/V0.1/Firm/{FRN}/DisciplinaryHistory`                   | FRN (str)                              |
| `/V0.1/Firm/{FRN}/Exclusions`                            | FRN (str)                              |
| `/V0.1/Firm/{FRN}/Individuals`                           | FRN (str)                              |
| `/V0.1/Firm/{FRN}/Names`                                 | FRN (str)                              |
| `/V0.1/Firm/{FRN}/Passports`                             | FRN (str)                              |
| `/V0.1/Firm/{FRN}/Passports/{Country}/Permission`        | FRN (str), Country (str)               |
| `/V0.1/Firm/{FRN}/Permissions`                           | FRN (str)                              |
| `/V0.1/Firm/{FRN}/Regulators`                            | FRN (str)                              |
| `/V0.1/Firm/{FRN}/Requirements`                          | FRN (str)                              |
| `/V0.1/Firm/{FRN}/Requirements/{ReqRef}/InvestmentTypes` | FRN (str), Requirement Reference (str) |
| `/V0.1/Firm/{FRN}/Waiver`                                | FRN (str)                              |

**NOTE:** The abbreviations "CF" and "AR" refer to "controlled functions" and "appointed representatives" respectively.

## Individuals

Individuals associated with firms are identified by unique individual reference numbers (IRN). and the following is a table summarising individual-specific API endpoints.

| API endpoint                                  | Parameters |
|-----------------------------------------------|------------|
| `/V0.1/Individuals/{IRN}`                     | IRN (str)  |
| `/V0.1/Individuals/{IRN}/CF`                  | IRN (str)  |
| `/V0.1/Individuals/{IRN}/DisciplinaryHistory` | IRN (str)  |

**NOTE:** The abbreviation "CF" refers to "controlled functions".

## Funds

Funds are identified by unique product reference numbers (PRN). The following is a table summarising fund-specific API endpoints:

| API endpoint              | Parameters |
|---------------------------|------------|
| `/V0.1/CIS/{PRN}`         | PRN (str)  |
| `/V0.1/CIS/{PRN}/Names`   | PRN (str)  |
| `/V0.1/CIS/{PRN}/Subfund` | PRN (str)  |

## Common Search

The common search API endpoint has the following structure:
```http
/V0.1/CommonSearch?q=<query>&type=<entity type>
```
where `<query>` is a substring of the name of a firm, individual or fund, of interest, and `<entity type>` should indicate whether the query refers to a firm (`"firm"`), individual (`"individual"`), or fund (`"fund"`). For example, here are a few valid common search requests:
```http
/V0.1/CommonSearch?q=Barclays+Bank+plc&type=firm
/V0.1/CommonSearch?q=Hastings+Direct&type=firm
/V0.1/CommonSearch?q=Natwest&type=firm
/V0.1/CommonSearch?q=Mark+Carney&type=individual
/V0.1/CommonSearch?q=John+Smith&type=individual
/V0.1/CommonSearch?q=Jupiter+Asia+Pacific+Income&type=fund
/V0.1/CommonSearch?q=abrdn+multi-asset+fund&type=fund
```

# Getting Started

Currently, `fsrapiclient` only uses the [`requests`](https://requests.readthedocs.io/en/latest/) library (and its dependencies). All you need to get started is a simple `pip install`:
```bash
pip install fsrapiclient
```
which will install all the dependencies.

Note that you first need to [register](https://register.fca.org.uk/Developer/ShAPI_LoginPage?ec=302&startURL=%2FDeveloper%2Fs%2F#) with the FS Register, and get your API key.

If you're interested in contributing see the [contributions guidelines](CONTRIBUTING.md).

# Usage

Import the FS Register client `fsrapiclient.api.FsrApiClient`, and create an instance using the signup email, which is the API username, and the API key:
```python
>>> from fsrapiclient.api import FsrApiClient
>>> client = FsrApiClient(<signup email>, <API key>)
>>> client
<fsrapiclient.api.FsrApiClient at 0x113c10800>
```

Each client instance maintains its own API session (`fsrapiclient.api.FsrApiSession`) state:
```python
>>> client.api_session
<fsrapiclient.api.FsrApiSession at 0x113392060>
```
storing the API username (signup email) and API key. These, and also the API version, are available as properties:
```python
>>> client.api_session.api_username
<signup email>
>>> client.api_session.api_key
<API key>
>>> client.api_version
V0.1
```

Almost client methods return an `fsrapiclient.api.FsrApiResponse` object, which has four properties specific to the FS Register API:

* `fsr_status` - an FS Register-specific status indicator for the request
* `fsr_message` - an FS Register-specific status message for the request
* `fsr_data` - the response data
* `fsr_resultinfo` - pagination information for the response data

## Common Search

The common search endpoint can be used via the `FsrApiClient.common_search` method to make generic queries for firms, individuals, or funds. It requires an URL-encoded string of the form:
```bash
q=<query string>&type=<entity type>
```
Use [`urlencode.parse.urlencode`](https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urlencode) to do the URL-encoding. Some examples are given below.
```python
from urllib.parse import urlencode
>>> client.common_search(urlencode({'q': 'barclays bank', 'type': 'firm'})).fsr_data
[{'URL': 'https://register.fca.org.uk/services/V0.1/Firm/759676',
  'Status': 'Authorised',
  'Reference Number': '759676',
  'Type of business or Individual': 'Firm',
  'Name': 'Barclays Bank UK PLC (Postcode: E14 5HP)'},
 ...
{'URL': 'https://register.fca.org.uk/services/V0.1/Firm/122702',
 'Status': 'Authorised',
 'Reference Number': '122702',
 'Type of business or Individual': 'Firm',
 'Name': 'Barclays Bank Plc (Postcode: E14 5HP)'}]
>>> client.common_search(urlencode({'q': 'mark carney', 'type': 'individual'})).fsr_data
[{'URL': 'https://register.fca.org.uk/services/V0.1/Individuals/MXC29012',
  'Status': 'Active',
  'Reference Number': 'MXC29012',
  'Type of business or Individual': 'Individual',
  'Name': 'Mark Carney'}] 
>>> client.common_search(urlencode({'q': 'jupiter asia pacific income', 'type': 'fund'}))
[{'URL': 'https://register.fca.org.uk/services/V0.1/CIS/635641',
  'Status': 'Recognised',
  'Reference Number': '635641',
  'Type of business or Individual': 'Collective investment scheme',
  'Name': 'Jupiter Asia Pacific Income Fund (IRL)'}]
```
The response data as stored in the `fsr_data` property might be non-empty or empty depending on whether the combination of query and entity type is valid, e.g.:
```python
>>> client.common_search(urlencode({'q': 'natwest', 'type': 'individual'})).fsr_data
# Null
```

## Searching for FRNs, IRNs and PRNs

Generally, firm reference numbers (FRN), individual reference numbers (IRN), and product reference numbers (PRN), may not be known in advance. These can be found via the following client search methods:

* `search_frn`
* `search_irn`
* `search_prn`

FRNs, IRNs, and PRNs uniquely identify firms, individuals, and funds, respectively, in the FS Register, whether current or past. 
The searches can be performed with the relevant method by name - the search is case-insensitive in name, and the more precise the name the more likely is an exact, unique result. Some examples are given below for each type of search, starting with FRNs:
```python
>>> client.search_frn('hiscox insurance company limited')
'113849'
```
Imprecise names in the search can produce multiple records, and will trigger an `fsrapiclient.api.FsrResponseException` indicating the problem, e.g.:
```python
>>> client.search_frn('hiscox')
FsrApiResponseException: Multiple firms returned. Firm name needs to be more precise. If you are unsure of the results please use the common search endpoint
```
In this case the exception was generated because a common search for `"hiscox"` shows that there are multiple firm entries featuring the name `"Hiscox"``:
```python
>>> client.common_search(urlencode({'q': 'hiscox', 'type': 'firm'})).fsr_data
[{'URL': 'https://register.fca.org.uk/services/V0.1/Firm/812274',
  'Status': 'No longer authorised',
  'Reference Number': '812274',
  'Type of business or Individual': 'Firm',
  'Name': 'HISCOX ASSURE'},
...
...
 {'URL': 'https://register.fca.org.uk/services/V0.1/Firm/732312',
  'Status': 'Authorised',
  'Reference Number': '732312',
  'Type of business or Individual': 'Firm',
  'Name': 'Hiscox MGA Ltd (Postcode: EC2N 4BQ)'}]
```
Searches for non-existent firms will trigger an `FsrApiResponseException` indicating that no data found in the FS Register for the given name:
```python
>>> client.search_frn('a nonexistent firm')
FsrApiResponseException: No data found in FSR API response. Please check the search parameters and try again.
```

A few examples are given below of IRN searches.
```python
>>> client.search_irn('mark carney')
'MXC29012'
>>> client.search_irn('mark c')
FsrApiResponseException: Multiple individuals returned. The individual name needs to be more precise. If you are unsure of the results please use the common search endpoint
>>> client.search_irn('a nonexistent individual')
FsrApiResponseException: No data found in FSR API response. Please check the search parameters and try again.
```

A few examples are given below of PRN searches.
```python
>>> client.search_prn('jupiter asia pacific income')
'635641'
>>> client.search('jupiter asia')
FsrApiResponseException: Multiple funds returned. The fund name needs to be more precise. If you are unsure of the results please use the common search endpoint
>>> client.search_frn('a nonexistent fund')
FsrApiResponseException: No data found in FSR API response. Please check the search parameters and try again.
```
## Firms

Firm-specific client methods, the associated API endpoints, and parameters and returns are summarised in the table below.

| Method                                  | API endpoint                                             | Parameters                             | Return           |
|-----------------------------------------|----------------------------------------------------------|----------------------------------------|------------------|
| `get_firm`                              | `/V0.1/Firm/{FRN}`                                       | FRN (str)                              | `FsrApiResponse` |
| `get_firm_addresses`                    | `/V0.1/Firm/{FRN}/Address`                               | FRN (str)                              | `FsrApiResponse` |
| `get_firm_appointed_representatives`    | `/V0.1/Firm/{FRN}/AR`                                    | FRN (str)                              | `FsrApiResponse` |
| `get_firm_controlled_functions`         | `/V0.1/Firm/{FRN}/CF`                                    | FRN (str)                              | `FsrApiResponse` |
| `get_firm_disciplinary_history`         | `/V0.1/Firm/{FRN}/DisciplinaryHistory`                   | FRN (str)                              | `FsrApiResponse` |
| `get_firm_exclusions`                   | `/V0.1/Firm/{FRN}/Exclusions`                            | FRN (str)                              | `FsrApiResponse` |
| `get_firm_individuals`                  | `/V0.1/Firm/{FRN}/Individuals`                           | FRN (str)                              | `FsrApiResponse` |
| `get_firm_names`                        | `/V0.1/Firm/{FRN}/Names`                                 | FRN (str)                              | `FsrApiResponse` |
| `get_firm_passports`                    | `/V0.1/Firm/{FRN}/Passports`                             | FRN (str)                              | `FsrApiResponse` |
| `get_firm_passport_permissions`         | `/V0.1/Firm/{FRN}/Passports/{Country}/Permission`        | FRN (str), Country (str)               | `FsrApiResponse` |
| `get_firm_permissions`                  | `/V0.1/Firm/{FRN}/Permissions`                           | FRN (str)                              | `FsrApiResponse` |
| `get_firm_regulators`                   | `/V0.1/Firm/{FRN}/Regulators`                            | FRN (str)                              | `FsrApiResponse` |
| `get_firm_requirements`                 | `/V0.1/Firm/{FRN}/Requirements`                          | FRN (str)                              | `FsrApiResponse` |
| `get_firm_requirement_investment_types` | `/V0.1/Firm/{FRN}/Requirements/{ReqRef}/InvestmentTypes` | FRN (str), Requirement Reference (str) | `FsrApiResponse` |
| `get_firm_waivers`                      | `/V0.1/Firm/{FRN}/Waiver`                                | FRN (str)                              | `FsrApiResponse` |

Examples are given below for Barclays Bank Plc.
```python
>>> client.get_firm('122702').fsr_data
[{'Name': 'https://register.fca.org.uk/services/V0.1/Firm/122702/Names',
  'Individuals': 'https://register.fca.org.uk/services/V0.1/Firm/122702/Individuals',
  'Requirements': 'https://register.fca.org.uk/services/V0.1/Firm/122702/Requirements',
  'Permission': 'https://register.fca.org.uk/services/V0.1/Firm/122702/Permissions',
  'Passport': 'https://register.fca.org.uk/services/V0.1/Firm/122702/Passports',
  'Regulators': 'https://register.fca.org.uk/services/V0.1/Firm/122702/Regulators',
  'Appointed Representative': 'https://register.fca.org.uk/services/V0.1/Firm/122702/AR',
  'Address': 'https://register.fca.org.uk/services/V0.1/Firm/122702/Address',
  'Waivers': 'https://register.fca.org.uk/services/V0.1/Firm/122702/Waivers',
  'Exclusions': 'https://register.fca.org.uk/services/V0.1/Firm/122702/Exclusions',
  'DisciplinaryHistory': 'https://register.fca.org.uk/services/V0.1/Firm/122702/DisciplinaryHistory',
  'System Timestamp': '30/11/2024 20:34',
  'Exceptional Info Details': [],
  'Status Effective Date': '01/12/2001',
  'E-Money Agent Status': '',
  'PSD / EMD Effective Date': '',
  'Client Money Permission': 'Control but not hold client money',
  'Sub Status Effective from': '',
  'Sub-Status': '',
  'Mutual Society Number': '',
  'Companies House Number': '01026167',
  'MLRs Status Effective Date': '',
  'MLRs Status': '',
  'E-Money Agent Effective Date': '',
  'PSD Agent Effective date': '',
  'PSD Agent Status': '',
  'PSD / EMD Status': '',
  'Status': 'Authorised',
  'Business Type': 'Regulated',
  'Organisation Name': 'Barclays Bank Plc',
  'FRN': '122702'}]
>>> client.get_firm_addresses('122702')
[{'URL': 'https://register.fca.org.uk/services/V0.1/Firm/122702/Address?Type=PPOB',
  'Website Address': 'www.barclays.com',
  'Phone Number': '+442071161000',
  'Country': 'UNITED KINGDOM',
  'Postcode': 'E14 5HP',
  'County': '',
  'Town': 'London',
  'Address Line 4': '',
  'Address LIne 3': '',
  'Address Line 2': '',
  'Address Line 1': 'One Churchill Place',
  'Address Type': 'Principal Place of Business'},
 {'URL': 'https://register.fca.org.uk/services/V0.1/Firm/122702/Address?Type=Complaint',
  'Website Address': '',
  'Phone Number': '+4403301595858',
  'Country': 'UNITED KINGDOM',
  'Postcode': 'NN4 7SG',
  'County': 'Northamptonshire',
  'Town': 'Northampton',
  'Address Line 4': '',
  'Address LIne 3': '',
  'Address Line 2': '',
  'Address Line 1': '1234 Pavilion Drive',
  'Individual': '',
  'Address Type': 'Complaints Contact'}]
>>> client.get_firm_controlled_functions('122702').fsr_data
[{'Current': {'(6707)SMF4 Chief Risk': {'Suspension / Restriction End Date': '',
    'Suspension / Restriction Start Date': '',
    'Restriction': '',
    'Effective Date': '16/02/2023',
    'Individual Name': 'Bevan Cowie',
    'Name': 'SMF4 Chief Risk',
    'URL': 'https://register.fca.org.uk/services/V0.1/Individuals/BXC00280'},
...
   '(22338)[PRA CF] Significant risk taker or Material risk taker': {'End Date': '30/06/2020',
    'Suspension / Restriction End Date': '',
    'Suspension / Restriction Start Date': '',
    'Restriction': '',
    'Effective Date': '07/03/2016',
    'Individual Name': 'Lynne Atkin',
    'Name': '[PRA CF] Significant risk taker or Material risk taker',
    'URL': 'https://register.fca.org.uk/services/V0.1/Individuals/LAA01049'}}}]
>>> client.get_firm_disciplinary_history('122702').fsr_data
[{'TypeofDescription': "On 19 August 2009, the FSA imposed a penalty on Barclays Bank plc and Barclays Capital Securities Limited (Barclays) of £2,450,000 (discounted from £3,500,000 for early settlement) in respect of breaches of SUP 17 of the FSA Handbook and breaches of Principles 2 and 3 of the FSA's Principles for Businesses which occurred between 1 October 2006 and 31 October 2008. The breach of SUP 17 related to Barclays failure to submit accurate transaction reports as required in respect of an estimated 57.5 million transactions. Barclays breached Principle 2 by failing to conduct its business with due skill, care and diligence in failing to respond sufficiently to opportunities to review the adequacy of its transaction reporting systems. Barclays breached Principle 3 by failing to take reasonable care to organise and control its affairs responsibly and effectively, with adequate risk management systems, to meet the requirements to submit accurate transaction reports to the FSA",
  'TypeofAction': 'Fines',
  'EnforcementType': 'FSMA',
  'ActionEffectiveFrom': '08/09/2009'},
 ...
 {'TypeofDescription': "On 23 September 2022, the FCA decided to impose a financial penalty on Barclays Bank Plc. The reason for this action is because Barclays Bank Plc failed to comply with Listing Rule 1.3.3 in October 2008. This matter has been referred by Barclays Bank Plc to the Upper Tribunal. The FCA’s findings and proposed action are therefore provisional and will not take effect pending determination of this matter by the Upper Tribunal. The FCA’s decision was issued on 23 September 2022 and a copy of the Decision Notice is displayed on the FCA's web site here: https://www.fca.org.uk/publication/decision-notices/barclays-bank-plc-dn-2022.pdf \xa0",
  'TypeofAction': 'Fines',
  'EnforcementType': 'FSMA',
  'ActionEffectiveFrom': '23/09/2022'}]
>>> client.get_firm_exclusions('122702').fsr_data
[{'PSD2_Exclusion_Type': 'Limited Network Exclusion',
  'Particular_Exclusion_relied_upon': '2(k)(iii) – may be used only to acquire a very limited range of goods or services',
  'Description_of_services': 'Precision pay Virtual Prepaid - DVLA Service'}]
>>> client.get_firm_individuals('122702').fsr_data
[{'Status': 'Approved by regulator',
  'URL': 'https://register.fca.org.uk/services/V0.1/Individuals/BXC00280',
  'IRN': 'BXC00280',
  'Name': 'Bevan Cowie'},
...
 {'Status': 'Approved by regulator',
  'URL': 'https://register.fca.org.uk/services/V0.1/Individuals/TXW00011',
  'IRN': 'TXW00011',
  'Name': 'Herbert Wright'}]
>>> client.get_firm_names('122702').fsr_data
[{'Current Names': [{'Effective From': '17/05/2013',
    'Status': 'Trading',
    'Name': 'Barclays Bank'},
...
   {'Effective To': '25/01/2010',
    'Effective From': '08/03/2004',
    'Status': 'Trading',
    'Name': 'Banca Woolwich'}]}]
>>> client.get_firm_passports('122702').fsr_data
[{'Passports': [{'PassportDirection': 'Passporting Out',
    'Permissions': 'https://register.fca.org.uk/services/V0.1/Firm/122702/Passports/GIBRALTAR/Permission',
    'Country': 'GIBRALTAR'}]}]
>>> client.get_firm_passport_permissions('122702', 'Gibraltar')
[{'Permissions': [{'Name': '*  - additional MiFID services and activities subject to mutual recognition under the BCD',
    'InvestmentTypes': []},
...
 {'Permissions': [{'Name': 'Insurance Distribution or Reinsurance Distribution',
    'InvestmentTypes': []}],
  'PassportType': 'Service',
  'PassportDirection': 'Passporting Out',
  'Directive': 'Insurance Distribution',
  'Country': 'GIBRALTAR'}]
>>> client.get_firm_permissions('122702').fsr_data
{'Debt Adjusting': [{'Limitation': ['This permission is limited to debt adjusting with no debt management activity']}],
 'Credit Broking': [{'Limitation Not Found': ['Valid limitation not present']}],
 ...
  'Accepting Deposits': [{'Customer Type': ['All']},
  {'Investment Type': ['Deposit']}]}
>>> client.get_firm_regulators('122702').fsr_data
[{'Termination Date': '',
  'Effective Date': '01/04/2013',
  'Regulator Name': 'Financial Conduct Authority'},
...
 {'Termination Date': '30/11/2001',
  'Effective Date': '25/11/1993',
  'Regulator Name': 'Securities and Futures Authority'}]
>>> client.get_firm_requirements('122702').fsr_data
[{'Effective Date': '23/03/2020',
  'Written Notice - Market Risk Consolidation': 'REQUIREMENTS RELEVANT TO THE MARKET RISK CONSOLIDATION PERMISSION THAT THE FIRM HAS SOUGHT AND THE PRA IMPOSES UNDER SECTION 55M (5) OF THE ACT 1.This Market Risk Consolidation Permission applies to an institution or undertaking listed in Table 1 only for as long as it remains part of the Barclays Group. The firm must notify the PRA promptly if any of those institutions or undertakings ceases to be part of the Barclays Group. 2.The firm must, no later than 23 business days after the end of each quarter, ending March, June, September and December submit, in respect of that quarter, a report to the PRA highlighting the capital impact of market risk consolidation for each of the institutions listed in Table 1. 3.The firm must: 1.ensure that any existing legal agreements or arrangements necessary for fulfilment of the conditions of Article 325(2) of the CRR as between any of the institutions in Table 1 are maintained; and 2.notify the PRA of any variation in the terms of such agreements, or of any change in the relevant legal or regulatory framework of which it becomes aware and which may have an impact on the ability of any of the institutions listed in Table 1 to meet the conditions of Article 325(2) of the CRR. THE MARKET RISK CONSOLIDATION PERMISSION Legal Entities 1.The Market Risk Consolidation Permission means that the firm may use positions in an institution or undertaking listed in Table 1 to offset positions in another institution or undertaking listed therein only for the purposes of calculating net positions and own funds requirements in accordance with Title IV of the CRR on a consolidated basis. Table 1 Institutions and Location of undertaking: Barclays Bank PLC (BBPLC) - UK Barclays Capital Securities Limited (BCSL) UK Barclays Bank Ireland - Ireland',
  'Requirement Reference': 'OR-0170047',
  'Financial Promotions Requirement': 'FALSE'},
 ...
 {'Effective Date': '01/10/2024',
  'Financial Promotion for other unauthorised clients': 'This firm can: (1) approve its own financial promotions as well as those of members of its wider group and, in certain circumstances, those of its appointed representatives; and (2) approve financial promotions for other unauthorised persons for the following types of investment:',
  'Requirement Reference': 'OR-0262545',
  'Financial Promotions Requirement': 'TRUE',
  'Financial Promotions Investment Types': 'https://register.fca.org.uk/services/V0.1/Firm/122702/Requirements/OR-0262545/InvestmentTypes'}]
>>> client.get_firm_requirement_investment_types('122702').fsr_data
[{'Investment Type Name': 'Certificates representing certain securities'},
 {'Investment Type Name': 'Debentures'},
 {'Investment Type Name': 'Government and public security'},
 {'Investment Type Name': 'Listed shares'},
 {'Investment Type Name': 'Warrants'}]
>>> client.get_firm_waivers('122702').fsr_data
[{'Waivers_Discretions_URL': 'https://register.fca.org.uk/servlet/servlet.FileDownload?file=00P0X00001YXBw1UAH',
  'Waivers_Discretions': 'A4823494P.pdf',
  'Rule_ArticleNo': ['CRR Ar.313']},
...
 {'Waivers_Discretions_URL': 'https://register.fca.org.uk/servlet/servlet.FileDownload?file=00P4G00002oJPciUAG',
  'Waivers_Discretions': 'A00003642P.pdf',
  'Rule_ArticleNo': ['Perm & Wav - CRR Ru 2.2']}]
```

## Individuals

Individual-specific client methods, the associated API endpoints, and parameters and returns are summarised in the table below.

| Method                                | API endpoint                                  | Parameters | Return           |
|-------------------------------------- |-----------------------------------------------|------------|------------------|
| `get_individual`                      | `/V0.1/Individuals/{IRN}`                     | IRN (str)  | `FsrApiResponse` |
| `get_individual_controlled_functions` | `/V0.1/Individuals/{IRN}/CF`                  | IRN (str)  | `FsrApiResponse` |
| `get_individual_disciplinary_history` | `/V0.1/Individuals/{IRN}/DisciplinaryHistory` | IRN (str)  | `FsrApiResponse` |

Some examples are given below.
```python
>>> client.get_individual('MXC29012').fsr_data
[{'Details': {'Disciplinary History': 'https://register.fca.org.uk/services/V0.1/Individuals/MXC29012/DisciplinaryHistory',
   'Current roles & activities': 'https://register.fca.org.uk/services/V0.1/Individuals/MXC29012/CF',
   'IRN': 'MXC29012',
   'Commonly Used Name': 'Mark',
   'Status': 'Certified / assessed by firm',
   'Full Name': 'Mark Carney'},
  'Workplace Location 1': {'Firm Name': 'TSB Bank plc',
   'Location 1': 'Liverpool'}}]
>>> client.get_individual_controlled_functions('MXC29012')
[{'Previous': {'(5)Appointed representative dealing with clients for which they require qualification': {'Customer Engagement Method': 'Face To Face; Telephone; Online',
    'End Date': '05/04/2022',
    'Suspension / Restriction End Date': '',
    'Suspension / Restriction Start Date': '',
    'Restriction': '',
    'Effective Date': '23/10/2020',
    'Firm Name': 'HL Partnership Limited',
    'Name': 'Appointed representative dealing with clients for which they require qualification',
    'URL': 'https://register.fca.org.uk/services/V0.1/Firm/303397'},
...
   '(1)The London Institute of Banking and Finance (LIBF) - formerly known as IFS': {'Customer Engagement Method': '',
    'Suspension / Restriction End Date': '',
    'Suspension / Restriction Start Date': '',
    'Restriction': '',
    'Effective Date': '',
    'Firm Name': 'Echo Finance Limited',
    'Name': 'The London Institute of Banking and Finance (LIBF) - formerly known as IFS',
    'URL': 'https://register.fca.org.uk/services/V0.1/Firm/570073'}}}]
>>> client.get_individual_disciplinary_history('MXC29012')
# None
```

## Funds

Fund-specific client methods, the associated API endpoints, and parameters and returns are summarised in the table below.

| Method              | API endpoint              | Parameters | Return           |
|---------------------|---------------------------|------------|------------------|
| `get_fund`          | `/V0.1/CIS/{PRN}`         | PRN (str)  | `FsrApiResponse` |
| `get_fund_names`    | `/V0.1/CIS/{PRN}/Names`   | PRN (str)  | `FsrApiResponse` |
| `get_fund_subfunds` | `/V0.1/CIS/{PRN}/Subfund` | PRN (str)  | `FsrApiResponse` |

Some examples are given below.

```python
>>> client.get_fund('185045').fsr_data
[{'Sub-funds': 'https://register.fca.org.uk/services/V0.1/CIS/185045/Subfund',
  'Other Name': 'https://register.fca.org.uk/services/V0.1/CIS/185045/Names',
  'CIS Depositary': 'https://register.fca.org.uk/services/V0.1/Firm/805574',
  'CIS Depositary Name': 'Citibank UK Limited',
  'Operator Name': 'abrdn Fund Managers Limited',
  'Operator': 'https://register.fca.org.uk/services/V0.1/Firm/121803',
  'MMF Term Type': '',
  'MMF NAV Type': '',
  'Effective Date': '23/12/1997',
  'Scheme Type': 'UCITS (COLL)',
  'Product Type': 'ICVC',
  'ICVC Registration No': 'SI000001',
  'Status': 'Authorised'}]
>>> client.get_fund_names('185045').fsr_data
[{'Effective To': '22/08/2019',
  'Effective From': '23/12/1997',
  'Product Other Name': 'ABERDEEN INVESTMENT FUNDS ICVC'},
 {'Effective To': '01/08/2022',
  'Effective From': '23/12/1997',
  'Product Other Name': 'Aberdeen Standard OEIC I'}]
>>> client.get_fund_subfunds('185045').fsr_data
[{'URL': 'https://register.fca.org.uk/services/apexrest/V0.1/CIS/185045',
  'Sub-Fund Type': 'Other',
  'Name': 'abrdn (AAM) UK Smaller Companies Fund'},
...
 {'URL': 'https://register.fca.org.uk/services/apexrest/V0.1/CIS/185045',
  'Sub-Fund Type': 'Other',
  'Name': 'abrdn Strategic Bond Fund'}]
```


