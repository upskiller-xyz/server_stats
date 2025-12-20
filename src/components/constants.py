from .extended_enum import ExtendedEnum


BUSINESS_DF = 1.0

class RequestKeys(ExtendedEnum):
    """Enumeration for request data keys."""
    GROUND_TRUTH = "ground_truth"
    SIMULATION = "simulation"
    IMAGE = "image"
    THRESHOLD = "threshold"
    MODE = "mode"
    BINS = "bins"
    MIN_VALUE = "min_value"
    MAX_VALUE = "max_value"


class RequestMode(ExtendedEnum):
    """Enumeration for request processing modes."""
    SINGLE = "single"
    COMPARISON = "comparison"


class MetricNames(ExtendedEnum):
    """Enumeration for metric result names."""
    # Statistical Metrics
    MEAN_DIFFERENCE = "mean_difference"
    MEDIAN_DIFFERENCE = "median_difference"
    MEAN = "mean"
    MEDIAN = "median"

    # MAE Metrics
    MAE_DEFAULT = "mae_default"
    MAE_BUSINESS = "mae_business"

    # IoU Metrics
    QUANTIZED_IOU = "quantized_iou"
    QUANTIZED_IOU_BUSINESS = "quantized_iou_business"
    QUANTIZED_IOU_ALL = "quantized_iou_all"
    QUANTIZED_IOU_SENSITIVE = "quantized_iou_sensitive"
    # QUANTIZED_IOU_LE = "quantized_iou_le"
    # QUANTIZED_IOU_GT = "quantized_iou_gt"

    # Accuracy Metrics
    THRESHOLD_ACCURACY = "threshold_accuracy"
    THRESHOLD_ACCURACY_1_25 = "threshold_accuracy_1.25"
    THRESHOLD_ACCURACY_1_5 = "threshold_accuracy_1.5"
    THRESHOLD_ACCURACY_2_0 = "threshold_accuracy_2.0"

    # Compliance Metrics
    COMPLIANCE = "compliance"
    COMPLIANCE_DIFFERENCE = "compliance_difference"
    COMPLIANCE_PERCENTAGE = "compliance_percentage"
    COMPLIANT_PIXELS = "compliant_pixels"
    TOTAL_VALID_PIXELS = "total_valid_pixels"

    @classmethod
    def get_display_name(cls, metric_name):
        """Get user-friendly display names for metrics."""
        display_names = {
            cls.MEAN_DIFFERENCE: "Mean difference",
            cls.MEDIAN_DIFFERENCE: "Median difference",
            cls.QUANTIZED_IOU: "Quantized IoU",
            cls.THRESHOLD_ACCURACY: "Threshold accuracy"
        }
        return display_names.get(metric_name, metric_name.value.replace('_', ' ').title())


class IoUMethods(ExtendedEnum):
    """Enumeration for Quantized IoU calculation methods."""
    ALL = "all"
    LE = "le"
    GT = "gt"
    BETWEEN = "between"


class ErrorMessages(ExtendedEnum):
    """Enumeration for error messages."""
    MISSING_DATA = "Missing data in request"
    MISSING_IMAGE = "Missing image in request"
    MISSING_GROUND_TRUTH_SIMULATION = "Missing ground_truth or simulation in request"
    MISSING_GT_OUTPUT = "Missing ground truth or output in request"
    MISSING_SIMULATION_GT = "Missing simulation or ground truth in request"
    INTERNAL_SERVER_ERROR = "Internal server error: {}"
    INVALID_METHOD = "Invalid method"
    INVALID_MODE = "Invalid mode"
    COMPARISON_REQUIRED = "{} calculation requires both ground_truth and simulation data for comparison"



# Default values
class Defaults(ExtendedEnum):
    """Default values for various parameters."""
    THRESHOLD_1_0 = 1.0
    THRESHOLD_1_25 = 1.25
    THRESHOLD_1_5 = 1.5
    THRESHOLD_2_0 = 2.0
    THRESHOLD_0_1 = 0.1
    THRESHOLD_0_5 = 0.5
    NUM_INTERVALS_10 = 10
    MIN_VALUE_0 = 0.0
    MAX_VALUE_10 = 10.0
    MIN_VALUE_0_9 = 0.9
    MAX_VALUE_1_1 = 1.1
    BINS_ALL = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    BINS_BUSINESS = [0.0, 0.5, 1.0, 2.0, 5.0, 10.0]
    BINS_SENSITIVE = [0.9, 1.1]