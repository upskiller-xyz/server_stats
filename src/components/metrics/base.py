from abc import ABC, abstractmethod
import numpy as np
from typing import Optional


class BaseMetric(ABC):
    """Base class for all metrics."""
    
    @abstractmethod
    def calculate(self, values: np.ndarray, mask: Optional[np.ndarray] = None):
        """
        Calculate the metric on the given values with an optional mask.
        
        Args:
            values: Result of float values (numpy array)
            mask: Optional boolean mask of same shape as values. 
                 True indicates valid values, False indicates values to ignore.
                 If None, all values are considered valid.
        
        Returns:
            The calculated metric value (type depends on the specific metric)
        """
        pass

    @classmethod
    @abstractmethod
    def compare(cls, value1, value2) -> float:
        """
        Compare two metric values and return a similarity/difference score.
        
        Args:
            value1: First metric value
            value2: Second metric value
            
        Returns:
            float: Comparison score. Interpretation depends on the specific metric.
        """
        pass