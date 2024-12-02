from __future__ import annotations


__all__ = ['FsrApiClient',
           'FsrApiResponse',
           'FsrApiSession',]


# -- IMPORTS --

# -- Standard libraries --
import pathlib
import sys
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

from urllib.parse import urlencode

# -- 3rd party libraries --
import requests

from requests.models import Response

# -- Internal libraries --
from fsrapiclient.constants import FSR_API_CONSTANTS
from fsrapiclient.exceptions import (
    FsrApiRequestException,
    FsrApiResponseException,
)


class FsrApiSession(requests.Session):
    """A simple ``requests.Session``-based class for an FS Register API session.

    Examples
    --------
    >>> import os
    >>> session = FsrApiSession(os.environ['API_USERNAME'], os.environ['API_KEY'])
    >>> type(session)
    <class 'api.FsrApiSession'>
    >>> assert session.api_username == os.environ['API_USERNAME']
    >>> assert session.api_key == os.environ['API_KEY']
    >>> assert session.headers == {'ACCEPT': 'application/json', 'X-AUTH-EMAIL': os.environ['API_USERNAME'], 'X-AUTH-KEY': os.environ['API_KEY']}
    """

    _api_username: str
    _api_key: str

    def __init__(self, api_username: str, api_key: str) -> None:
        """Initialiser requiring the API username and key.

        Parameters
        ----------
        api_username : str
            The API username which will be the email used to sign up on the
            FS Register developer portal:
            ::

                https://register.fca.org.uk/Developer/s/

        api_key : str
            The API key obtained from the registration profile on the FS
            Register API developer portal.

        Examples
        --------
        >>> import os; from urllib.parse import urlencode
        >>> session = FsrApiSession(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> assert session.api_username == os.environ['API_USERNAME']
        >>> assert session.api_key == os.environ['API_KEY']
        >>> assert session.headers == {'ACCEPT': 'application/json', 'X-AUTH-EMAIL': os.environ['API_USERNAME'], 'X-AUTH-KEY': os.environ['API_KEY']}
        """
        super().__init__()

        self._api_username = api_username
        self._api_key = api_key
        self.headers = {
            'ACCEPT': 'application/json',
            'X-AUTH-EMAIL': self._api_username,
            'X-AUTH-KEY': self._api_key
        }

    @property
    def api_username(self) -> str:
        """:py:class:`str`: The API username (FS Register signup email).

        Returns
        -------
        str
            The API username.

        Examples
        --------
        >>> import os; from urllib.parse import urlencode
        >>> session = FsrApiSession(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> assert session.api_username == os.environ['API_USERNAME']
        """
        return self._api_username

    @property
    def api_key(self) -> str:
        """:py:class:`str`: The API key (obtained from the registration profile).

        Returns
        -------
        str
            The API key.

        Examples
        --------
        >>> import os; from urllib.parse import urlencode
        >>> session = FsrApiSession(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> assert session.api_key == os.environ['API_KEY']
        """
        return self._api_key


class FsrApiResponse(requests.models.Response):
    """A simple ``requests.Response``-based wrapper for FS Register API responses.

    Examples
    --------
    >>> import os; from urllib.parse import urlencode
    >>> client = FsrApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
    >>> res = client.common_search(urlencode({'q': 'Hastings Direct', 'type': 'firm'}))
    >>> res
    <Response [200]>
    """

    __attrs__ = Response.__attrs__

    def __init__(self, response):
        """Initialiser requiring a `requests.Response` object.

        Parameters
        ----------
        response : requests.Response
            The response from the original request.
        """    
        self.__dict__.update(**response.__dict__)

    @property
    def fsr_status(self) -> str:
        """:py:class:`str`: The FS Register status code from the original request.

        Returns
        -------
        str
            The FS Register status code from the original request.
        """
        return self.json().get('Status')

    @property
    def fsr_resultinfo(self) -> dict:
        """:py:class:`dict`: The FS Register pagination information on the response from the original request.

        Returns
        -------
        dict
            The FS Register pagination information on the response from the original request.
        """
        return self.json().get('ResultInfo')

    @property
    def fsr_message(self) -> str:
        """:py:class:`str`: The FS Register status message from the original request.

        Returns
        -------
        str
            The FS Register status message from the original request.
        """
        return self.json().get('Message')

    @property
    def fsr_data(self) -> dict | list[dict]:
        """:py:class:`dict` or :py:class:`list`: The FS Register data from the original request.

        Returns
        -------
        str
            The FS Register data from the original request - will either be a
            :py:class:`dict` or a :py:class:`list` of dicts.
        """
        return self.json().get('Data')


