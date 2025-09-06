"""Exceptions module."""


class PdfToolBaseError(Exception):
    """PDF Tool Base Exception."""


class PdfReorganizeInvalidIndexesError(PdfToolBaseError):
    """PDF Reorganize Invalid indexes."""
