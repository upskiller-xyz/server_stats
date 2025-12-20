from typing import Dict, Set
import numpy as np
from src.components.metric_types import MetricType


class MetricCalculator:
    """
    Calculates all metrics for given result and mask.
    Uses Strategy pattern with metric type mapping.
    """

    # Metrics to include in endpoint responses
    ENDPOINT_METRICS: Set[str] = {'mean', 'median', 'min', 'max', 'valid_area'}

    def __init__(self):
        """Initialize calculator with metric type mapping."""
        self._metric_map = self._build_metric_map()

    def _build_metric_map(self) -> Dict[str, type]:
        """
        Build mapping of metric names to metric classes.

        Returns:
            Dictionary mapping metric names to metric classes
        """
        return {
            metric_type.name.lower(): metric_type.value
            for metric_type in MetricType.get_members()
        }

    def calculate_all(self, values: np.ndarray, mask: np.ndarray, filter_for_endpoint: bool = True) -> Dict[str, float]:
        """
        Calculate all available metrics on the masked values.

        Args:
            values: Result of float values (0-10)
            mask: Binary mask (same dimensions as values)
            filter_for_endpoint: If True, only return metrics in ENDPOINT_METRICS

        Returns:
            Dictionary of metric names to calculated values
        """
        results = {}
        boolean_mask = mask.astype(bool)

        for metric_name, metric_class in self._metric_map.items():
            # Skip metrics not in endpoint set if filtering is enabled
            if filter_for_endpoint and metric_name not in self.ENDPOINT_METRICS:
                continue

            try:
                result = metric_class.calculate(values, boolean_mask)
                results[metric_name] = self._format_result(result)
            except Exception as e:
                # Skip metrics that fail to calculate
                results[metric_name] = None

        return results

    def _format_result(self, result) -> float:
        """
        Format metric result to float or handle special cases.

        Args:
            result: Raw metric result

        Returns:
            Formatted float value or None for invalid results
        """
        if isinstance(result, (int, float)):
            if np.isnan(result) or np.isinf(result):
                return None
            return float(result)
        elif isinstance(result, np.ndarray):
            # For metrics that return arrays, convert to list
            return result.tolist()
        elif isinstance(result, dict):
            # For metrics that return dictionaries
            return result
        return result
