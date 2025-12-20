import numpy as np
from typing import Optional
from .base import BaseMetric


class RangePolygonMetric(BaseMetric):
    """Find areas where values are within a specified range in the masked image."""
    
        
    def calculate(cls, values: np.ndarray, mask: Optional[np.ndarray] = None, min_value: Optional[float]=0, max_value: Optional[float]=1) -> np.ndarray:
        """
        Create a binary mask where 1 indicates values within the range.
        
        Args:
            values: Matrix of float values (numpy array)
            mask: Optional boolean mask of same shape as values.
                 True indicates valid values, False indicates values to ignore.
                 If None, all values are considered valid.
        
        Returns:
            np.ndarray: Binary mask where 1 indicates values within the range,
                       0 indicates values outside the range or masked out values.
        """
        # Create range mask
        range_mask = (values >= min_value) & (values <= max_value)
        
        if mask is not None:
            # Combine with provided mask
            mask = mask.astype(bool)
            range_mask = range_mask & mask
            
        return range_mask.astype(np.uint8)
        
    @classmethod
    def compare(cls, mask1: np.ndarray, mask2: np.ndarray) -> float:
        """
        Compare two binary masks using Intersection over Union (IoU).
        
        Args:
            mask1: First binary mask
            mask2: Second binary mask (must be same shape as mask1)
            
        Returns:
            float: IoU score between the masks.
                  Returns 0.0 if there's no overlap or if either mask is empty.
        """
        if mask1.shape != mask2.shape:
            raise ValueError("Masks must have the same shape")
            
        intersection = np.logical_and(mask1, mask2).sum()
        union = np.logical_or(mask1, mask2).sum()
        
        return float(intersection / union) if union > 0 else cls._invalid(0)
    
    @classmethod
    def _invalid(cls, threshold: float) -> dict:
        return float(0)