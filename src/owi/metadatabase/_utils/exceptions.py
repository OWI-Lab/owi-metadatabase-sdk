"""
Custom exceptions for the API client. These exceptions encapsulate
common errors that can occur during API calls and data post-processing.
"""

from typing import Optional

import requests


class APIException(Exception):
    """
    Base exception for all errors raised by API.

    This is the parent class for all custom exceptions in the package.
    It provides a consistent interface for error handling across API operations.

    Parameters
    ----------
    message : str
        Human-readable error message describing what went wrong.

    Examples
    --------
    >>> exc = APIException("Something went wrong")
    >>> str(exc)
    'Something went wrong'
    >>> exc.message
    'Something went wrong'
    """

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return self.message


class APIConnectionError(APIException):
    """
    Exception raised when the API cannot be reached or returns a failure.

    This exception is raised when there are network issues, server errors,
    or other connection-related problems during API communication.

    Parameters
    ----------
    message : str
        Human-readable error message.
    response : requests.Response or None, optional
        The HTTP response object if available, default is None.

    Examples
    --------
    >>> exc = APIConnectionError("Network timeout")
    >>> str(exc)
    'Network timeout'
    >>> exc.message
    'Network timeout'
    """

    def __init__(self, message: str, response: Optional[requests.Response] = None) -> None:
        self.response = response
        super().__init__(message)

    def __str__(self) -> str:
        status = f" (Status: {self.response.status_code})" if self.response else ""
        return f"{self.message}{status}"


class DataNotFoundError(APIException):
    """
    Exception raised when no data is found for the given query parameters.

    This exception indicates that the API request was successful but returned
    no results matching the search criteria.

    Parameters
    ----------
    message : str, optional
        Human-readable error message, default is "No data found for the given search criteria."

    Examples
    --------
    >>> exc = DataNotFoundError()
    >>> str(exc)
    'No data found for the given search criteria.'

    >>> exc = DataNotFoundError("No turbine T99 in project")
    >>> str(exc)
    'No turbine T99 in project'
    """

    def __init__(self, message: str = "No data found for the given search criteria.") -> None:
        super().__init__(message)


class DataProcessingError(APIException):
    """
    Exception raised when there is a problem while processing the data.

    This exception indicates that data was retrieved successfully from the API
    but could not be processed, transformed, or validated correctly.

    Parameters
    ----------
    message : str, optional
        Human-readable error message, default is "Error during data processing."

    Examples
    --------
    >>> exc = DataProcessingError()
    >>> str(exc)
    'Error during data processing.'

    >>> exc = DataProcessingError("Cannot parse geometry coordinates")
    >>> str(exc)
    'Cannot parse geometry coordinates'
    """

    def __init__(self, message: str = "Error during data processing.") -> None:
        super().__init__(message)


class InvalidParameterError(APIException):
    """
    Exception raised when query parameters are invalid or missing.

    This exception is raised before making API requests when the provided
    parameters fail validation checks or are inconsistent.

    Parameters
    ----------
    message : str, optional
        Human-readable error message, default is "Invalid or missing parameters for the request."

    Examples
    --------
    >>> exc = InvalidParameterError()
    >>> str(exc)
    'Invalid or missing parameters for the request.'

    >>> exc = InvalidParameterError("Project name required")
    >>> str(exc)
    'Project name required'
    """

    def __init__(self, message: str = "Invalid or missing parameters for the request.") -> None:
        super().__init__(message)
