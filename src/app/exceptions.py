"""All exceptions for the API app."""


class DBConnectionException(BaseException):
    """Exception for DB connection issues."""

    pass


class SegmentVariantNotDefined(BaseException):
    """Exception for segment not yet defined."""

    pass
