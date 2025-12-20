import numpy as np
import cv2
from typing import Optional, List


class QuantizedIoU:
    """Quantized IoU metric with only classmethod interface."""

    @classmethod
    def compare(cls, ground_truth: np.ndarray, 
                simulation: np.ndarray,
                mask: Optional[np.ndarray] = None,
                bins: Optional[List[float]] = None,
                ) -> float:
        """
        Compare two images using quantized IoU with given value range bins.

        Args:
            ground_truth: Ground truth image values
            simulation: Simulated image values
            mask: Optional boolean mask to apply to both images
            bins: List of bin boundaries defining value ranges
            epsilon: Small value to avoid division by zero

        Returns:
            float: Quantized IoU value
        """

        if ground_truth.shape != simulation.shape:
            raise ValueError("Ground truth and simulation must have the same shape")

        if bins is None:
            bins = list(range(0,11))

        if len(bins) < 2:
            raise ValueError("bins must contain at least 2 values")

        if bins != sorted(bins):
            raise ValueError("bin values must be in ascending order")
        
        if mask is None:
            mask = np.ones_like(ground_truth, dtype=bool)
        mask = mask.astype(bool)
        

        # Calculate IoU for each bin range using correct formula
        num_intervals = len(bins) - 1
        
        mask = mask.reshape(ground_truth.shape)

        gt_masks = [x for x in [cls._in_range(ground_truth, bins[i], bins[i+1], mask) for i in range(num_intervals)]]
        sim_masks = [x for x in [cls._in_range(simulation, bins[i], bins[i+1], mask) for i in range(num_intervals)]]
        iou_scores = [cls._iou(gt_masks[i], sim_masks[i]) for i in range(num_intervals)]

        return float(np.mean(iou_scores))
    
    @classmethod
    def _iou(cls, gt_mask, sim_mask) -> float:
        """
        Helper method to calculate IoU between two boolean masks.

        Args:
            gt_mask: Ground truth boolean mask
            sim_mask: Simulated boolean mask

        Returns:
            float: IoU value
        """
        intersection = np.logical_and(gt_mask, sim_mask)
        union = np.logical_or(gt_mask, sim_mask)
        
        intersection_sum = np.sum(intersection)
        union_sum = np.sum(union)
        
        if union_sum == 0:
            return 1.0  # Both empty, consider perfect match
        
        return intersection_sum / union_sum
    
    @classmethod
    def _invalid(cls, threshold: float) -> dict:
        return float(0)
    
    @classmethod
    def _in_range(cls, values: np.ndarray, min_value: float, max_value: float, mask:Optional[np.ndarray]) -> np.ndarray:
        """
        Helper method to create a boolean mask for values within a specified range.

        Args:
            values: Input image values
            min_value: Minimum value of the range (inclusive)
            max_value: Maximum value of the range (inclusive)
        Returns:
            np.ndarray: Boolean mask where True indicates values within the range
        """
        if mask is None:
            mask = np.ones_like(values, dtype=bool)
        mask = mask.astype(bool).reshape(values.shape)
        return (values >= min_value) & (values <= max_value) & mask

    @classmethod
    def calculate(cls, values: np.ndarray, mask: Optional[np.ndarray] = None,
                  **kwargs) -> float:
        """
        Calculate metric for single image - returns 1.0 as it doesn't make sense for one image.

        Args:
            values: Input image values
            mask: Optional boolean mask
            **kwargs: Additional parameters (ignored)

        Returns:
            float: Always returns 1.0
        """
        return 1.0

