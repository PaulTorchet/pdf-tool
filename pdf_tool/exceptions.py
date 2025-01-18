"""Exceptions module."""


class PdfToolBaseException(Exception):
    """PDF Tool Base Exception."""


class PdfReorganizeInvalidIndexesException(PdfToolBaseException):
    """PDF Reorganize Invalid indexes."""
