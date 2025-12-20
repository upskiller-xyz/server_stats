from .extended_enum import ExtendedEnum
from typing import Type

from . import metrics as m


class MetricType(ExtendedEnum):
    """Enumeration of available metrics."""
    
    MEAN = m.MeanMetric
    MEDIAN = m.MedianMetric
    RANGE_POLYGON = m.RangePolygonMetric
    THRESHOLD_ACCURACY = m.ThresholdAccuracy
    COMPLIANCE_ANALYSIS = m.ComplianceMetric
    QUANTIZED_IOU = m.QuantizedIoU
    MAE = m.MAEMetric
    