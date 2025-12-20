import numpy as np
from typing import Optional
from .base import BaseMetric


class MaxMetric(BaseMetric):
    """Calculate maximum of masked values."""

    @classmethod
    def calculate(cls, values: np.ndarray, mask: Optional[np.ndarray] = None) -> float:
        """
        Calculate maximum for single image input.

        Args:
            values: Input image values
            mask: Optional boolean mask for valid pixels

        Returns:
            float: Maximum of valid pixels
        """
        if mask is None:
            return float(np.max(values))

        mask = mask.astype(bool)

        masked_values = values[mask]
        if len(masked_values) == 0:
            return cls._invalid(0.0)

        return float(np.max(masked_values))

    @classmethod
    def compare(cls, ground_truth: np.ndarray, simulation: np.ndarray, mask: Optional[np.ndarray] = None) -> float:
        """
        Compare two images by calculating maximum difference.

        Args:
            ground_truth: Ground truth image values
            simulation: Simulated image values
            mask: Optional boolean mask for valid pixels

        Returns:
            float: Difference between the maximums
        """
        gt_max = cls.calculate(ground_truth, mask)
        sim_max = cls.calculate(simulation, mask)

        if np.isnan(gt_max) or np.isnan(sim_max):
            return cls._invalid(0.0)
        return gt_max - sim_max

    @classmethod
    def _invalid(cls, threshold: float) -> dict:
        return float('nan')
