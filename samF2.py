import numpy as np
import torch
import cv2
from scipy.ndimage import binary_dilation, binary_erosion, gaussian_filter
from sam2.build_sam import build_sam2
from sam2.sam2_image_predictor import SAM2ImagePredictor

print (f"Using device: {torch.device('cuda' if torch.cuda.is_available() else 'cpu')}")
def sam_validation(image, coordinates):
    # Load SAM2 model
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = build_sam2("sam2.1_hiera_l.yaml", "sam2.1_hiera_large.pt", device=device)
    predictor = SAM2ImagePredictor(model)
    
    if not isinstance(coordinates, np.ndarray):
        coordinates = np.array(coordinates)
    if coordinates.ndim == 1:
        coordinates = coordinates.reshape(1, -1)
    
    predictor.set_image(image)
    masks, scores, _ = predictor.predict(
        point_coords=coordinates,
        point_labels=np.ones(len(coordinates), dtype=np.int32),
        multimask_output=True
    )
    
    mask = masks[0]
    mask = binary_erosion(mask, iterations=1)
    mask = binary_dilation(mask, iterations=2)
    mask = gaussian_filter(mask.astype(float), sigma=3)
    
    # Create RGBA output
    result = np.zeros((image.shape[0], image.shape[1], 4), dtype=np.uint8)
    result[:, :, :3] = image
    result[:, :, 3] = (mask * 255).astype(np.uint8)
    
    return result 

print ("SAM validation function is ready to use.")