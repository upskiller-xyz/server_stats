import numpy as np
from typing import Optional
from .base import BaseMetric


class ThresholdAccuracy(BaseMetric):
    """Threshold accuracy metric using numpy arrays."""
    
    
    @classmethod
    def calculate(cls, values: np.ndarray, mask: Optional[np.ndarray] = None, threshold: float = 1.25) -> float:
        """
        Calculate threshold accuracy for a single image.
        
        Args:
            values: Input image values
            mask: Optional boolean mask for valid pixels
            threshold: Threshold value for accuracy calculation
            
        Returns:
            float: Accuracy percentage or NaN if no valid pixels
        """
        if mask is not None:
            valid_pixels = mask.astype(bool)
            if not np.any(valid_pixels):
                return cls._invalid(threshold)
            masked_values = values[valid_pixels]
            return float(np.mean(masked_values > threshold) * 100)
        else:
            return float(np.mean(values > threshold) * 100)
    
    @classmethod
    def compare(cls, ground_truth: np.ndarray, simulation: np.ndarray,
                mask: Optional[np.ndarray] = None, threshold: float = 1.25) -> float:
        """
        Compare two images by calculating threshold accuracy.
        
        Args:
            ground_truth: Ground truth image values
            simulation: Simulated image values
            threshold: Threshold value for accuracy calculation
            
        Returns:
            float: Threshold accuracy percentage
        """
        if simulation.shape != ground_truth.shape:
            raise ValueError("Simulation and ground truth arrays must have the same shape")
        
        valid_pixels = (ground_truth > 0) & (simulation > 0)
        if mask is not None:
            valid_pixels = mask.astype(bool)
        
        if not np.any(valid_pixels):
            return cls._invalid(threshold)
        
        # Calculate the ratio
        sim_valid = simulation[valid_pixels]
        gt_valid = ground_truth[valid_pixels]
        
        ratio = np.maximum(sim_valid / gt_valid, gt_valid / sim_valid)
        # Count pixels where ratio is less than threshold
        correct_pixels = np.sum(ratio < threshold)
        total_pixels = np.sum(valid_pixels)
        
        accuracy = (correct_pixels / total_pixels) * 100
        return float(accuracy)
    
    
    @classmethod
    def _invalid(cls, threshold: float) -> dict:
        return float('nan')