class FsrApiClient:
    """API client for the FS Register API (V0.1).

    Consult the developer documentation for further details on the underlying
    API.

    https://register.fca.org.uk/Developer/s/

    Examples
    --------
    >>> import os; from urllib.parse import urlencode
    >>> client = FsrApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
    >>> res = client.common_search(urlencode({'q': 'Hastings Direct', 'type': 'firm'}))
    >>> res
    <Response [200]>
    >>> res.fsr_data
    [{'URL': 'https://register.fca.org.uk/services/V0.1/Firm/969197', 'Status': 'Authorised', 'Reference Number': '969197', 'Type of business or Individual': 'Firm', 'Name': 'Hastings Financial Services Limited (Postcode: TN39 3LW)'}, {'URL': 'https://register.fca.org.uk/services/V0.1/Firm/311492', 'Status': 'Authorised', 'Reference Number': '311492', 'Type of business or Individual': 'Firm', 'Name': 'Hastings Insurance Services Limited (Postcode: TN39 3LW)'}, {'URL': 'https://register.fca.org.uk/services/V0.1/Firm/536726', 'Status': 'Authorised', 'Reference Number': '536726', 'Type of business or Individual': 'Firm', 'Name': 'I Go 4 Ltd. (Postcode: PE4 6JT)'}]
    >>> res.fsr_status
    'FSR-API-04-01-00'
    >>> res.fsr_message
    'Ok. Search successful'
    >>> res.fsr_resultinfo
    {'page': '1', 'per_page': '20', 'total_count': '3'}
    >>> client.search_frn("Hastings Insurance Services Limited")
    '311492'
    >>> client.search_frn('direct line')
    Traceback (most recent call last):
    ...
    fsrapiclient.exceptions.FsrApiResponseException: Multiple firms returned. Firm name needs to be more precise. If you are unsure of the results please use the common search endpoint
    >>> client.search_frn('direct line insurance plc')
    '202684'
    """

    _api_session: FsrApiSession

    def __init__(self, api_username: str, api_key: str):
        """Initialiser requiring the API username and key.

        Parameters
        ----------
        api_username : str
            The API username which will be the email used to sign up on the
            FS Register developer portal:
            ::

                https://register.fca.org.uk/Developer/s/

        api_key : str
            The API key obtained from the registration profile on the FS
            Register API developer portal.

        Examples
        --------
        >>> import os; from fsrapiclient.constants import FSR_API_CONSTANTS
        >>> client = FsrApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> assert client.api_session.api_username == os.environ['API_USERNAME']
        >>> assert client.api_session.api_key == os.environ['API_KEY']
        >>> assert client.api_session.headers == {'ACCEPT': 'application/json', 'X-AUTH-EMAIL': os.environ['API_USERNAME'], 'X-AUTH-KEY': os.environ['API_KEY']}
        >>> assert client.api_version == FSR_API_CONSTANTS.API_VERSION.value
        """
        self._api_session = FsrApiSession(api_username, api_key)

    @property
    def api_session(self) -> FsrApiSession:
        """:py:class:`~fsrapiclient.api.FsrApiSession`: The FS Register status message from the original request.

        Returns
        -------
        FsrApiSession
            The current :py:class:`~fsrapiclient.api.FsrApiSession` object.

        Examples
        --------
        >>> import os
        >>> client = FsrApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> assert isinstance(client.api_session, FsrApiSession)
        """
        return self._api_session

    @property
    def api_version(self) -> str:
        """:py:class:`str`: The FS Register API version being used by the client.

        Returns
        -------
        str
            The FS Register API version being used by the client.

        Examples
        --------
        >>> import os; from fsrapiclient.constants import FSR_API_CONSTANTS
        >>> client = FsrApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> assert client.api_version == FSR_API_CONSTANTS.API_VERSION.value
        """
        return FSR_API_CONSTANTS.API_VERSION.value

    def common_search(self, search_str: str) -> FsrApiResponse:
        """`py:class:~fsrapiclient.api.FsrApiResponse``: Returns a response containing the results of a search using the FS Register API common search API endpoint.

        Directly calls on the FS Register API common search endpoint:
        ::

            /V0.1/Search?q=<query>&type=<entity type>

        to perform a case-insensitive search in the FS Register on the given
        search string and entity type (``"firm"``, ``"individual"``,
        ``"fund"``).

        Returns an ``FsrApiResponse`` object if the API call completes
        without exceptions or errors.

        Parameters
        ----------
        search_str : str
            The search string - this should be a URL-encoded, parameterised
            search string of the form:
            ::

                q=<entity name>&type=<entity type>

            where ``<entity name>`` is the name of a firm, individual or fund
            (collective investment scheme), and ``<entity type>`` is one of
            the strings ``"firm"``, ``"individual"``, or ``"fund"``.

        Returns
        -------
        FsrApiResponse
            An FS Register API response object, if the request completed
            successfully.

        Raises
        ------
        FsrApiRequestException
            If there was a ``requests.RequestException`` in making the original
            request.

        Examples
        --------
        >>> import os; from urllib.parse import urlencode
        >>> client = FsrApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> res = client.common_search(urlencode({'q': 'Hastings Direct', 'type': 'firm'}))
        >>> res
        <Response [200]>
        >>> assert res.fsr_data
        >>> assert res.fsr_status
        >>> assert res.fsr_message
        >>> assert res.fsr_resultinfo
        >>> client.common_search(urlencode({'q': 'Hastings Direct', 'type': 'firm'}))
        <Response [200]>
        """
        url = f'{FSR_API_CONSTANTS.BASEURL.value}/{self.api_version}/Search?{search_str}'

        try:
            return FsrApiResponse(self.api_session.get(url))
        except requests.RequestException as e:
            raise FsrApiRequestException(e)

    def search_frn(self, firm_name: str) -> str:
        """:py:class:`str`: Returns the unique firm reference number (FRN) of a given firm, if found.

        Uses the FS Register API common search endpoint:
        ::

            /V0.1/Search?q=<firm name>&type=firm

        to perform a case-insensitive firm-type search in the FS Register on the
        given firm name.

        Returns a non-null string of the FRN if the firm name is found,
        otherwise ``None`` is returned.

        Parameters
        ----------
        firm_name : str
            The firm name - need not be in any particular case. The name
            needs to be precise enough to guarantee a unique return value,
            otherwise multiple records exist and an exception is raised.

        Raises
        ------
        FsrApiRequestException
            If there was a request exception from calling the common search
            handler.

        FsrApiResponseError
            If there was an error in the FS Register API response or in
            processing the response.

        Returns
        -------
        str
            A string version of the firm reference number (FRN), if found.

        Examples
        --------
        >>> import os
        >>> client = FsrApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> client.search_frn("Hastings Insurance Services Limited")
        '311492'
        >>> client.search_frn('hiscox insurance company limited')
        '113849'
        >>> client.search_frn('direct line')
        Traceback (most recent call last):
        ...
        fsrapiclient.exceptions.FsrApiResponseException: Multiple firms returned. Firm name needs to be more precise. If you are unsure of the results please use the common search endpoint
        >>> client.search_frn('direct line insurance')
        Traceback (most recent call last):
        ...
        fsrapiclient.exceptions.FsrApiResponseException: Multiple firms returned. Firm name needs to be more precise. If you are unsure of the results please use the common search endpoint
        >>> client.search_frn('direct line insurance plc')
        '202684'
        >>> client.search_frn('Hiscxo Insurance Company')
        Traceback (most recent call last):
        ...
        fsrapiclient.exceptions.FsrApiResponseException: No data found in FS Register API response. Please check the search parameters and try again.
        >>> client.search_frn('hiscox insurance company')
        '113849'
        """
        try:
            res = self.common_search(urlencode({'q': firm_name, 'type': 'firm'}))
        except FsrApiRequestException:
            raise

        if res.ok and res.fsr_data:
            if len(res.fsr_data) > 1:
                raise FsrApiResponseException(
                    'Multiple firms returned. Firm name needs to be more '
                    'precise. If you are unsure of the results please use the '
                    'common search endpoint'
                )

            try:
                return res.fsr_data[0]['Reference Number']
            except (KeyError, IndexError):
                raise FsrApiResponseException(
                    'Unexpected response data structure from the FS Register API for '
                    'general firm search by name! Please check the FS Register API '
                    'developer documentation at https://register.fca.org.uk/Developer/s/'
                )
        elif not res.fsr_data:
            raise FsrApiResponseException(
                'No data found in FS Register API response. Please check the search '
                'parameters and try again.'
            )
        else:
            raise FsrApiResponseException(
                f'FS Register API search request failed for some other reason: '
                f'{res.reason}'
            )

    def _firm_info(self, frn: str, modifiers: tuple[str] = None) -> FsrApiResponse:
        """:py:class:`~fsrapiclient.api.FsrApiResponse`: A private, base handler for firm information API handlers.

        Is the base handler for the following firm-specific FS Register API
        endpoints (in alphabetical order):
        ::

            /V0.1/Firm/{FRN}
            /V0.1/Firm/{FRN}/Address
            /V0.1/Firm/{FRN}/AR
            /V0.1/Firm/{FRN}/CF
            /V0.1/Firm/{FRN}/DisciplinaryHistory
            /V0.1/Firm/{FRN}/Exclusions
            /V0.1/Firm/{FRN}/Individuals
            /V0.1/Firm/{FRN}/Names
            /V0.1/Firm/{FRN}/Passports
            /V0.1/Firm/{FRN}/Passports/{Country}/Permission
            /V0.1/Firm/{FRN}/Permissions
            /V0.1/Firm/{FRN}/Regulators
            /V0.1/Firm/{FRN}/Requirements
            /V0.1/Firm/{FRN}/Requirements/{ReqRef}/InvestmentTypes
            /V0.1/Firm/{FRN}/Waiver
            
        .. note::

           This is a private method and is **not** intended for direct use by
           end users.

        Uses the firm-specific FS Register API endpoint(s)
        ::

            /V0.1/Firm/{FRN}[/<optional modifier(s)>]

        and returns an ``FsrApiResponse``, e.g. a request for information
        on Hiscox Insurance Company Limited, which has the FRN 113849.
        ::

            /V0.1/Firm/113849

        The optional modifiers, given as a tuple of strings, should represent a
        valid ordered combination of actions and/or resources related to the
        firm given by the FRN.

        The modifier strings should **NOT** contain any leading or trailing
        forward slashes (``"/"``) as this can lead to badly formed URLs
        and to responses with no FS Register data - in any case, any leading or
        trailing forward slashes are stripped before the request.

        Parameters
        ----------
        frn : str
            The firm reference number (FRN).

        modifiers : tuple, default=None
            Optional tuple of strings indicating a valid ordered combination of
            resource and/or action modifiers for the firm in question. Should
            **NOT** have a leading or trailing forward slashes (``"/"``).

        Raises
        ------
        FsrApiRequestException
            If there was a request exception from calling the firm search
            endpoint.

        Returns
        -------
        FsrApiResponse
            The FS Register API response object - there may still be no data in
            the response if the FRN isn't found.
        """
        url = f'{FSR_API_CONSTANTS.BASEURL.value}/{self.api_version}/Firm/{frn}'

        if modifiers:
            url += f'/{"/".join(modifiers)}'

        try:
            return FsrApiResponse(self.api_session.get(url))
        except requests.RequestException as e:
            raise FsrApiRequestException(e)

    def get_firm(self, frn: str) -> FsrApiResponse:
        """:py:class:`~fsrapiclient.api.FsrApiResponse`: Returns a response containing firm details, given its firm reference number (FRN)

        Handler for the top-level firm details API endpoint:
        ::

            /V0.1/Firm/{FRN}

        Returns an ``FsrApiResponse``, which could have data if the FRN exists,
        or null if it not.

        Parameters
        ----------
        frn : str
            The firm reference number (FRN).

        Returns
        -------
        FsrApiResponse
            The FS Register API response object - there may still be no data in
            the response if the FRN isn't found.

        Examples
        --------
        >>> import os
        >>> client = FsrApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> res = client.get_firm('122702')
        >>> res
        <Response [200]>
        >>> assert res.fsr_data[0]['Organisation Name'] == 'Barclays Bank Plc'
        >>> res = client.get_firm('1234567890')
        >>> assert not res.fsr_data
        """
        return self._firm_info(frn)

    def get_firm_names(self, frn: str) -> FsrApiResponse:
        """:py:class:`~fsrapiclient.api.FsrApiResponse`: Returns a response containing the alternative or secondary trading name details of a firm, given its firm reference number (FRN).

        Handler for the firm names FS Register API endpoint:
        ::

            /V0.1/Firm/{FRN}/Names

        Returns an ``FsrApiResponse``, which could have data if the FRN exists,
        or null if it not.

        Parameters
        ----------
        frn : str
            The firm reference number (FRN).

        Returns
        -------
        FsrApiResponse
            The FS Register API response object - there may still be no data in
            the response if the FRN isn't found.

        Examples
        --------
        >>> import os
        >>> client = FsrApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> res = client.get_firm_names('122702')
        >>> res
        <Response [200]>
        >>> assert res.fsr_data[0]['Current Names'][0]['Name'] == 'Barclays Bank'
        >>> assert res.fsr_data[1]['Previous Names']
        >>> res = client.get_firm_names('1234567890')
        >>> assert not res.fsr_data
        """
        return self._firm_info(frn, modifiers=('Names',))

    def get_firm_addresses(self, frn: str) -> FsrApiResponse:
        """:py:class:`~fsrapiclient.api.FsrApiResponse`: Returns a response containing the address details of a firm, given its firm reference number (FRN).

        Handler for the firm address details FS Register API endpoint:
        ::

            /V0.1/Firm/{FRN}/Address

        Returns an ``FsrApiResponse``, which could have data if the FRN exists,
        or null if it not.

        Parameters
        ----------
        frn : str
            The firm reference number (FRN).

        Returns
        -------
        FsrApiResponse
            The FS Register API response object - there may still be no data in
            the response if the FRN isn't found.

        Examples
        --------
        >>> import os
        >>> client = FsrApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> res = client.get_firm_addresses('122702')
        >>> res
        <Response [200]>
        >>> assert res.fsr_data
        >>> res = client.get_firm_addresses('1234567890')
        >>> assert not res.fsr_data
        """
        return self._firm_info(frn, modifiers=('Address',))

    def get_firm_controlled_functions(self, frn: str) -> FsrApiResponse:
        """:py:class:`~fsrapiclient.api.FsrApiResponse`: Returns a response containing the controlled functions associated with a firm ,given its firm reference number (FRN).

        Handler for the firm controlled functions FS Register API endpoint:
        ::

            /V0.1/Firm/{FRN}/CF

        Returns an ``FsrApiResponse``, which could have data if the FRN exists,
        or null if it not.

        Parameters
        ----------
        frn : str
            The firm reference number (FRN).

        Returns
        -------
        FsrApiResponse
            The FS Register API response object - there may still be no data in
            the response if the FRN isn't found.

        Examples
        --------
        >>> import os
        >>> client = FsrApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> res = client.get_firm_controlled_functions('122702')
        >>> res
        <Response [200]>
        >>> assert res.fsr_data
        >>> res = client.get_firm_controlled_functions('1234567890')
        >>> assert not res.fsr_data
        """
        return self._firm_info(frn, modifiers=('CF',))

    def get_firm_individuals(self, frn: str) -> FsrApiResponse:
        """:py:class:`~fsrapiclient.api.FsrApiResponse`: Returns a response containing the individuals associated with a firm, given its firm reference number (FRN).

        Handler for the firm individuals FS Register API endpoint:
        ::

            /V0.1/Firm/{FRN}/Individuals

        Returns an ``FsrApiResponse``, which could have data if the FRN exists,
        or null if it not.

        Parameters
        ----------
        frn : str
            The firm reference number (FRN).

        Returns
        -------
        FsrApiResponse
            The FS Register API response object - there may still be no data in
            the response if the FRN isn't found.

        Examples
        --------
        >>> import os
        >>> client = FsrApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> res = client.get_firm_individuals('122702')
        >>> res
        <Response [200]>
        >>> assert res.fsr_data
        >>> res = client.get_firm_individuals('1234567890')
        >>> assert not res.fsr_data
        """
        return self._firm_info(frn, modifiers=('Individuals',))

    def get_firm_permissions(self, frn: str) -> FsrApiResponse:
        """:py:class:`~fsrapiclient.api.FsrApiResponse`: Returns a response containing the permissions associated with a firm, given its firm reference number (FRN).

        Handler for the firm permissions FS Register API endpoint:
        ::

            /V0.1/Firm/{FRN}/Permissions

        Returns an ``FsrApiResponse``, which could have data if the FRN exists,
        or null if it not.

        Parameters
        ----------
        frn : str
            The firm reference number (FRN).

        Returns
        -------
        FsrApiResponse
            The FS Register API response object - there may still be no data in
            theresponse if the FRN isn't found.

        Examples
        --------
        >>> import os
        >>> client = FsrApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> res = client.get_firm_permissions('122702')
        >>> res
        <Response [200]>
        >>> assert res.fsr_data
        >>> res = client.get_firm_permissions('1234567890')
        >>> assert not res.fsr_data
        """
        return self._firm_info(frn, modifiers=('Permissions',))

    def get_firm_requirements(self, frn: str) -> FsrApiResponse:
        """:py:class:`~fsrapiclient.api.FsrApiResponse`: Returns a response containing the requirements associated with a firm, given its firm reference number (FRN).

        Handler for the firm requirements FS Register API endpoint:
        ::

            /V0.1/Firm/{FRN}/Requirements

        Returns an ``FsrApiResponse``, which could have data if the FRN exists,
        or null if it not.

        Parameters
        ----------
        frn : str
            The firm reference number (FRN).

        Returns
        -------
        FsrApiResponse
            The FS Register API response object - there may still be no data in
            the response if the FRN isn't found.

        Examples
        --------
        >>> import os
        >>> client = FsrApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> res = client.get_firm_requirements('122702')
        >>> res
        <Response [200]>
        >>> assert res.fsr_data
        >>> res = client.get_firm_requirements('1234567890')
        >>> assert not res.fsr_data
        """
        return self._firm_info(frn, modifiers=('Requirements',))

    def get_firm_requirement_investment_types(self, frn: str, req_ref: str) -> FsrApiResponse:
        """:py:class:`~fsrapiclient.api.FsrApiResponse`: Returns a response containing any investment types listed for a specific requirement associated with a firm, given its firm reference number (FRN).

        Handler for the firm requirement investment types FS Register API endpoint:
        ::

            /V0.1/Firm/{FRN}/Requirements/<ReqRef>/InvestmentTypes

        Returns an ``FsrApiResponse``, which could have data if the FRN exists,
        or null if it not.

        Parameters
        ----------
        frn : str
            The firm reference number (FRN).

        req_ref : str
            The requirement reference number as a string.

        Returns
        -------
        FsrApiResponse
            The FS Register API response object - there may still be no data in
            the response if the FRN isn't found.

        Examples
        --------
        >>> import os
        >>> client = FsrApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> res = client.get_firm_requirement_investment_types('122702', 'OR-0262545')
        >>> assert res.fsr_data
        >>> res = client.get_firm_requirement_investment_types('1234567890', 'OR-0262545')
        >>> assert not res.fsr_data
        """
        return self._firm_info(frn, modifiers=('Requirements', req_ref, 'InvestmentTypes'))

    def get_firm_regulators(self, frn: str) -> FsrApiResponse:
        """:py:class:`~fsrapiclient.api.FsrApiResponse`: Returns a response containing the regulators associated with a firm, given its firm reference number (FRN).

        Handler for the firm regulators FS Register API endpoint:
        ::

            /V0.1/Firm/{FRN}/Regulators

        Returns an ``FsrApiResponse``, which could have data if the FRN exists,
        or null if it not.

        Parameters
        ----------
        frn : str
            The firm reference number (FRN).

        Returns
        -------
        FsrApiResponse
            The FS Register API response object - there may still be no data in
            the response if the FRN isn't found.

        Examples
        --------
        >>> import os
        >>> client = FsrApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> res = client.get_firm_regulators('122702')
        >>> res
        <Response [200]>
        >>> assert res.fsr_data
        >>> res = client.get_firm_regulators('1234567890')
        >>> assert not res.fsr_data
        """
        return self._firm_info(frn, modifiers=('Regulators',))

    def get_firm_passports(self, frn: str) -> FsrApiResponse:
        """:py:class:`~fsrapiclient.api.FsrApiResponse`: Returns a response containing the passports associated with a firm, given its firm reference number (FRN).

        Handler for the firm passports FS Register API endpoint:
        ::

            /V0.1/Firm/{FRN}/Passports

        Returns an ``FsrApiResponse``, which could have data if the FRN exists,
        or null if it not.

        Parameters
        ----------
        frn : str
            The firm reference number (FRN).

        Returns
        -------
        FsrApiResponse
            The FS Register API response object - there may still be no data in
            the response if the FRN isn't found.

        Examples
        --------
        >>> import os
        >>> client = FsrApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> res = client.get_firm_passports('122702')
        >>> res
        <Response [200]>
        >>> assert res.fsr_data
        >>> res = client.get_firm_passports('1234567890')
        >>> assert not res.fsr_data
        """
        return self._firm_info(frn, modifiers=('Passports',))

    def get_firm_passport_permissions(self, frn: str, country: str) -> FsrApiResponse:
        """:py:class:`~fsrapiclient.api.FsrApiResponse`: Returns a response containing country-specific passport permissions for a firm and a country, given its firm reference number (FRN) and country name.

        Handler for the firm passport permissions FS Register API endpoint:
        ::

            /V0.1/Firm/{FRN}/Requirements/{Country}/Permission

        Returns an ``FsrApiResponse``, which could have data if the FRN exists,
        or null if it not.

        Parameters
        ----------
        frn : str
            The firm reference number (FRN).

        country : str
            The country name.

        Returns
        -------
        FsrApiResponse
            The FS Register API response object - there may still be no data in
            the response if the FRN isn't found.

        Examples
        --------
        >>> import os
        >>> client = FsrApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> res = client.get_firm_passport_permissions('122702', 'Gibraltar')
        >>> assert res.fsr_data
        >>> res = client.get_firm_passport_permissions('1234567890', 'Gibraltar')
        >>> assert not res.fsr_data
        """
        return self._firm_info(frn, modifiers=('Passports', country, 'Permission'))

    def get_firm_waivers(self, frn: str) -> FsrApiResponse:
        """:py:class:`~fsrapiclient.api.FsrApiResponse`: Returns a response containing any waivers applying to a firm, given its firm reference number (FRN).

        Handler for the firm waivers FS Register API endpoint:
        ::

            /V0.1/Firm/{FRN}/Waivers

        Returns an ``FsrApiResponse``, which could have data if the FRN exists,
        or null if it not.

        Parameters
        ----------
        frn : str
            The firm reference number (FRN).

        Returns
        -------
        FsrApiResponse
            The FS Register API response object - there may still be no data in
            the response if the FRN isn't found.

        Examples
        --------
        >>> import os
        >>> client = FsrApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> res = client.get_firm_waivers('122702')
        >>> res
        <Response [200]>
        >>> assert res.fsr_data
        >>> res = client.get_firm_waivers('1234567890')
        >>> assert not res.fsr_data
        """
        return self._firm_info(frn, modifiers=('Waivers',))

    def get_firm_exclusions(self, frn: str) -> FsrApiResponse:
        """:py:class:`~fsrapiclient.api.FsrApiResponse`: Returns a response containing any exclusions applying to a firm, given its firm reference number (FRN).

        Handler for the firm exclusions FS Register API endpoint:
        ::

            /V0.1/Firm/{FRN}/Exclusions

        Returns an ``FsrApiResponse``, which could have data if the FRN exists,
        or null if it not.

        Parameters
        ----------
        frn : str
            The firm reference number (FRN).

        Returns
        -------
        FsrApiResponse
            The FS Register API response object - there may still be no data in
            the response if the FRN isn't found.

        Examples
        --------
        >>> import os
        >>> client = FsrApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> res = client.get_firm_exclusions('122702')
        >>> res
        <Response [200]>
        >>> assert res.fsr_data
        >>> res = client.get_firm_exclusions('1234567890')
        >>> assert not res.fsr_data
        """
        return self._firm_info(frn, modifiers=('Exclusions',))

    def get_firm_disciplinary_history(self, frn: str) -> FsrApiResponse:
        """:py:class:`~fsrapiclient.api.FsrApiResponse`: Returns a response containing the disciplinary history of a firm, given its firm reference number (FRN).

        Handler for the firm disciplinary history FS Register API endpoint:
        ::

            /V0.1/Firm/{FRN}/DisciplinaryHistory

        Returns an ``FsrApiResponse``, which could have data if the FRN exists,
        or null if it not.

        Parameters
        ----------
        frn : str
            The firm reference number (FRN).

        Returns
        -------
        FsrApiResponse
            The FS Register API response object - there may still be no data in
            the response if the FRN isn't found.

        Examples
        --------
        >>> import os
        >>> client = FsrApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> res = client.get_firm_disciplinary_history('122702')
        >>> res
        <Response [200]>
        >>> assert res.fsr_data
        >>> res = client.get_firm_disciplinary_history('1234567890')
        >>> assert not res.fsr_data
        """
        return self._firm_info(frn, modifiers=('DisciplinaryHistory',))

    def get_firm_appointed_representatives(self, frn: str) -> FsrApiResponse:
        """:py:class:`~fsrapiclient.api.FsrApiResponse`: Returns a response containing information on the appointed representatives of a firm, given its firm reference number (FRN).

        Handler for the firm appointed representatives FS Register API
        endpoint:
        ::

            /V0.1/Firm/{FRN}/AR

        Returns an ``FsrApiResponse``, which could have data if the FRN exists,
        or null if it not.

        Parameters
        ----------
        frn : str
            The firm reference number (FRN).

        Returns
        -------
        FsrApiResponse
            The FS Register API response object - there may still be no data in
            the response if the FRN isn't found.

        Examples
        --------
        >>> import os
        >>> client = FsrApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> res = client.get_firm_appointed_representatives('122702')
        >>> res
        <Response [200]>
        >>> assert res.fsr_data
        >>> assert any([res.fsr_data['PreviousAppointedRepresentatives'], res.fsr_data['CurrentAppointedRepresentatives']])
        >>> res = client.get_firm_appointed_representatives('1234567890')
        >>> assert not any([res.fsr_data['PreviousAppointedRepresentatives'], res.fsr_data['CurrentAppointedRepresentatives']])
        """
        return self._firm_info(frn, modifiers=('AR',))

    def search_irn(self, individual_name: str) -> str:
        """:py:class:`str`: Returns the unique individual reference number (IRN) of a given individual, if found.

        Uses the FS Register API common search endpoint:
        ::

            /V0.1/Search?q=<individual name>&type=individual

        to perform a case-insensitive individual-type search in the FS Register on the
        given name.

        Returns a non-null string of the IRN if the individual name is found,
        otherwise ``None`` is returned.

        Parameters
        ----------
        individual_name : str
            The individual name - need not be in any particular case. The name
            needs to be precise enough to guarantee a unique return value,
            otherwise multiple records exist and an exception is raised.

        Raises
        ------
        FsrApiRequestException
            If there was a request exception from calling the common search
            handler.

        FsrApiResponseError
            If there was an error in the FS Register API response or in
            processing the response.

        Returns
        -------
        str
            A string version of the individual reference number (IRN), if
            found.

        Examples
        --------
        >>> import os
        >>> client = FsrApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> client.search_irn('Mark Carney')
        'MXC29012'
        >>> client.search_irn('mark Carney')
        'MXC29012'
        >>> client.search_irn('Mark C')
        Traceback (most recent call last):
        ...
        fsrapiclient.exceptions.FsrApiResponseException: Multiple individuals returned. The individual name needs to be more precise. If you are unsure of the results please use the common search endpoint
        >>> client.search_irn('A Nonexistent Person')
        Traceback (most recent call last):
        ...
        fsrapiclient.exceptions.FsrApiResponseException: No data found in FS Register API response. Please check the search parameters and try again.
        """
        try:
            res = self.common_search(urlencode({'q': individual_name, 'type': 'individual'}))
        except FsrApiRequestException:
            raise
            
        if res.ok and res.fsr_data:
            if len(res.fsr_data) > 1:
                raise FsrApiResponseException(
                    'Multiple individuals returned. The individual name needs '
                    'to be more precise. If you are unsure of the results '
                    'please use the common search endpoint'
                )

            try:
                return res.fsr_data[0]['Reference Number']
            except (KeyError, IndexError):
                raise FsrApiResponseException(
                    'Unexpected response data structure from the FS Register API for '
                    'general individual search by name! Please check the FS Register API '
                    'developer documentation at https://register.fca.org.uk/Developer/s/'
                )
        elif not res.fsr_data:
            raise FsrApiResponseException(
                'No data found in FS Register API response. Please check the search '
                'parameters and try again.'
            )
        else:
            raise FsrApiResponseException(
                f'FS Register API search request failed for some other reason: '
                f'{res.reason}'
            )

    def _individual_info(self, irn: str, modifiers: tuple[str] = None) -> FsrApiResponse:
        """:py:class:`~fsrapiclient.api.FsrApiResponse`: A private, base handler for individual information API handlers.

        Is the base handler for the following individual-specific FS Register
        API endpoints:
        ::

            /V0.1/Individuals/{IRN}
            /V0.1/Individuals/{IRN}/CF
            /V0.1/Individuals/{IRN}/DisciplinaryHistory

        .. note::

           This is a private method and is **not** intended for direct use by
           end users.

        Uses the FS Register API individual endpoint(s)
        ::

            /V0.1/Individuals/{IRN}[/<optional modifier(s)>]

        and returns an ``FsrApiResponse``, e.g. a request for information
        on "Mark Carney", who has the IRN 'MXC29012'.
        ::

            /V0.1/Individuals/MXC29012

        The optional modifiers, given as a tuple of strings, should represent a
        valid ordered combination of actions and/or resources related to the
        individual given by the IRN.

        The modifier strings should **NOT** contain any leading or trailing
        forward slashes (``"/"``) as this can lead to badly formed URLs
        and to responses with no FS Register data - in any case, any leading or
        trailing forward slashes are stripped before the request.

        Parameters
        ----------
        irn : str
            The individual reference number (IRN).

        modifiers : tuple, default=None
            Optional tuple of strings indicating a valid ordered combination of
            resource and/or action modifiers for the individual in question.
            Should**NOT** have a leading or trailing forward slashes (``"/"``).

        Raises
        ------
        FsrApiRequestException
            If there was a request exception from calling the firm search
            endpoint.

        Returns
        -------
        FsrApiResponse
            The FS Register API response object - there may still be no data in
            the response if the FRN isn't found.
        """
        url = f'{FSR_API_CONSTANTS.BASEURL.value}/{self.api_version}/Individuals/{irn}'

        if modifiers:
            url += f'/{"/".join(modifiers)}'

        try:
            return FsrApiResponse(self.api_session.get(url))
        except requests.RequestException as e:
            raise FsrApiRequestException(e)

    def get_individual(self, irn: str) -> FsrApiResponse:
        """:py:class:`~fsrapiclient.api.FsrApiResponse` : Returns a response containing individual details, given their individual reference number (IRN)

        Handler for top-level individual details API endpoint:
        ::

            /V0.1/Individuals/{IRN}

        Returns an ``FsrApiResponse``, which could have data if the IRN exists,
        or null if it not.

        Parameters
        ----------
        irn : str
            The individual reference number (IRN).

        Returns
        -------
        FsrApiResponse
            The FS Register API response object - there may still be no data in
            the response if the IRN isn't found.

        Examples
        --------
        >>> import os
        >>> client = FsrApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> res = client.get_individual('MXC29012')
        >>> res
        <Response [200]>
        >>> assert res.fsr_data[0]['Details']['Full Name'] == 'Mark Carney'
        >>> res = client.get_individual('1234567890')
        >>> assert not res.fsr_data
        """
        return self._individual_info(irn)

    def get_individual_controlled_functions(self, irn: str) -> FsrApiResponse:
        """:py:class:`~fsrapiclient.api.FsrApiResponse` : Returns a response containing the controlled functions associated with an individual, given their individual reference number (FRN).

        Handler for the individual controlled functions FS Register API endpoint:
        ::

            /V0.1/Firm/{IRN}/CF

        Returns an ``FsrApiResponse``, which could have data if the IRN exists,
        or null if it not.

        Parameters
        ----------
        irn : str
            The individual reference number (IRN).

        Returns
        -------
        FsrApiResponse
            The FS Register API response object - there may still be no data in
            the response if the IRN isn't found.

        Examples
        --------
        >>> import os
        >>> client = FsrApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> res = client.get_individual_controlled_functions('MXC29012')
        >>> res
        <Response [200]>
        >>> assert res.fsr_data
        >>> res = client.get_individual_controlled_functions('1234567890')
        >>> assert not res.fsr_data
        """
        return self._individual_info(irn, modifiers=('CF',))

    def get_individual_disciplinary_history(self, irn: str) -> FsrApiResponse:
        """:py:class:`~fsrapiclient.api.FsrApiResponse` : Returns a response containing the disciplinary history of an individual, given their individual reference number (FRN).

        Handler for the individual disciplinary history FS Register API endpoint:
        ::

            /V0.1/Firm/{IRN}/DisciplinaryHistory

        Returns an ``FsrApiResponse``, which could have data if the IRN exists,
        or null if it not.

        Parameters
        ----------
        irn : str
            The individual reference number (IRN).

        Returns
        -------
        FsrApiResponse
            The FS Register API response object - there may still be no data in
            the response if the IRN isn't found.

        Examples
        --------
        >>> import os
        >>> client = FsrApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> client.search_irn('Leigh Mackey')
        'LXM01328'
        >>> res = client.get_individual_disciplinary_history('LXM01328')
        >>> res
        <Response [200]>
        >>> assert res.fsr_data
        >>> res = client.get_individual_disciplinary_history('1234567890')
        >>> assert not res.fsr_data
        """
        return self._individual_info(irn, modifiers=('DisciplinaryHistory',))

    def search_prn(self, fund_name: str) -> str:
        """:py:class:`~fsrapiclient.api.FsrApiResponse` : Returns the unique product reference number (IRN) of a given fund or collective investment scheme (CIS), including subfunds, if it exists.

        Uses the FS Register API common search endpoint:
        ::

            /V0.1/Search?q=<fund name>&type=fund

        to perform a case-insensitive fund-type search in the FS Register on
        the given name.

        Returns a non-null string of the PRN if the fund name is found,
        otherwise ``None`` is returned.

        Parameters
        ----------
        fund_name : str
            The fund name - need not be in any particular case. The name needs
            to be precise enough to guarantee a unique return value, otherwise
            multiple records exist and an exception is raised.

        Raises
        ------
        FsrApiRequestException
            If there was a request exception from calling the common search
            handler.

        FsrApiResponseError
            If there was an error in the FS Register API response or in
            processing the response.

        Returns
        -------
        str
            A string version of the product reference number (PRN), if found.

        Examples
        --------
        >>> import os
        >>> client = FsrApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> client.search_prn('Northern Trust')
        Traceback (most recent call last):
        ...
        fsrapiclient.exceptions.FsrApiResponseException: Multiple funds returned. The fund name needs to be more precise. If you are unsure of the results please use the common search endpoint
        >>> client.search_prn('Northern Trust High Dividend ESG World Equity')
        Traceback (most recent call last):
        ...
        fsrapiclient.exceptions.FsrApiResponseException: Multiple funds returned. The fund name needs to be more precise. If you are unsure of the results please use the common search endpoint
        >>> client.search_prn('Northern Trust High Dividend ESG World Equity Feeder Fund')
        '913937'
        >>> client.search_prn('A nonexistent fund')
        Traceback (most recent call last):
        ...
        fsrapiclient.exceptions.FsrApiResponseException: No data found in FS Register API response. Please check the search parameters and try again.
        """
        try:
            res = self.common_search(urlencode({'q': fund_name, 'type': 'fund'}))
        except FsrApiRequestException:
            raise
            
        if res.ok and res.fsr_data:
            if len(res.fsr_data) > 1:
                raise FsrApiResponseException(
                    'Multiple funds returned. The fund name needs '
                    'to be more precise. If you are unsure of the results '
                    'please use the common search endpoint'
                )

            try:
                return res.fsr_data[0]['Reference Number']
            except (KeyError, IndexError):
                raise FsrApiResponseException(
                    'Unexpected response data structure from the FS Register API for '
                    'general fund search by name! Please check the FS Register API '
                    'developer documentation at https://register.fca.org.uk/Developer/s/'
                )
        elif not res.fsr_data:
            raise FsrApiResponseException(
                'No data found in FS Register API response. Please check the search '
                'parameters and try again.'
            )
        else:
            raise FsrApiResponseException(
                f'FS Register API search request failed for some other reason: '
                f'{res.reason}'
            )

    def _fund_info(self, prn: str, modifiers: tuple[str] = None) -> FsrApiResponse:
        """:py:class:`~fsrapiclient.api.FsrApiResponse` : A private, base handler for fund (or collective investment scheme (CIS)) information API handlers.

        Is the base handler for the following fund-specific FS Register API
        endpoints:
        ::

            /V0.1/CIS/{PRN}
            /V0.1/CIS/{PRN}/Subfund
            /V0.1/CIS/{PRN}/Names

        .. note::

           This is a private method and is **not** intended for direct use by
           end users.

        Uses the FS Register API individual endpoint(s)
        ::

            /V0.1/CIS/{PRN}[/<optional modifier(s)>]

        and returns an ``FsrApiResponse``, e.g. a request for information
        on "'Northern Trust High Dividend ESG World Equity Feeder Fund", which
        has the PRN '913937'.
        ::

            /V0.1/CIS/913937

        The optional modifiers, given as a tuple of strings, should represent a
        valid ordered combination of actions and/or resources related to the
        fund given by the PRN.

        The modifier strings should **NOT** contain any leading or trailing
        forward slashes (``"/"``) as this can lead to badly formed URLs
        and to responses with no FS Register data - in any case, any leading or
        trailing forward slashes are stripped before the request.

        Parameters
        ----------
        prn : str
            The product reference number (IRN).

        modifiers : tuple, default=None
            Optional tuple of strings indicating a valid ordered combination of
            resource and/or action modifiers for the fund in question.
            Should**NOT** have a leading or trailing forward slashes (``"/"``).

        Raises
        ------
        FsrApiRequestException
            If there was a request exception from calling the firm search
            endpoint.

        Returns
        -------
        FsrApiResponse
            The FS Register API response object - there may still be no data in
            the response if the FRN isn't found.
        """
        url = f'{FSR_API_CONSTANTS.BASEURL.value}/{self.api_version}/CIS/{prn}'

        if modifiers:
            url += f'/{"/".join(modifiers)}'

        try:
            return FsrApiResponse(self.api_session.get(url))
        except requests.RequestException as e:
            raise FsrApiRequestException(e)

    def get_fund(self, prn: str) -> FsrApiResponse:
        """:py:class:`~fsrapiclient.api.FsrApiResponse` : Returns a response containing fund (or collective investment scheme (CIS)) details, given its product reference number (PRN)

        Handler for top-level fund details API endpoint:
        ::

            /V0.1/CIS/{PRN}

        Returns an ``FsrApiResponse``, which could have data if the PRN exists,
        or null if it not.

        Parameters
        ----------
        prn : str
            The product reference number (PRN).

        Returns
        -------
        FsrApiResponse
            The FS Register API response object - there may still be no data in
            the response if the PRN isn't found.

        Examples
        --------
        >>> import os
        >>> client = FsrApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> res = client.get_fund('185045')
        >>> res
        <Response [200]>
        >>> assert res.fsr_data
        >>> res = client.get_fund('1234567890')
        >>> assert not res.fsr_data
        """
        return self._fund_info(prn)

    def get_fund_names(self, prn: str) -> FsrApiResponse:
        """:py:class:`~fsrapiclient.api.FsrApiResponse` : Returns a response containing the alternative or secondary trading name details of a fund (or collective investment scheme (CIS)), given its product reference number (PRN).

        Handler for top-level fund names API endpoint:
        ::

            /V0.1/CIS/{PRN}/Names

        Returns an ``FsrApiResponse``, which could have data if the PRN exists,
        or null if it not.

        Parameters
        ----------
        prn : str
            The product reference number (PRN).

        Returns
        -------
        FsrApiResponse
            The FS Register API response object - there may still be no data in
            the response if the PRN isn't found.

        Examples
        --------
        >>> import os
        >>> client = FsrApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> res = client.get_fund_names('185045')
        >>> res
        <Response [200]>
        >>> assert res.fsr_data
        >>> res = client.get_fund_names('1234567890')
        >>> assert not res.fsr_data
        """
        return self._fund_info(prn, modifiers=('Names',))

    def get_fund_subfunds(self, prn: str) -> FsrApiResponse:
        """:py:class:`~fsrapiclient.api.FsrApiResponse` : Returns a response containing the subfund details of a fund (or collective investment scheme (CIS)), given its product reference number (PRN).

        Handler for top-level subfund details API endpoint:
        ::

            /V0.1/CIS/{PRN}/Subfund

        Returns an ``FsrApiResponse``, which could have data if the PRN exists,
        or null if it not.

        Parameters
        ----------
        prn : str
            The product reference number (PRN).

        Returns
        -------
        FsrApiResponse
            The FS Register API response object - there may still be no data in
            the response if the PRN isn't found.

        Examples
        --------
        >>> import os
        >>> client = FsrApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> res = client.get_fund_subfunds('185045')
        >>> res
        <Response [200]>
        >>> assert res.fsr_data
        >>> res = client.get_fund_subfunds('1234567890')
        >>> assert not res.fsr_data
        """
        return self._fund_info(prn, modifiers=('Subfund',))

if __name__ == "__main__":      # pragma: no cover
    # Doctest the module from the project root using
    #
    #     export API_USERNAME=<API username> && export API_KEY=<API key> && python -m doctest -v src/fsrapiclient/api.py && unset API_USERNAME && unset API_KEY
    #
    import doctest
    doctest.testmod()
