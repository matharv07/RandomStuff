import cv2
import numpy as np

def process_image(image):
    if image is None: return 0.0

    debug_img = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 1. Blur & Canny (Standard)
    # Less blur to keep thin layers distinct
    blurred = cv2.GaussianBlur(gray, (3, 3), 0) 
    
    # Auto-tune thresholds
    v = np.median(blurred)
    lower = int(max(0, (1.0 - 0.33) * v))
    upper = int(min(255, (1.0 + 0.33) * v))
    edges = cv2.Canny(blurred, lower, upper)
    
    # 2. FIND CONTOURS ON RAW EDGES (No Morphological Closing)
    # RETR_LIST: We don't care about hierarchy, just get every scrap of edge
    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        return 0.0

    valid_fragments = [] # Store (angle, contour)
    angles = []
    
    for cnt in contours:
        # Filter: Ignore tiny grit, keep "segments"
        if cv2.arcLength(cnt, False) < 15: 
            continue
            
        # 3. Orient the Fragment
        # fitLine calculates the general direction of this specific squiggly line
        [vx, vy, x, y] = cv2.fitLine(cnt, cv2.DIST_L2, 0, 0.01, 0.01)
        
        # Convert vector to angle (0-180)
        angle = np.degrees(np.arctan2(vy, vx))[0]
        if angle < 0: angle += 180
        
        angles.append(angle)
        valid_fragments.append((angle, cnt))

    if not angles:
        return 0.0

    # 4. Histogram & Peak Detection (The "Parallel Check")
    # We increase bins to 36 (5-degree precision) for tighter control
    hist, bin_edges = np.histogram(angles, bins=36, range=(0, 180))
    hist[0] += hist[-1] # Wrap-around
    
    # Smooth the histogram to find the "general" direction (avoids noise peaks)
    # [1, 4, 6, 4, 1] is a Gaussian-like smoothing kernel
    hist_smooth = np.convolve(hist, [1, 2, 3, 2, 1], mode='same')
    
    peak_bin_idx = np.argmax(hist_smooth)
    peak_angle = bin_edges[peak_bin_idx]
    
    # Define a tolerance window (e.g., +/- 10 degrees from peak)
    tolerance = 10 
    
    # 5. Visualization & Scoring
    aligned_pixels = 0
    total_pixels = 0
    
    for angle, cnt in valid_fragments:
        length = cv2.arcLength(cnt, False)
        total_pixels += length
        
        # Check diff, handling the 0/180 wrap
        diff = abs(angle - peak_angle)
        if diff > 90: diff = 180 - diff
        
        if diff < tolerance:
            # GREEN: This fragment is part of the layer system
            cv2.drawContours(debug_img, [cnt], -1, (0, 255, 0), 2)
            aligned_pixels += length
        else:
            # RED: This is a random crack or noise
            # Draw thinner (1px) to de-emphasize
            cv2.drawContours(debug_img, [cnt], -1, (0, 0, 255), 1)

    # 6. Final Probability
    # Ratio of "Aligned Edge Length" to "Total Edge Length"
    if total_pixels == 0: return 0.0
    
    p_align = aligned_pixels / total_pixels
    
    # Boost the score if we have A LOT of aligned pixels (strong evidence)
    # e.g., if we found 5000 pixels of aligned edges, we are very confident
    p_evidence = min(1.0, aligned_pixels / 1000.0)
    
    p_final = round(p_align * p_evidence, 4)

    # Display
    cv2.rectangle(debug_img, (0, 0), (350, 40), (0, 0, 0), -1)
    text = f"Prob: {p_final} | P_Align: {round(p_align, 2)}"
    color = (0, 255, 0) if p_final > 0.5 else (0, 0, 255)
    cv2.putText(debug_img, text, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    
    cv2.imshow("Layer Flow Analysis", debug_img)
    cv2.waitKey(0)
    
    return p_final