import numpy as np
from typing import Optional
from .base import BaseMetric


class MeanMetric(BaseMetric):
    """Calculate arithmetic mean of masked values."""
    
    @classmethod
    def calculate(cls, values: np.ndarray, mask: Optional[np.ndarray] = None) -> float:
        """
        Calculate mean for single image input.
        
        Args:
            values: Input image values
            mask: Optional boolean mask for valid pixels
            
        Returns:
            float: Mean of valid pixels
        """
        if mask is None:
            return float(np.mean(values))
        
        mask = mask.astype(bool)
        
        
        masked_values = values[mask]
        if len(masked_values) == 0:
            return cls._invalid(0.0)
        
        return float(np.mean(masked_values))
        
    @classmethod
    def compare(cls, ground_truth: np.ndarray, simulation: np.ndarray, mask: Optional[np.ndarray] = None) -> float:
        """
        Compare two images by calculating mean difference.
        
        Args:
            ground_truth: Ground truth image values
            simulation: Simulated image values
            mask: Optional boolean mask for valid pixels
            
        Returns:
            float: Absolute difference between the means
        """
        gt_mean = cls.calculate(ground_truth, mask)
        sim_mean = cls.calculate(simulation, mask)
        
        if np.isnan(gt_mean) or np.isnan(sim_mean):
            return cls._invalid(0.0)
        return gt_mean - sim_mean
    
    @classmethod
    def _invalid(cls, threshold: float) -> dict:
        return float('nan')