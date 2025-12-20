from dataclasses import dataclass, field
from typing import Dict, Optional
import numpy as np

from .metric_types import MetricType


@dataclass
class EvalResult:
    """Container for evaluation results across multiple metrics."""
    
    result: dict[MetricType, float] = field(default_factory=dict)
    
    
    def compare(self, other: 'EvalResult') -> Dict[str, float]:
        """
        Compare this result with another result using appropriate comparison methods.
        
        Args:
            other: Another EvalResult instance to compare with
            
        Returns:
            dict: Mapping of metrics to their comparison scores
        """
        comparisons = {
            mm: mm.value.compare(self.result[mm], other.result[mm])
            for mm in MetricType.get_members()
        }
        return comparisons


class Evaluator:
    """Class for evaluating images using multiple metrics."""

    _metrics = MetricType.get_members()
    
    @classmethod
    def run(cls, 
            image: np.ndarray, 
            mask: Optional[np.ndarray] = None
            ) -> EvalResult:
        """
        Evaluate an image using all available metrics.
        
        Args:
            image: Input image as a numpy array
            mask: Optional mask array of same shape as image.
                 True indicates valid values, False indicates values to ignore.
            min_value: Minimum value for range polygon metric (default: 0.0)
            max_value: Maximum value for range polygon metric (default: 1.0)
            
        Returns:
            EvalResult: Container with all metric results
        """
        # Calculate metrics
        result = {}
        for mm in cls._metrics:
            if mm == MetricType.RANGE_POLYGON:
                # Range polygon metric needs additional parameters
                metric_instance = mm.value(min_value=0.0, max_value=1.0)
            else:
                metric_instance = mm.value()
            result[mm] = metric_instance.calculate(image, mask)
        
        return EvalResult(
            result
        )
