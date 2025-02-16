# -- IMPORTS --

# -- Standard libraries --

# -- 3rd party libraries --

# -- Internal libraries --
from fsrapiclient.constants import FSR_API_CONSTANTS


class TestFsrApiConstants:

	def test_fsr_api_constants(self):
		assert FSR_API_CONSTANTS.API_VERSION.value == 'V0.1'
		assert FSR_API_CONSTANTS.BASEURL.value == 'https://register.fca.org.uk/services/V0.1'
		assert FSR_API_CONSTANTS.RESOURCE_TYPES.value == {
			'firm': {'type_name': 'firm', 'endpoint_base': 'Firm'},
			'fund': {'type_name': 'fund', 'endpoint_base': 'CIS'},
			'individual': {'type_name': 'individual', 'endpoint_base': 'Individuals'}
		}
