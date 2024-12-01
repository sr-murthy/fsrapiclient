# -- IMPORTS --

# -- Standard libraries --
import os
import unittest.mock as mock

from urllib.parse import urlencode

# -- 3rd party libraries --
import pytest
import requests

# -- Internal libraries --
import fsrapiclient.api

from fsrapiclient.api import FsrApiSession, FsrApiClient
from fsrapiclient.constants import FSR_API_CONSTANTS
from fsrapiclient.exceptions import FsrApiRequestException, FsrApiResponseException


class _TestFsrApi:

    _api_username = os.environ['API_USERNAME']
    _api_key = os.environ['API_KEY']


class TestFsrApiSession(_TestFsrApi):

    def test_fsr_api_session(self):
        test_session = FsrApiSession(self._api_username, self._api_key)

        assert test_session.api_username == self._api_username
        assert test_session.api_key == self._api_key
        assert test_session.headers == {
            'Accept': 'application/json',
            'X-Auth-Email': self._api_username,
            'X-Auth-Key': self._api_key
        }


class TestFsrApiClient(_TestFsrApi):

    def test_fsr_api_client____init__(self):
        test_client = FsrApiClient(self._api_username, self._api_key)

        assert test_client.api_session.api_username == self._api_username
        assert test_client.api_session.api_key == self._api_key
        assert test_client.api_session.headers == {
            'Accept': 'application/json',
            'X-Auth-Email': self._api_username,
            'X-Auth-Key': self._api_key
        }
        assert test_client.api_version == FSR_API_CONSTANTS.API_VERSION.value

    def test_fsr_api_client__common_search__api_request_exception_raised(self):
        test_client = FsrApiClient(self._api_username, self._api_key)

        with mock.patch('fsrapiclient.api.FsrApiSession.get') as mock_api_session_get:
            mock_api_session_get.side_effect = requests.RequestException('test RequestException')

            with pytest.raises(FsrApiRequestException):
                test_client.common_search(urlencode({'q': 'exceptional query', 'type': 'firm'}))

    def test_fsr_api_client__common_search__no_api_request_exception(self):
        test_client = FsrApiClient(self._api_username, self._api_key)

        recv_response = test_client.common_search(urlencode({'q': 'hastings direct', 'type': 'firm'}))
        assert recv_response.ok
        assert recv_response.fsr_data
        assert len(recv_response.fsr_data)
        assert recv_response.fsr_status == 'FSR-API-04-01-00'
        assert recv_response.fsr_message == 'Ok. Search successful'
        assert recv_response.fsr_resultinfo

        recv_response = test_client.common_search(urlencode({'q': 'non existent firm', 'type': 'firm'}))
        assert recv_response.ok
        assert not recv_response.fsr_data
        assert recv_response.fsr_status == 'FSR-API-04-01-11'
        assert recv_response.fsr_message == 'No search result found'
        assert not recv_response.fsr_resultinfo

    def test_fsr_api_client__search_frn__api_request_exception_raised(self):
        test_client = FsrApiClient(self._api_username, self._api_key)

        with mock.patch('fsrapiclient.api.FsrApiSession.get') as mock_api_session_get:
            mock_api_session_get.side_effect = requests.RequestException('test RequestException')

            with pytest.raises(FsrApiRequestException):
                test_client.search_frn('exceptional search')

    def test_fsr_api_client__search_frn__response_not_ok__api_response_exception_raised(self):
        test_client = FsrApiClient(self._api_username, self._api_key)

        with mock.patch('fsrapiclient.api.FsrApiClient.common_search', return_value=mock.MagicMock(ok=False)):
            with pytest.raises(FsrApiResponseException):
                test_client.search_frn('exceptional search')

    def test_fsr_api_client__search_frn__no_fsr_data_in_response__api_response_exception_raised(self):
        test_client = FsrApiClient(self._api_username, self._api_key)

        with mock.patch('fsrapiclient.api.FsrApiSession.get') as mock_api_session_get:
            mock_response = mock.create_autospec(requests.Response)
            mock_response.json = mock.MagicMock(name='json', return_value=dict())
            mock_api_session_get.return_value = mock_response

            with pytest.raises(FsrApiResponseException):
                test_client.search_frn('exceptional search')

    def test_fsr_api_client__search_frn__fsr_data_with_index_error__api_response_exception_raised(self):
        test_client = FsrApiClient(self._api_username, self._api_key)

        with mock.patch('fsrapiclient.api.FsrApiSession.get') as mock_api_session_get:
            mock_response = mock.create_autospec(requests.Response)
            mock_response.json = mock.MagicMock(name='json', return_value={'Data': []})
            mock_api_session_get.return_value = mock_response

            with pytest.raises(FsrApiResponseException):
                test_client.search_frn('exceptional search')

    def test_fsr_api_client__search_frn__fsr_data_with_key_error__api_response_exception_raised(self):
        test_client = FsrApiClient(self._api_username, self._api_key)

        with mock.patch('fsrapiclient.api.FsrApiSession.get') as mock_api_session_get:
            mock_response = mock.create_autospec(requests.Response)
            mock_response.json = mock.MagicMock(name='json', return_value={'Data': [{'not a Reference Number': None}]})
            mock_api_session_get.return_value = mock_response

            with pytest.raises(FsrApiResponseException):
                test_client.search_frn('exceptional search')

    def test_fsr_api_client__search_frn__no_request_exception(self):
        test_client = FsrApiClient(self._api_username, self._api_key)

        # Covers the case of a successful FRN search for an existing firm
        recv_frn = test_client.search_frn('hiscox insurance company')
        assert isinstance(recv_frn, str)
        assert recv_frn

        # Covers the case of a failed FRN search for an incorrectly specified firm
        with pytest.raises(FsrApiResponseException):
            test_client.search_frn('nonexistent123 insurance company')

        # Covers the case of an FRN search based on an inadequately specified firm
        # that produces multiple results
        with pytest.raises(FsrApiResponseException):
            test_client.search_frn('direct line')

    def test_fsr_api_client___firm_info__no_modifiers__request_exception_raised(self):
        test_client = FsrApiClient(self._api_username, self._api_key)

        with mock.patch('fsrapiclient.api.FsrApiSession.get') as mock_api_session_get:
            mock_api_session_get.side_effect = requests.RequestException('test RequestException')

            with pytest.raises(FsrApiRequestException):
                test_client._firm_info('test_frn')

    def test_fsr_api_client___firm_info__modifiers__request_exception_raised(self):
        test_client = FsrApiClient(self._api_username, self._api_key)

        with mock.patch('fsrapiclient.api.FsrApiSession.get') as mock_api_session_get:
            mock_api_session_get.side_effect = requests.RequestException('test RequestException')

            with pytest.raises(FsrApiRequestException):
                test_client._firm_info('test_frn', modifiers=('test_modifier1', 'test_modifier2',))

    def test_fsr_api_client___firm_info(self):
        test_client = FsrApiClient(self._api_username, self._api_key)

        # Covers the case of a request for an existing firm which is
        # Hiscox Insurance Company Limited with the FRN 113849
        recv_response = test_client._firm_info('113849')
        assert recv_response.ok
        assert recv_response.fsr_data
        assert recv_response.fsr_data[0]['Organisation Name'] == 'Hiscox Insurance Company Limited'

        # Covers the case of a request for an non-existent firm given by
        # a non-existent FRN 1234567890
        recv_response = test_client._firm_info('1234567890')
        assert recv_response.ok
        assert not recv_response.fsr_data

        # Covers the case of a request for the secondary or
        # alternative business or trading names used by Hiscox Insurance
        # Company Limited (FRN 113849)
        recv_response = test_client._firm_info('113849', modifiers=('Names',))
        assert recv_response.ok
        assert recv_response.fsr_data

        # Covers the case of a request for the secondary or alternative business
        # or trading names of a non-existent firm
        recv_response = test_client._firm_info('1234567890', modifiers=('Names',))
        assert recv_response.ok
        assert not recv_response.fsr_data

        # Covers the case of a request for the listed business
        # address of Hiscox Insurance Company Limited (FRN 113849)
        recv_response = test_client._firm_info('113849', modifiers=('Address',))
        assert recv_response.ok
        assert recv_response.fsr_data

        # Covers the case of a request for the listed business address of a non-
        # existent firm
        recv_response = test_client._firm_info('1234567890', modifiers=('Address',))
        assert recv_response.ok
        assert not recv_response.fsr_data

        # Covers the case of a request for the controlled functions
        # (CF) of Hiscox Insurance Company Limited (FRN 113849)
        recv_response = test_client._firm_info('113849', modifiers=('CF',))
        assert recv_response.ok
        assert recv_response.fsr_data

        # Covers the case of a request for the controlled functions (CF) of a
        # non-existent firm
        recv_response = test_client._firm_info('1234567890', modifiers=('CF',))
        assert recv_response.ok
        assert not recv_response.fsr_data

        # Covers the case of a request for the individuals
        # associated with Hiscox Insurance Company Limited (FRN 113849)
        recv_response = test_client._firm_info('113849', modifiers=('Individuals',))
        assert recv_response.ok
        assert recv_response.fsr_data

        # Covers the case of a request for the individuals associated with a
        # existent firm
        recv_response = test_client._firm_info('1234567890', modifiers=('Individuals',))
        assert recv_response.ok
        assert not recv_response.fsr_data

        # Covers the case of a request for the activities and
        # permissions associated with Hiscox Insurance Company Limited (FRN 113849)
        recv_response = test_client._firm_info('113849', modifiers=('Permissions',))
        assert recv_response.ok
        assert recv_response.fsr_data

        # Covers the case of a request for the activities and permissions
        # associated with a non-existent firm
        recv_response = test_client._firm_info('1234567890', modifiers=('Permissions',))
        assert recv_response.ok
        assert not recv_response.fsr_data

        # Covers the case of a request for the requirements
        # associated with Hiscox Insurance Company Limited (FRN 113849)
        recv_response = test_client._firm_info('113849', modifiers=('Requirements',))
        assert recv_response.ok
        assert recv_response.fsr_data

        # Covers the case of a request for the requirements associated with a
        # non-existent firm
        recv_response = test_client._firm_info('1234567890', modifiers=('Requirements',))
        assert recv_response.ok
        assert not recv_response.fsr_data

        # Covers the case of a request for the investment types
        # associated with a specific requirement associated with Hiscox Insurance
        # Company Limited (FRN 113849)
        recv_response = test_client._firm_info('113849', modifiers=('Requirements', 'OR-0131728', 'InvestmentTypes',))
        assert recv_response.ok
        assert not recv_response.fsr_data

        # Covers the case of a request for the regulators
        # listed for Hiscox Insurance Company Limited (FRN 113849)
        recv_response = test_client._firm_info('113849', modifiers=('Regulators',))
        assert recv_response.ok
        assert recv_response.fsr_data

        # Covers the case of a request for the regulators listed for a
        # non-existent firm
        recv_response = test_client._firm_info('1234567890', modifiers=('Regulators',))
        assert recv_response.ok
        assert not recv_response.fsr_data

        # Covers the case of a request for the passports
        # associated with Hiscox Insurance Company Limited (FRN 113849)
        recv_response = test_client._firm_info('113849', modifiers=('Passports',))
        assert recv_response.ok
        assert recv_response.fsr_data

        # Covers the case of a request for the passports associated with a
        # non-existent firm
        recv_response = test_client._firm_info('1234567890', modifiers=('Passports',))
        assert recv_response.ok
        assert not recv_response.fsr_data

        # Covers the case of a request for the passports
        # for a specific country, Gibraltar, associated with Hiscox Insurance Company Limited (FRN 113849)
        recv_response = test_client._firm_info('113849', modifiers=('Passports', 'Gibraltar', 'Permission',))
        assert recv_response.ok
        assert recv_response.fsr_data

        # Covers the case of a request for the passports for a specific country
        # associated with a non-existent firm
        recv_response = test_client._firm_info('1234567890', modifiers=('Passports', 'Gibraltar', 'Permission',))
        assert recv_response.ok
        assert not recv_response.fsr_data

        # Covers the case of a request for any waivers
        # associated with Hiscox Insurance Company Limited (FRN 113849)
        recv_response = test_client._firm_info('113849', modifiers=('Waivers',))
        assert recv_response.ok
        assert recv_response.fsr_data

        # Covers the case of a request for any waivers associated with a
        # non-existent firm
        recv_response = test_client._firm_info('1234567890', modifiers=('Waivers',))
        assert recv_response.ok
        assert not recv_response.fsr_data

        # Covers the case of a request for any exclusions
        # applying to Barclays Bank plc (FRN 122702)
        recv_response = test_client._firm_info('122702', modifiers=('Exclusions',))
        assert recv_response.ok
        assert recv_response.fsr_data

        # Covers the case of a request for any exclusions applying to a
        # non-existent firm
        recv_response = test_client._firm_info('1234567890', modifiers=('Exclusions',))
        assert recv_response.ok
        assert not recv_response.fsr_data

        # Covers the case of a request for the disciplinary history
        # of Barclays Bank plc (FRN 122702)
        recv_response = test_client._firm_info('122702', modifiers=('DisciplinaryHistory',))
        assert recv_response.ok
        assert recv_response.fsr_data

        # Covers the case of a request for the disciplinary history of a
        # non-existent firm
        recv_response = test_client._firm_info('1234567890', modifiers=('DisciplinaryHistory',))
        assert recv_response.ok
        assert not recv_response.fsr_data

        # Covers the case of a request for the appointed representatives of
        # Hiscox Insurance Company Limited (FRN 113849)
        recv_response = test_client._firm_info('113849', modifiers=('AR',))
        assert recv_response.ok
        assert (
            recv_response.fsr_data['PreviousAppointedRepresentatives'] or 
            recv_response.fsr_data['CurrentAppointedRepresentatives']
        )

        # Covers the case of a request for the appointed representatives
        # of a non-existent firm
        recv_response = test_client._firm_info('1234567890', modifiers=('AR',))
        assert recv_response.ok
        assert not recv_response.fsr_data['PreviousAppointedRepresentatives']
        assert not recv_response.fsr_data['CurrentAppointedRepresentatives']

    def test_fsr_api_client__get_firm(self):
        test_client = FsrApiClient(self._api_username, self._api_key)

        # Covers the case of a request for the firm details of
        # an existing firm, Hiscox Insurance Company Limited (FRN 113849)
        recv_response = test_client.get_firm('113849')
        assert recv_response.ok
        assert recv_response.fsr_data
        assert recv_response.fsr_data[0]['Organisation Name'] == 'Hiscox Insurance Company Limited'

        # Covers the case of a request for the firm details of
        # an existing firm, Hiscox Insurance Company Limited (FRN 113849)
        recv_response = test_client.get_firm('1234567890')
        assert recv_response.ok
        assert not recv_response.fsr_data

    def test_fsr_api_client__get_firm_names(self):
        test_client = FsrApiClient(self._api_username, self._api_key)

        # Covers the case of a request for an existing firm which is
        # Hiscox Insurance Company Limited (FRN 113849)
        recv_response = test_client.get_firm_names('113849')
        assert recv_response.ok
        assert recv_response.fsr_data
        assert recv_response.fsr_data[0]['Current Names'][0]['Name'] == 'Hiscox'
        assert recv_response.fsr_data[1]['Previous Names']

        # Covers the case of a request for an non-existent firm given by
        # a non-existent FRN 1234567890
        recv_response = test_client.get_firm_names('1234567890')
        assert recv_response.ok
        assert not recv_response.fsr_data

    def test_fsr_api_client__get_firm_addresses(self):
        test_client = FsrApiClient(self._api_username, self._api_key)

        # Covers the case of a request for an existing firm which is
        # Hiscox Insurance Company Limited (FRN 113849)
        recv_response = test_client.get_firm_addresses('113849')
        assert recv_response.ok
        assert recv_response.fsr_data

        # Covers the case of a request for an non-existent firm given by
        # a non-existent FRN 1234567890
        recv_response = test_client.get_firm_addresses('1234567890')
        assert recv_response.ok
        assert not recv_response.fsr_data

    def test_fsr_api_client__get_firm_controlled_functions(self):
        test_client = FsrApiClient(self._api_username, self._api_key)

        # Covers the case of a request for an existing firm which is
        # Hiscox Insurance Company Limited (FRN 113849)
        recv_response = test_client.get_firm_controlled_functions('113849')
        assert recv_response.ok
        assert recv_response.fsr_data

        # Covers the case of a request for an non-existent firm given by
        # a non-existent FRN 1234567890
        recv_response = test_client.get_firm_controlled_functions('1234567890')
        assert recv_response.ok
        assert not recv_response.fsr_data

    def test_fsr_api_client__get_firm_individuals(self):
        test_client = FsrApiClient(self._api_username, self._api_key)

        # Covers the case of a request for an existing firm which is
        # Hiscox Insurance Company Limited (FRN 113849)
        recv_response = test_client.get_firm_individuals('113849')
        assert recv_response.ok
        assert recv_response.fsr_data

        # Covers the case of a request for an non-existent firm given by
        # a non-existent FRN 1234567890
        recv_response = test_client.get_firm_individuals('1234567890')
        assert recv_response.ok
        assert not recv_response.fsr_data

    def test_fsr_api_client__get_firm_permissions(self):
        test_client = FsrApiClient(self._api_username, self._api_key)

        # Covers the case of a request for an existing firm which is
        # Hiscox Insurance Company Limited (FRN 113849)
        recv_response = test_client.get_firm_permissions('113849')
        assert recv_response.ok
        assert recv_response.fsr_data

        # Covers the case of a request for an non-existent firm given by
        # a non-existent FRN 1234567890
        recv_response = test_client.get_firm_permissions('1234567890')
        assert recv_response.ok
        assert not recv_response.fsr_data

    def test_fsr_api_client__get_firm_requirements(self):
        test_client = FsrApiClient(self._api_username, self._api_key)

        # Covers the case of a request for an existing firm which is
        # Hiscox Insurance Company Limited (FRN 113849)
        recv_response = test_client.get_firm_requirements('113849')
        assert recv_response.ok
        assert recv_response.fsr_data

        # Covers the case of a request for an non-existent firm given by
        # a non-existent FRN 1234567890
        recv_response = test_client.get_firm_requirements('1234567890')
        assert recv_response.ok
        assert not recv_response.fsr_data

    def test_fsr_api_client__get_firm_requirement_investment_types(self):
        test_client = FsrApiClient(self._api_username, self._api_key)

        # Covers the case of a request for an existing firm which is
        # Barclays Bank Plc (FRN 122702)
        recv_response = test_client.get_firm_requirement_investment_types('122702', 'OR-0262545')
        assert recv_response.ok
        assert recv_response.fsr_data

        # Covers the case of an unrequest for an existing firm which is
        # Barclays Bank Plc (FRN 122702)
        recv_response = test_client.get_firm_requirement_investment_types('122702', 'OR-1234567890')
        assert recv_response.ok
        assert not recv_response.fsr_data

        # Covers the case of a request for an non-existent firm given by
        # a non-existent FRN 1234567890
        recv_response = test_client.get_firm_requirement_investment_types('1234567890', 'OR-0262545')
        assert recv_response.ok
        assert not recv_response.fsr_data

    def test_fsr_api_client__get_firm_regulators(self):
        test_client = FsrApiClient(self._api_username, self._api_key)

        # Covers the case of a request for an existing firm which is
        # Hiscox Insurance Company Limited (FRN 113849)
        recv_response = test_client.get_firm_regulators('113849')
        assert recv_response.ok
        assert recv_response.fsr_data

        # Covers the case of a request for an non-existent firm given by
        # a non-existent FRN 1234567890
        recv_response = test_client.get_firm_regulators('1234567890')
        assert recv_response.ok
        assert not recv_response.fsr_data

    def test_fsr_api_client__get_firm_passports(self):
        test_client = FsrApiClient(self._api_username, self._api_key)

        # Covers the case of a request for an existing firm which is
        # Hiscox Insurance Company Limited (FRN 113849)
        recv_response = test_client.get_firm_passports('113849')
        assert recv_response.ok
        assert recv_response.fsr_data

        # Covers the case of a request for an non-existent firm given by
        # a non-existent FRN 1234567890
        recv_response = test_client.get_firm_passports('1234567890')
        assert recv_response.ok
        assert not recv_response.fsr_data

    def test_fsr_api_client__get_firm_passport_permissions(self):
        test_client = FsrApiClient(self._api_username, self._api_key)

        # Covers the case of a request for an existing firm which is
        # Hiscox Insurance Company Limited (FRN 113849)
        recv_response = test_client.get_firm_passport_permissions('113849', 'Gibraltar')
        assert recv_response.ok
        assert recv_response.fsr_data

        # Covers the case of a unrequest for an existing firm which is
        # Hiscox Insurance Comnpany Limited (FRN 113849)
        recv_response = test_client.get_firm_passport_permissions('113849', 'Germany')
        assert recv_response.ok
        assert not recv_response.fsr_data

        # Covers the case of a request for an non-existent firm given by
        # a non-existent FRN 1234567890
        recv_response = test_client.get_firm_passport_permissions('1234567890', 'Gibraltar')
        assert recv_response.ok
        assert not recv_response.fsr_data

    def test_fsr_api_client__get_firm_waivers(self):
        test_client = FsrApiClient(self._api_username, self._api_key)

        # Covers the case of a request for an existing firm which is
        # Hiscox Insurance Company Limited (FRN 113849)
        recv_response = test_client.get_firm_waivers('113849')
        assert recv_response.ok
        assert recv_response.fsr_data

        # Covers the case of a request for an non-existent firm given by
        # a non-existent FRN 1234567890
        recv_response = test_client.get_firm_waivers('1234567890')
        assert recv_response.ok
        assert not recv_response.fsr_data

    def test_fsr_api_client__get_firm_exclusions(self):
        test_client = FsrApiClient(self._api_username, self._api_key)

        # Covers the case of a request for an existing firm which is
        # Barclays Bank Plc (FRN 122702)
        recv_response = test_client.get_firm_exclusions('122702')
        assert recv_response.ok
        assert recv_response.fsr_data

        # Covers the case of an unrequest for an existing firm which is
        # Hiscox Insurance Company Limited (FRN 113849)
        recv_response = test_client.get_firm_exclusions('113849')
        assert recv_response.ok
        assert not recv_response.fsr_data

        # Covers the case of a request for an non-existent firm given by
        # a non-existent FRN 1234567890
        recv_response = test_client.get_firm_exclusions('1234567890')
        assert recv_response.ok
        assert not recv_response.fsr_data

    def test_fsr_api_client__get_firm_disciplinary_history(self):
        test_client = FsrApiClient(self._api_username, self._api_key)

        # Covers the case of a request for an existing firm which is
        # Barclays Bank Plc (FRN 122702)
        recv_response = test_client.get_firm_disciplinary_history('122702')
        assert recv_response.ok
        assert recv_response.fsr_data

        # Covers the case of an unrequest for an existing firm which is
        # Hiscox Insurance Company Limited (FRN 113849)
        recv_response = test_client.get_firm_disciplinary_history('113849')
        assert recv_response.ok
        assert not recv_response.fsr_data

        # Covers the case of a request for an non-existent firm given by
        # a non-existent FRN 1234567890
        recv_response = test_client.get_firm_disciplinary_history('1234567890')
        assert recv_response.ok
        assert not recv_response.fsr_data

    def test_fsr_api_client__get_firm_appointed_representatives(self):
        test_client = FsrApiClient(self._api_username, self._api_key)

        # Covers the case of a request for an existing firm which is
        # Hiscox Insurance Company Limited (FRN 113849)
        recv_response = test_client.get_firm_appointed_representatives('113849')
        assert recv_response.ok
        assert recv_response.fsr_data
        assert any([
            recv_response.fsr_data['PreviousAppointedRepresentatives'],
            recv_response.fsr_data['CurrentAppointedRepresentatives']
        ])

        # Covers the case of a request for an non-existent firm given by
        # a non-existent FRN 1234567890
        recv_response = test_client.get_firm_appointed_representatives('1234567890')
        assert recv_response.ok
        assert not any([
            recv_response.fsr_data['PreviousAppointedRepresentatives'],
            recv_response.fsr_data['CurrentAppointedRepresentatives']
        ])

    def test_fsr_api_client__search_irn__api_request_exception_raised(self):
        test_client = FsrApiClient(self._api_username, self._api_key)

        with mock.patch('fsrapiclient.api.FsrApiSession.get') as mock_api_session_get:
            mock_api_session_get.side_effect = requests.RequestException('test RequestException')

            with pytest.raises(FsrApiRequestException):
                test_client.search_irn('exceptional search')

    def test_fsr_api_client__search_irn__response_not_ok__api_response_exception_raised(self):
        test_client = FsrApiClient(self._api_username, self._api_key)

        with mock.patch('fsrapiclient.api.FsrApiClient.common_search', return_value=mock.MagicMock(ok=False)):
            with pytest.raises(FsrApiResponseException):
                test_client.search_irn('exceptional search')

    def test_fsr_api_client__search_irn__no_fsr_data_in_response__api_response_exception_raised(self):
        test_client = FsrApiClient(self._api_username, self._api_key)

        with mock.patch('fsrapiclient.api.FsrApiSession.get') as mock_api_session_get:
            mock_response = mock.create_autospec(requests.Response)
            mock_response.json = mock.MagicMock(name='json', return_value=dict())
            mock_api_session_get.return_value = mock_response

            with pytest.raises(FsrApiResponseException):
                test_client.search_irn('exceptional search')

    def test_fsr_api_client__search_irn__fsr_data_with_index_error__api_response_exception_raised(self):
        test_client = FsrApiClient(self._api_username, self._api_key)

        with mock.patch('fsrapiclient.api.FsrApiSession.get') as mock_api_session_get:
            mock_response = mock.create_autospec(requests.Response)
            mock_response.json = mock.MagicMock(name='json', return_value={'Data': []})
            mock_api_session_get.return_value = mock_response

            with pytest.raises(FsrApiResponseException):
                test_client.search_irn('exceptional search')

    def test_fsr_api_client__search_irn__fsr_data_with_key_error__api_response_exception_raised(self):
        test_client = FsrApiClient(self._api_username, self._api_key)

        with mock.patch('fsrapiclient.api.FsrApiSession.get') as mock_api_session_get:
            mock_response = mock.create_autospec(requests.Response)
            mock_response.json = mock.MagicMock(name='json', return_value={'Data': [{'not a Reference Number': None}]})
            mock_api_session_get.return_value = mock_response

            with pytest.raises(FsrApiResponseException):
                test_client.search_irn('exceptional search')

    def test_fsr_api_client__search_irn__no_api_request_exception(self):
        test_client = FsrApiClient(self._api_username, self._api_key)

        # Covers the case of a successful IRN searh for an existing individual
        recv_frn = test_client.search_irn('mark carney')
        assert isinstance(recv_frn, str)
        assert recv_frn

        # Covers the case of a failed IRN search for an incorrectly specified individual
        with pytest.raises(FsrApiResponseException):
            test_client.search_irn('a nonexistent person')

        # Covers the case of an IRN search based on an inadequately specified individual
        # that produces multiple results
        with pytest.raises(FsrApiResponseException):
            test_client.search_irn('mark C')

    def test_fsr_api_client___individual_info__no_modifiers__request_exception_raised_and_propagated(self):
        test_client = FsrApiClient(self._api_username, self._api_key)

        with mock.patch('fsrapiclient.api.FsrApiSession.get') as mock_api_session_get:
            mock_api_session_get.side_effect = requests.RequestException('test RequestException')

            with pytest.raises(FsrApiRequestException):
                test_client._individual_info('test_irn')

    def test_fsr_api_client___individual_info__modifiers__request_exception_raised_and_propagated(self):
        test_client = FsrApiClient(self._api_username, self._api_key)

        with mock.patch('fsrapiclient.api.FsrApiSession.get') as mock_api_session_get:
            mock_api_session_get.side_effect = requests.RequestException('test RequestException')

            with pytest.raises(FsrApiRequestException):
                test_client._individual_info('test_irn', modifiers=('test_modifier1', 'test_modifier2',))

    def test_fsr_api_client___individual_info(self):
        test_client = FsrApiClient(self._api_username, self._api_key)

        # Covers the case of a request for an existing individual
        # 'Mark Carney'(IRN 'MXC29012')
        recv_response = test_client._individual_info('MXC29012')
        assert recv_response.ok
        assert recv_response.fsr_data
        assert recv_response.fsr_data[0]['Details']['Full Name'] == 'Mark Carney'

        # Covers the case of a request for an non-existent individual
        recv_response = test_client._individual_info('1234567890')
        assert recv_response.ok
        assert not recv_response.fsr_data

        # Covers the case of a request for the controlled functions
        # associated with an existing individual, 'Mark Carney'
        recv_response = test_client._individual_info('MXC29012', modifiers=('CF',))
        assert recv_response.ok
        assert recv_response.fsr_data

        # Covers the case of a request for the controlled functions associated
        # with a non-existent individual
        recv_response = test_client._individual_info('1234567890', modifiers=('CF',))
        assert recv_response.ok
        assert not recv_response.fsr_data

        # Covers the case of a request for the disciplinary history
        # of an individual, 'Leigh Mackey' (IRN 'LXM01328')
        recv_response = test_client._individual_info('LXM01328', modifiers=('DisciplinaryHistory',))
        assert recv_response.ok
        assert recv_response.fsr_data

        # Covers the case of an unrequest for the disciplinary history
        # of an individual, 'Mark Carney' (IRN 'MXC29012')
        recv_response = test_client._individual_info('MXC29012', modifiers=('DisciplinaryHistory',))
        assert recv_response.ok
        assert not recv_response.fsr_data

        # Covers the case of a request for the disciplinary history of a non-
        # existent individual
        recv_response = test_client._firm_info('1234567890', modifiers=('DisciplinaryHistory',))
        assert recv_response.ok
        assert not recv_response.fsr_data

    def test_fsr_api_client__get_individual(self):
        test_client = FsrApiClient(self._api_username, self._api_key)

        # Covers the case of a request for the details of an
        # existing individual, 'Mark Carney' (IRN 'MXC29012')
        recv_response = test_client.get_individual('MXC29012')
        assert recv_response.ok
        assert recv_response.fsr_data
        assert recv_response.fsr_data[0]['Details']['Full Name'] == 'Mark Carney'

        # Covers the case of a request for the details of a non-existent individual
        recv_response = test_client.get_individual('1234567890')
        assert recv_response.ok
        assert not recv_response.fsr_data

    def test_fsr_api_client__get_individual_controlled_functions(self):
        test_client = FsrApiClient(self._api_username, self._api_key)

        # Covers the case of a request for an existing individual -
        # 'Mark Carney' (IRN 'MXC29012')
        recv_response = test_client.get_individual_controlled_functions('MXC29012')
        assert recv_response.ok
        assert recv_response.fsr_data

        # Covers the case of a request for an non-existent individual given by
        # a non-existent IRN '1234567890'
        recv_response = test_client.get_individual_controlled_functions('1234567890')
        assert recv_response.ok
        assert not recv_response.fsr_data

    def test_fsr_api_client__get_individual_disciplinary_history(self):
        test_client = FsrApiClient(self._api_username, self._api_key)

        # Covers the case of a request for an existing individual with -
        # disciplinary history, 'Leigh Mackey' (IRN 'LXM01328')
        recv_response = test_client.get_individual_disciplinary_history('LXM01328')
        assert recv_response.ok
        assert recv_response.fsr_data

        # Covers the case of a request for an non-existent individual given by
        # a non-existent IRN '1234567890'
        recv_response = test_client.get_individual_disciplinary_history('1234567890')
        assert recv_response.ok
        assert not recv_response.fsr_data

    def test_fsr_api_client__search_prn__api_request_exception_raised(self):
        test_client = FsrApiClient(self._api_username, self._api_key)

        with mock.patch('fsrapiclient.api.FsrApiSession.get') as mock_api_session_get:
            mock_api_session_get.side_effect = requests.RequestException('test RequestException')

            with pytest.raises(FsrApiRequestException):
                test_client.search_prn('exceptional search')

    def test_fsr_api_client__search_prn__response_not_ok__api_response_exception_raised(self):
        test_client = FsrApiClient(self._api_username, self._api_key)

        with mock.patch('fsrapiclient.api.FsrApiClient.common_search', return_value=mock.MagicMock(ok=False)):
            with pytest.raises(FsrApiResponseException):
                test_client.search_prn('exceptional search')

    def test_fsr_api_client__search_prn__no_fsr_data_in_response__api_response_exception_raised(self):
        test_client = FsrApiClient(self._api_username, self._api_key)

        with mock.patch('fsrapiclient.api.FsrApiSession.get') as mock_api_session_get:
            mock_response = mock.create_autospec(requests.Response)
            mock_response.json = mock.MagicMock(name='json', return_value=dict())
            mock_api_session_get.return_value = mock_response

            with pytest.raises(FsrApiResponseException):
                test_client.search_prn('exceptional search')

    def test_fsr_api_client__search_prn__fsr_data_with_index_error__api_response_exception_raised(self):
        test_client = FsrApiClient(self._api_username, self._api_key)

        with mock.patch('fsrapiclient.api.FsrApiSession.get') as mock_api_session_get:
            mock_response = mock.create_autospec(requests.Response)
            mock_response.json = mock.MagicMock(name='json', return_value={'Data': []})
            mock_api_session_get.return_value = mock_response

            with pytest.raises(FsrApiResponseException):
                test_client.search_prn('exceptional search')

    def test_fsr_api_client__search_prn__fsr_data_with_key_error__api_response_exception_raised(self):
        test_client = FsrApiClient(self._api_username, self._api_key)

        with mock.patch('fsrapiclient.api.FsrApiSession.get') as mock_api_session_get:
            mock_response = mock.create_autospec(requests.Response)
            mock_response.json = mock.MagicMock(name='json', return_value={'Data': [{'not a Reference Number': None}]})
            mock_api_session_get.return_value = mock_response

            with pytest.raises(FsrApiResponseException):
                test_client.search_prn('exceptional search')

    def test_fsr_api_client__search_prn__no_api_request_exception(self):
        test_client = FsrApiClient(self._api_username, self._api_key)

        # Covers the case of a successful PRN searh for an existing fund
        recv_prn = test_client.search_prn('jupiter asia pacific income fund')
        assert isinstance(recv_prn, str)
        assert recv_prn

        # Covers the case of a failed PRN search for an incorrectly specified fund
        with pytest.raises(FsrApiResponseException):
            test_client.search_prn('a nonexistent fund')

        # Covers the case of a PRN search based on an inadequately specified fund
        # name that produces multiple results
        with pytest.raises(FsrApiResponseException):
            test_client.search_prn('jupiter asia pacific')

    def test_fsr_api_client___fund_info__no_modifiers__request_exception_raised(self):
        test_client = FsrApiClient(self._api_username, self._api_key)

        with mock.patch('fsrapiclient.api.FsrApiSession.get') as mock_api_session_get:
            mock_api_session_get.side_effect = requests.RequestException('test RequestException')

            with pytest.raises(FsrApiRequestException):
                test_client._fund_info('test_prn')

    def test_fsr_api_client___fund_info__modifiers__request_exception_raised(self):
        test_client = FsrApiClient(self._api_username, self._api_key)

        with mock.patch('fsrapiclient.api.FsrApiSession.get') as mock_api_session_get:
            mock_api_session_get.side_effect = requests.RequestException('test RequestException')

            with pytest.raises(FsrApiRequestException):
                test_client._fund_info('test_prn', modifiers=('test_modifier1', 'test_modifier2',))

    def test_fsr_api_client___fund_info(self):
        test_client = FsrApiClient(self._api_username, self._api_key)

        # Covers the case of a request for an existing fund which is
        # 'Jupiter Asia Pacific Income Fund (IRL)' with the PRN 1006826
        recv_response = test_client._fund_info('1006826')
        assert recv_response.ok
        assert recv_response.fsr_data

        # Covers the case of a request for an non-existent fund given by
        # a non-existent PRN 1234567890
        recv_response = test_client._fund_info('1234567890')
        assert recv_response.ok
        assert not recv_response.fsr_data

        # Covers the case of a request for the subfund details of an
        # existing fund with PRN 185045
        recv_response = test_client._fund_info('185045', modifiers=('Subfund',))
        assert recv_response.ok
        assert recv_response.fsr_data

        # Covers the case of a request for the non-existent subfund details of an
        # existing fund with PRN 1006826
        recv_response = test_client._fund_info('1006826', modifiers=('Subfund',))
        assert recv_response.ok
        assert not recv_response.fsr_data

        # Covers the case of a request for the non-existent subfund details
        # of a non-existent fund
        recv_response = test_client._fund_info('1234567890', modifiers=('Subfund',))
        assert recv_response.ok
        assert not recv_response.fsr_data

        # Covers the case of a request for the alternative or secondary trading
        # names of an existing fund with PRN 185045
        recv_response = test_client._fund_info('185045', modifiers=('Names',))
        assert recv_response.ok
        assert recv_response.fsr_data

        # Covers the case of a request for the non-existent alternative or
        # secondary trading names of an existing fund with PRN 1006826
        recv_response = test_client._fund_info('1006826', modifiers=('Names',))
        assert recv_response.ok
        assert not recv_response.fsr_data

        # Covers the case of a request for the non-existent alternative or
        # secondary trading names of a non-existing fund with a non-existent
        # PRN 1234567890
        recv_response = test_client._fund_info('1234567890', modifiers=('Names',))
        assert recv_response.ok
        assert not recv_response.fsr_data

    def test_fsr_api_client__get_fund(self):
        test_client = FsrApiClient(self._api_username, self._api_key)

        # Covers the case of a request for the details of an
        # existing fund, 'Jupiter Asia Pacific Income Fund (IRL)' (PRN '635641')
        recv_response = test_client.get_fund('635641')
        assert recv_response.ok
        assert recv_response.fsr_data

        # Covers the case of a request for the details of a non-existent fund
        recv_response = test_client.get_fund('1234567890')
        assert recv_response.ok
        assert not recv_response.fsr_data

    def test_fsr_api_client__get_fund_names(self):
        test_client = FsrApiClient(self._api_username, self._api_key)

        # Covers the case of a request for the alternate/secondary names
        # details of existing fund with PRN 185045
        recv_response = test_client.get_fund_names('185045')
        assert recv_response.ok
        assert recv_response.fsr_data

        # Covers the case of a request for the alternate/secondary name
        # details of an existing fund with PRN 1006826
        recv_response = test_client.get_fund_names('1006826')
        assert recv_response.ok
        assert not recv_response.fsr_data

        # Covers the case of a request for the alternate/secondary name
        # details of a non-existent fund
        recv_response = test_client.get_fund_names('1234567890')
        assert recv_response.ok
        assert not recv_response.fsr_data

    def test_fsr_api_client__get_fund_subfunds(self):
        test_client = FsrApiClient(self._api_username, self._api_key)

        # Covers the case of a request for the subfund details of an
        # existing fund with PRN 185045
        recv_response = test_client.get_fund_subfunds('185045')
        assert recv_response.ok
        assert recv_response.fsr_data

        # Covers the case of a request for the subfund details of an
        # existing fund with PRN 1006826
        recv_response = test_client.get_fund_subfunds('1006826')
        assert recv_response.ok
        assert not recv_response.fsr_data

        # Covers the case of a request for the subfund details of a
        # non-existent fund
        recv_response = test_client.get_fund_subfunds('1234567890')
        assert recv_response.ok
        assert not recv_response.fsr_data