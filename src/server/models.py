from typing import Dict, List, Any
from dataclasses import dataclass
import numpy as np


@dataclass
class RunRequest:
    """Request model for /run endpoint."""
    matrix: np.ndarray
    mask: np.ndarray

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RunRequest':
        """
        Create RunRequest from dictionary.

        Args:
            data: Dictionary containing matrix and mask

        Returns:
            RunRequest instance
        """
        matrix = np.array(data['matrix'], dtype=float)
        mask = np.array(data['mask'], dtype=int)
        return cls(matrix=matrix, mask=mask)


@dataclass
class RunResponse:
    """Response model for /run endpoint."""
    metrics: Dict[str, float]

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert response to dictionary.

        Returns:
            Dictionary representation of response
        """
        return {"metrics": self.metrics}


@dataclass
class ErrorResponse:
    """Error response model."""
    error: str

    def to_dict(self) -> Dict[str, str]:
        """
        Convert error response to dictionary.

        Returns:
            Dictionary representation of error
        """
        return {"error": self.error}
