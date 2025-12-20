import numpy as np
from typing import Optional

from ..constants import MetricNames, RequestKeys
from .base import BaseMetric


class ComplianceMetric(BaseMetric):
    """Analyze compliance by calculating percentage of pixels with values >threshold in unmasked areas."""
    
    
    
    @classmethod
    def calculate(cls, values: np.ndarray, mask: Optional[np.ndarray] = None, threshold: float = 0.1) -> float:
        """
        Calculate compliance percentage for single image input.
        
        Args:
            values: Input image values
            mask: Optional boolean mask for valid pixels
            threshold: Value threshold for compliance (default: 0.1)
            
        Returns:
            float: Compliance percentage
        """
        result = cls.calculate_compliance(values, mask, threshold)
        return result[MetricNames.COMPLIANCE_PERCENTAGE.value]
    
    @classmethod
    def compare(cls, ground_truth: np.ndarray, simulation: np.ndarray, mask: Optional[np.ndarray] = None, threshold: float = 0.1) -> float:
        """
        Compare two images by calculating compliance difference.
        
        Args:
            ground_truth: Ground truth image values
            simulation: Simulated image values
            mask: Optional boolean mask for valid pixels
            threshold: Value threshold for compliance (default: 0.1)
            
        Returns:
            float: Difference in compliance percentages (simulation - ground_truth)
        """
        gt_compliance = cls.calculate(ground_truth, mask, threshold)
        sim_compliance = cls.calculate(simulation, mask, threshold)
        
        if np.isnan(gt_compliance) or np.isnan(sim_compliance):
            return cls._invalid(threshold)
        return gt_compliance - sim_compliance 
    
    @classmethod
    def calculate_compliance(cls, image: np.ndarray, mask: np.ndarray = None, threshold: float = 1.0) -> dict:
        """
        Calculate compliance percentage for pixels with values > threshold in unmasked areas.
        
        Args:
            image: Input image as numpy array
            mask: Optional boolean mask where True indicates valid pixels (unmasked areas)
            threshold: Value threshold for compliance (default: 1.0)
            
        Returns:
            dict: Compliance analysis results
        """
        if mask is None:
            mask = image >= 0
        
        mask = mask.astype(bool)
        
        valid_pixels = image[mask]
        
        if len(valid_pixels) == 0:
            return cls._invalid_full(threshold)
        
        compliant_pixels = np.sum(valid_pixels > threshold)
        total_valid_pixels = len(valid_pixels)
        
        compliance_percentage = (compliant_pixels / total_valid_pixels) * 100.0
        
        return {
            MetricNames.COMPLIANCE_PERCENTAGE.value: float(compliance_percentage),
            MetricNames.COMPLIANT_PIXELS.value: int(compliant_pixels),
            MetricNames.TOTAL_VALID_PIXELS.value: int(total_valid_pixels),
            RequestKeys.THRESHOLD.value: float(threshold)
        }
    
    @classmethod
    def _invalid_full(cls, threshold: float) -> dict:
        return {
                MetricNames.COMPLIANCE_PERCENTAGE.value: cls._invalid(threshold),
                MetricNames.COMPLIANT_PIXELS.value: 0,
                MetricNames.TOTAL_VALID_PIXELS.value: 0,
                RequestKeys.THRESHOLD.value: threshold
            }
    def _invalid(cls, threshold: float) -> dict:
        return  float('nan')
            