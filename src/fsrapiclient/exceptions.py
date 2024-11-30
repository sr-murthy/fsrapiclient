__all__ = ['FsrApiException',
           'FsrApiRequestException',
           'FsrApiResponseException',]


# -- IMPORTS --

# -- Standard libraries --

# -- 3rd party libraries --

# -- Internal libraries --


class FsrApiException(Exception):
    ...


class FsrApiRequestException(FsrApiException):
    ...


class FsrApiResponseException(FsrApiException):
    ...
