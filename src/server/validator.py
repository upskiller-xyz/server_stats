from typing import Dict, Any, Optional
import numpy as np
from src.server.constants import ValidationMessages, RequestKeys


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


class RequestValidator:
    """
    Validates incoming requests for the /run endpoint.
    Follows Single Responsibility Principle.
    """

    def __init__(self, min_value: float = 0.0, max_value: float = 10.0):
        """
        Initialize validator with value constraints.

        Args:
            min_value: Minimum allowed matrix value
            max_value: Maximum allowed matrix value
        """
        self._min_value = min_value
        self._max_value = max_value

    def validate(self, data: Dict[str, Any]) -> None:
        """
        Validate request data.

        Args:
            data: Request data dictionary

        Raises:
            ValidationError: If validation fails
        """
        self._validate_required_fields(data)
        matrix = self._validate_matrix(data[RequestKeys.MATRIX.value])
        mask = self._validate_mask(data[RequestKeys.MASK.value])
        self._validate_dimensions(matrix, mask)
        self._validate_mask_has_valid_area(mask)

    def _validate_required_fields(self, data: Dict[str, Any]) -> None:
        """
        Validate that required fields are present.

        Args:
            data: Request data dictionary

        Raises:
            ValidationError: If required fields are missing
        """
        if RequestKeys.MATRIX.value not in data:
            raise ValidationError(ValidationMessages.MISSING_MATRIX.value)

        if RequestKeys.MASK.value not in data:
            raise ValidationError(ValidationMessages.MISSING_MASK.value)

    def _validate_matrix(self, matrix_data: Any) -> np.ndarray:
        """
        Validate and convert matrix data.

        Args:
            matrix_data: Raw matrix data

        Returns:
            Validated numpy array

        Raises:
            ValidationError: If matrix validation fails
        """
        if not isinstance(matrix_data, (list, np.ndarray)):
            raise ValidationError(ValidationMessages.INVALID_MATRIX_TYPE.value)

        try:
            matrix = np.array(matrix_data, dtype=float)
        except (ValueError, TypeError):
            raise ValidationError(ValidationMessages.INVALID_MATRIX_VALUES.value)

        if matrix.size == 0:
            raise ValidationError(ValidationMessages.EMPTY_MATRIX.value)

        if not self._check_value_range(matrix):
            raise ValidationError(ValidationMessages.INVALID_MATRIX_VALUES.value)

        return matrix

    def _validate_mask(self, mask_data: Any) -> np.ndarray:
        """
        Validate and convert mask data.

        Args:
            mask_data: Raw mask data

        Returns:
            Validated numpy array

        Raises:
            ValidationError: If mask validation fails
        """
        if not isinstance(mask_data, (list, np.ndarray)):
            raise ValidationError(ValidationMessages.INVALID_MASK_TYPE.value)

        try:
            mask = np.array(mask_data, dtype=int)
        except (ValueError, TypeError):
            raise ValidationError(ValidationMessages.INVALID_MASK_VALUES.value)

        if not self._check_binary_values(mask):
            raise ValidationError(ValidationMessages.INVALID_MASK_VALUES.value)

        return mask

    def _validate_dimensions(self, matrix: np.ndarray, mask: np.ndarray) -> None:
        """
        Validate that matrix and mask have matching dimensions.

        Args:
            matrix: Matrix array
            mask: Mask array

        Raises:
            ValidationError: If dimensions don't match
        """
        if matrix.shape != mask.shape:
            raise ValidationError(ValidationMessages.SHAPE_MISMATCH.value)

    def _validate_mask_has_valid_area(self, mask: np.ndarray) -> None:
        """
        Validate that mask contains at least one valid area (value of 1).

        Args:
            mask: Mask array

        Raises:
            ValidationError: If no valid area exists
        """
        if not np.any(mask == 1):
            raise ValidationError(ValidationMessages.NO_VALID_MASK_AREA.value)

    def _check_value_range(self, matrix: np.ndarray) -> bool:
        """
        Check if all matrix values are within valid range.

        Args:
            matrix: Matrix array

        Returns:
            True if all values are valid, False otherwise
        """
        return bool(np.all((matrix >= self._min_value) & (matrix <= self._max_value)))

    def _check_binary_values(self, mask: np.ndarray) -> bool:
        """
        Check if all mask values are binary (0 or 1).

        Args:
            mask: Mask array

        Returns:
            True if all values are binary, False otherwise
        """
        unique_values = np.unique(mask)
        return bool(np.all((unique_values == 0) | (unique_values == 1)))
