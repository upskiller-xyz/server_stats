import numpy as np
from typing import Optional
from .base import BaseMetric


class ValidAreaMetric(BaseMetric):
    """Calculate percentage of masked area with values over 1."""

    @classmethod
    def calculate(cls, values: np.ndarray, mask: Optional[np.ndarray] = None) -> float:
        """
        Calculate percentage of valid area with values over 1.

        Args:
            values: Input image values
            mask: Optional boolean mask for valid pixels

        Returns:
            float: Percentage (0-100) of masked area with values > 1
        """
        if mask is None:
            mask = np.ones_like(values, dtype=bool)
        else:
            mask = mask.astype(bool)

        masked_values = values[mask]
        if len(masked_values) == 0:
            return cls._invalid(0.0)

        values_over_one = np.sum(masked_values > 1)
        total_masked = len(masked_values)

        percentage = (values_over_one / total_masked) * 100.0
        return float(percentage)

    @classmethod
    def compare(cls, ground_truth: np.ndarray, simulation: np.ndarray, mask: Optional[np.ndarray] = None) -> float:
        """
        Compare two images by calculating difference in valid area percentages.

        Args:
            ground_truth: Ground truth image values
            simulation: Simulated image values
            mask: Optional boolean mask for valid pixels

        Returns:
            float: Difference between the valid area percentages
        """
        gt_percentage = cls.calculate(ground_truth, mask)
        sim_percentage = cls.calculate(simulation, mask)

        if np.isnan(gt_percentage) or np.isnan(sim_percentage):
            return cls._invalid(0.0)
        return gt_percentage - sim_percentage

    @classmethod
    def _invalid(cls, threshold: float) -> dict:
        return float('nan')
