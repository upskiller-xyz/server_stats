from src.components.extended_enum import ExtendedEnum


class ServerConfig(ExtendedEnum):
    """Server configuration constants."""
    DEFAULT_PORT = 5000
    DEFAULT_HOST = "0.0.0.0"
    MAX_CONTENT_LENGTH = 16777216  # 16MB


class HttpStatusCode(ExtendedEnum):
    """HTTP status codes."""
    OK = 200
    BAD_REQUEST = 400
    INTERNAL_SERVER_ERROR = 500


class RouteEndpoints(ExtendedEnum):
    """API route endpoints."""
    RUN = "/run"
    HEALTH = "/health"


class ResponseKeys(ExtendedEnum):
    """Response JSON keys."""
    ERROR = "error"
    METRICS = "metrics"
    STATUS = "status"


class RequestKeys(ExtendedEnum):
    """Request JSON keys."""
    MATRIX = "matrix"
    MASK = "mask"


class ValidationMessages(ExtendedEnum):
    """Validation error messages."""
    MISSING_MATRIX = "Missing 'matrix' in request body"
    MISSING_MASK = "Missing 'mask' in request body"
    INVALID_MATRIX_TYPE = "Matrix must be a list or array"
    INVALID_MASK_TYPE = "Mask must be a list or array"
    SHAPE_MISMATCH = "Matrix and mask must have the same dimensions"
    INVALID_MATRIX_VALUES = "Matrix values must be floats between 0 and 10"
    INVALID_MASK_VALUES = "Mask values must be binary (0 or 1)"
    EMPTY_MATRIX = "Matrix cannot be empty"
    NO_VALID_MASK_AREA = "Mask must contain at least one value of 1"
