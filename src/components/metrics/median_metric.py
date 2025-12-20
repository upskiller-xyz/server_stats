import numpy as np
from typing import Optional
from .base import BaseMetric


class MedianMetric(BaseMetric):
    """Calculate median of masked values."""
    
    @classmethod
    def calculate(cls, values: np.ndarray, mask: Optional[np.ndarray] = None) -> float:
        """
        Calculate median for single image input.
        
        Args:
            values: Input image values
            mask: Optional boolean mask for valid pixels
            
        Returns:
            float: Median of valid pixels
        """
        if mask is None:
            # If no mask provided, use all values
            return float(np.median(values))
            
        # Ensure mask is boolean
        mask = mask.astype(bool)
        
        # Calculate median of masked values
        masked_values = values[mask]
        if len(masked_values) == 0:
            return cls._invalid(0.0)
            
        return float(np.median(masked_values))
        
    @classmethod
    def compare(cls, ground_truth: np.ndarray, simulation: np.ndarray, mask: Optional[np.ndarray] = None) -> float:
        """
        Compare two images by calculating median difference.
        
        Args:
            ground_truth: Ground truth image values
            simulation: Simulated image values
            mask: Optional boolean mask for valid pixels
            
        Returns:
            float: Absolute difference between the medians
        """
        gt_median = cls.calculate(ground_truth, mask)
        sim_median = cls.calculate(simulation, mask)
        
        if np.isnan(gt_median) or np.isnan(sim_median):
            return cls._invalid(0.0)
        return gt_median - sim_median 
    
    @classmethod
    def _invalid(cls, threshold: float) -> dict:
        return float('nan')