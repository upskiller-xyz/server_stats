import numpy as np
from typing import Optional
from .base import BaseMetric


class MAEMetric(BaseMetric):
    """Mean Absolute Error metric with configurable value ranges."""
    
    @classmethod
    def calculate(cls, values: np.ndarray, mask: Optional[np.ndarray] = None, min_value: float = 0.0, max_value: float = 1.0) -> float:
        """
        Calculate MAE for single image (always returns 0 since MAE requires comparison).
        
        Args:
            values: Input image values
            mask: Optional boolean mask for valid pixels
            min_value: Minimum value of the range (inclusive)
            max_value: Maximum value of the range (inclusive)
            
        Returns:
            float: Always 0.0 for single image
        """
        # For single image, MAE doesn't make sense - return 0
        return 0.0
    
    @classmethod
    def compare(cls, ground_truth: np.ndarray, simulation: np.ndarray, mask: Optional[np.ndarray] = None, min_value: float = 0.0, max_value: float = 1.0) -> float:
        """
        Compare two images by calculating Mean Absolute Error within specified range.
        
        Args:
            ground_truth: Ground truth image values
            simulation: Simulated image values
            mask: Optional boolean mask for valid pixels
            min_value: Minimum value of the range (inclusive)
            max_value: Maximum value of the range (inclusive)
            
        Returns:
            float: MAE for pixels within the specified value range
        """
        if simulation.shape != ground_truth.shape:
            raise ValueError("simulation and ground truth arrays must have the same shape")
        
        # Apply mask if provided
        if mask is not None:
            mask = mask.astype(bool)
            simulation_masked = simulation[mask]
            gt_masked = ground_truth[mask]
        else:
            simulation_masked = simulation.flatten()
            gt_masked = ground_truth.flatten()
        
        if len(simulation_masked) == 0:
            return cls._invalid(min_value)
        # Filter values within the specified range
        range_mask = (gt_masked >= min_value) & (gt_masked <= max_value)
        
        if not np.any(range_mask):
            return cls._invalid(min_value)
        
        # Calculate MAE for pixels within range
        sim_range = simulation_masked[range_mask]
        gt_range = gt_masked[range_mask]
        
        mae = np.mean(np.abs(sim_range - gt_range))
        return float(mae)
    
    @classmethod
    def _invalid(cls, threshold: float) -> dict:
        return float('nan')
    
    