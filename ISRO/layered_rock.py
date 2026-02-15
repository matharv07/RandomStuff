import cv2
import numpy as np

def process_image(image):
    if image is None: return 0.0

    debug_img = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    blurred = cv2.GaussianBlur(gray, (3, 3), 0) 
    
    v = np.median(blurred)
    lower = int(max(0, (1.0 - 0.33) * v))
    upper = int(min(255, (1.0 + 0.33) * v))
    edges = cv2.Canny(blurred, lower, upper)
    
    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        return 0.0

    valid_fragments = []
    angles = []
    
    for cnt in contours:
        if cv2.arcLength(cnt, False) < 15: 
            continue
            
        [vx, vy, x, y] = cv2.fitLine(cnt, cv2.DIST_L2, 0, 0.01, 0.01)
        
        angle = np.degrees(np.arctan2(vy, vx))[0]
        if angle < 0: angle += 180
        
        angles.append(angle)
        valid_fragments.append((angle, cnt))

    if not angles:
        return 0.0

    hist, bin_edges = np.histogram(angles, bins=36, range=(0, 180))
    hist[0] += hist[-1] 
    
    hist_smooth = np.convolve(hist, [1, 2, 3, 2, 1], mode='same')
    
    peak_bin_idx = np.argmax(hist_smooth)
    peak_angle = bin_edges[peak_bin_idx]
    
    tolerance = 20
    
    aligned_pixels = 0
    total_pixels = 0
    
    for angle, cnt in valid_fragments:
        length = cv2.arcLength(cnt, False)
        total_pixels += length
        
        diff = abs(angle - peak_angle)
        if diff > 90: diff = 180 - diff
        
        if diff < tolerance:
            cv2.drawContours(debug_img, [cnt], -1, (0, 255, 0), 2)
            aligned_pixels += length
        else:
            cv2.drawContours(debug_img, [cnt], -1, (0, 0, 255), 1)

    if total_pixels == 0: return 0.0
    
    p_align = aligned_pixels / total_pixels
    
    p_evidence = min(1.0, aligned_pixels / 1000.0)
    
    p_final = round(p_align * p_evidence, 4)
    if total_pixels == 0: return 0.0
    
    p_align = aligned_pixels / total_pixels
    
    # Boost the score if we have A LOT of aligned pixels (strong )
    # e.g., if we found 5000 pixels of aligned edges, we are very cevidenceonfident
    p_evidence = min(1.0, aligned_pixels / 1000.0)
    
    p_final = round(p_align * p_evidence, 4)

    cv2.rectangle(debug_img, (0, 0), (450, 40), (0, 0, 0), -1)
    text = f"Layered | Prob: {p_final} | P_Align: {round(p_align, 2)}"
    color = (0, 255, 0) if p_final > 0.5 else (0, 0, 255)
    cv2.putText(debug_img, text, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    
    cv2.imshow("Layer Flow Analysis", debug_img)
    cv2.waitKey(0)
    
    return p_final