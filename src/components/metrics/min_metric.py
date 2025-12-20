import numpy as np
from typing import Optional
from .base import BaseMetric


class MinMetric(BaseMetric):
    """Calculate minimum of masked values."""

    @classmethod
    def calculate(cls, values: np.ndarray, mask: Optional[np.ndarray] = None) -> float:
        """
        Calculate minimum for single image input.

        Args:
            values: Input image values
            mask: Optional boolean mask for valid pixels

        Returns:
            float: Minimum of valid pixels
        """
        if mask is None:
            return float(np.min(values))

        mask = mask.astype(bool)

        masked_values = values[mask]
        if len(masked_values) == 0:
            return cls._invalid(0.0)

        return float(np.min(masked_values))

    @classmethod
    def compare(cls, ground_truth: np.ndarray, simulation: np.ndarray, mask: Optional[np.ndarray] = None) -> float:
        """
        Compare two images by calculating minimum difference.

        Args:
            ground_truth: Ground truth image values
            simulation: Simulated image values
            mask: Optional boolean mask for valid pixels

        Returns:
            float: Difference between the minimums
        """
        gt_min = cls.calculate(ground_truth, mask)
        sim_min = cls.calculate(simulation, mask)

        if np.isnan(gt_min) or np.isnan(sim_min):
            return cls._invalid(0.0)
        return gt_min - sim_min

    @classmethod
    def _invalid(cls, threshold: float) -> dict:
        return float('nan')
