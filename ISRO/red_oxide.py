import cv2
import numpy as np

def process_image(image):
    if image is None:
        return 0.0

    output_img = image.copy()
    
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    avg_brightness = np.mean(gray)
    
    _, dark_mask = cv2.threshold(gray, avg_brightness * 0.85, 255, cv2.THRESH_BINARY_INV)
    
    lower_red1 = np.array([0, 60, 20])
    upper_red1 = np.array([10, 255, 180])
    
    lower_red2 = np.array([170, 60, 20])
    upper_red2 = np.array([180, 255, 180])
    
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    color_mask = cv2.bitwise_or(mask1, mask2)
    
    combined_mask = cv2.bitwise_and(color_mask, color_mask, mask=dark_mask)
    
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    
    clean_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_CLOSE, kernel)
    clean_mask = cv2.morphologyEx(clean_mask, cv2.MORPH_OPEN, kernel)

    contours, _ = cv2.findContours(clean_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    valid_regions = []
    total_oxide_area = 0
    
    for cnt in contours:
        area = cv2.contourArea(cnt)
        
        if area > 100:  
            valid_regions.append(cnt)
            total_oxide_area += area

    if valid_regions:
        overlay = output_img.copy()
        cv2.drawContours(overlay, valid_regions, -1, (0, 0, 255), -1) 
        alpha = 0.4
        cv2.addWeighted(overlay, alpha, output_img, 1 - alpha, 0, output_img)
        cv2.drawContours(output_img, valid_regions, -1, (0, 0, 255), 2)

    img_area = image.shape[0] * image.shape[1]
    
    if img_area > 0:
        coverage = total_oxide_area / img_area
        prob = min(1.0, coverage / 0.02)
    else:
        prob = 0.0
        
    p_final = round(prob, 4)

    cv2.rectangle(output_img, (0, 0), (350, 40), (0, 0, 0), -1)
    text = f"Oxide Prob: {p_final} | Regions: {len(valid_regions)}"
    color = (0, 255, 0) if p_final > 0.5 else (0, 0, 255)
    cv2.putText(output_img, text, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    cv2.imshow("Red Oxide Regions", output_img)
    cv2.waitKey(0)

    return p_final