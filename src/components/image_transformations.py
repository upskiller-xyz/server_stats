import numpy as np
import cv2


class ImageResizer:
    """Class for resizing images to the least of their dimensions."""
    
    @classmethod
    def resize_to_minimum(cls, image1: np.ndarray, image2: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """
        Resize both images to the minimum dimensions between them using OpenCV nearest neighbor scaling.
        
        Args:
            image1: First image as numpy array
            image2: Second image as numpy array
            
        Returns:
            tuple: (resized_image1, resized_image2) with minimum dimensions
        """
        if len(image1.shape) != len(image2.shape):
            raise ValueError("Images must have the same number of dimensions")
        
        # Get minimum dimensions
        min_height = min(image1.shape[0], image2.shape[0])
        min_width = min(image1.shape[1], image2.shape[1])
        
        # Resize images using OpenCV nearest neighbor interpolation
        resized_image1 = cv2.resize(image1, (min_width, min_height), interpolation=cv2.INTER_NEAREST)
        resized_image2 = cv2.resize(image2, (min_width, min_height), interpolation=cv2.INTER_NEAREST)
            
        return resized_image1, resized_image2


class ValueScaler:
    """Class for scaling image values based on their range."""
    
    @classmethod
    def scale_values(cls, image: np.ndarray) -> np.ndarray:
        """
        Scale image values based on their range.
        - If range is 0-more than 200: scale linearly where 0..255 translates to 0..10
        - If range is 0..10: do nothing
        
        Args:
            image: Input image as numpy array
            
        Returns:
            np.ndarray: Scaled image
        """
        if image.size == 0:
            return image
            
        min_val = np.min(image)
        max_val = np.max(image)
        
        # Check if range is 0..1 (scale to 0..10)
        if min_val >= 0 and max_val <= 1:
            # Linear scaling: 0..1 -> 0..10
            scaled = image.astype(np.float32) * 10.0
            print("Scaling applied: 0..1 -> 0..10")
            return scaled
        
        # Check if range is 0..10 (do nothing)
        if min_val >= 0 and max_val <= 10:
            print("No scaling")
            return image.astype(np.float32)
        
        # Check if range is 0-more than 200 (scale linearly 0..255 -> 0..10)
        if min_val >= 0 and max_val > 20:
            # Linear scaling: 0..255 -> 0..10
            scaled = (image.astype(np.float32) / 255.0) * 10.0
            print("Scaling applied: 0..255 -> 0..10")
            return scaled
        
        # For other ranges, return as float32 without scaling
        return image.astype(np.float32)


class ImageMasker:
    """Class for creating masks from ground truth images to exclude background pixels."""
    
    @classmethod
    def create_mask(cls, ground_truth: np.ndarray) -> np.ndarray:
        """
        Create a boolean mask from ground truth image.
        - Pixels with value 0 (grayscale) or [0,0,0] (RGB) are considered background (False)
        - If alpha channel exists, 0 transparency is considered background (False)
        - Valid pixels are marked as True
        
        Args:
            ground_truth: Ground truth image as numpy array
            
        Returns:
            np.ndarray: Boolean mask where True indicates valid pixels to compare
        """
        if ground_truth.size == 0:
            return np.array([], dtype=bool)
            
        # Handle different image formats
        if len(ground_truth.shape) == 2:
            # Grayscale image
            mask = ground_truth != 0
            
        elif len(ground_truth.shape) == 3:
            if ground_truth.shape[2] == 3:
                # RGB image - mask out [0,0,0] pixels
                mask = ~np.all(ground_truth == 0, axis=2)
                
            elif ground_truth.shape[2] == 4:
                # RGBA image - use alpha channel for masking
                alpha_channel = ground_truth[:, :, 3]
                # Also consider RGB values for additional masking
                # rgb_mask = ~np.all(ground_truth[:, :, :3] == 0, axis=2)
                mask = alpha_channel != 0
                # mask = rgb_mask & alpha_mask
                
            else:
                # Fallback for other multi-channel images
                mask = ~np.all(ground_truth == 0, axis=2)
                
        else:
            # Fallback for unexpected dimensions
            mask = ground_truth != 0
        cv2.imwrite("mask.png", mask.astype(np.uint8)*255)
        return mask.astype(bool)
    
    @classmethod
    def apply_mask(cls, image: np.ndarray, mask: np.ndarray) -> np.ndarray:
        """
        Apply mask to image by setting masked pixels to 0.
        
        Args:
            image: Input image
            mask: Boolean mask where True indicates valid pixels
            
        Returns:
            np.ndarray: Masked image
        """
        if image.shape[:2] != mask.shape:
            raise ValueError("Image and mask must have compatible shapes")
            
        masked_image = image.copy()
        if len(image.shape) == 2:
            # Grayscale
            masked_image[~mask] = 0
        else:
            # Multi-channel
            masked_image[~mask] = 0
            
        return masked_image