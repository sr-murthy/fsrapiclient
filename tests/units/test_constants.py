# -- IMPORTS --

# -- Standard libraries --

# -- 3rd party libraries --

# -- Internal libraries --
from fsrapiclient.constants import FSR_API_CONSTANTS


class TestFsrApiConstants:

	def test_fsr_api_constants(self):
		assert FSR_API_CONSTANTS.BASEURL.value == 'https://register.fca.org.uk/services'
		assert FSR_API_CONSTANTS.API_VERSION.value == 'V0.1'
		assert FSR_API_CONSTANTS.RESOURCE_TYPE_FIRM.value == 'firm'
		assert FSR_API_CONSTANTS.RESOURCE_TYPE_INDIVIDUAL.value == 'individual'
		assert FSR_API_CONSTANTS.RESOURCE_TYPE_FUND.value == 'fund'
