import math
import collections
import statistics
import csv

class AccelerometerProcessor:
    def __init__(self, 
                 unit_scale=9.81, # Convert g to m/s^2 (or similar scaling)
                 noise_window=5, 
                 deadband_threshold=0.1, 
                 outlier_threshold=3.0,
                 normalization_range=10.0): # Max expected value for normalization
        
        self.unit_scale = unit_scale
        self.deadband_threshold = deadband_threshold
        self.outlier_threshold = outlier_threshold
        self.normalization_range = normalization_range
        
        # History for noise removal (per axis)
        self.history_x = collections.deque(maxlen=noise_window)
        self.history_y = collections.deque(maxlen=noise_window)
        self.history_z = collections.deque(maxlen=noise_window)
        
        # History for outlier detection (magnitude based)
        self.mag_history = collections.deque(maxlen=20)

    def convert_units(self, raw_reading):
        """Convert raw readings to physical units (e.g., mm/s^2)."""
        return [val * self.unit_scale for val in raw_reading]

    def remove_noise(self, reading):
        """Apply moving average smoothing."""
        self.history_x.append(reading[0])
        self.history_y.append(reading[1])
        self.history_z.append(reading[2])
        avg_x = sum(self.history_x) / len(self.history_x)
        avg_y = sum(self.history_y) / len(self.history_y)
        avg_z = sum(self.history_z) / len(self.history_z)
        return [avg_x, avg_y, avg_z]

    def apply_threshold(self, reading):
        """Zero out values below a certain noise floor (deadband)."""
        return [0.0 if abs(val) < self.deadband_threshold else val for val in reading]

    def detect_outliers(self, reading):
        """Check if the reading is an outlier based on magnitude Z-score."""
        magnitude = math.sqrt(sum(x**2 for x in reading))
        
        if len(self.mag_history) < 5:
            self.mag_history.append(magnitude)
            return False, reading

        mean_mag = statistics.mean(self.mag_history)
        stdev_mag = statistics.stdev(self.mag_history)
        
        self.mag_history.append(magnitude)
        
        if stdev_mag == 0:
            return False, reading

        z_score = (magnitude - mean_mag) / stdev_mag
        is_outlier = abs(z_score) > self.outlier_threshold
        
        return is_outlier, reading

    def normalize(self, reading):
        """Normalize readings to range [-1, 1] based on expected max range."""
        return [max(-1.0, min(1.0, val / self.normalization_range)) for val in reading]

    def process(self, raw_reading):
        # 1. Unit Conversion
        converted = self.convert_units(raw_reading)
        # 2. Noise Removal
        smoothed = self.remove_noise(converted)
        # 3. Thresholding
        thresholded = self.apply_threshold(smoothed)
        # 4. Outlier Detection
        is_outlier, _ = self.detect_outliers(thresholded)
        # 5. Normalization
        normalized = self.normalize(thresholded)
        return {
            "raw": raw_reading,
            "converted": converted,
            "smoothed": smoothed,
            "thresholded": thresholded,
            "is_outlier": is_outlier,
            "normalized": normalized
        }

def main():
    input_file = "input_sensor_accelerometer.txt"
    output_file = "output_sensor_accelerometer.txt"
    processor = AccelerometerProcessor(
        unit_scale=9810.0, 
        noise_window=5,
        deadband_threshold=100.0, 
        outlier_threshold=3.0,
        normalization_range=20000.0)

    print(f"Reading from {input_file}...")
    print(f"{'Step':<5} | {'Raw (g)':<25} | {'Smoothed (mm/s²)':<25} | {'Outlier':<8} | {'Norm X':<8}")
    print("-" * 85)

    try:
        with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
            reader = csv.DictReader(infile)
            fieldnames = ['time_step', 
                          'raw_x', 'raw_y', 'raw_z', 
                          'smooth_x', 'smooth_y', 'smooth_z', 
                          'is_outlier', 
                          'norm_x', 'norm_y', 'norm_z']
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in reader:
                t = row['time_step']
                try:
                    raw_reading = [float(row['ax_g']), float(row['ay_g']), float(row['az_g'])]
                except ValueError:
                    continue # Skip bad lines
                result = processor.process(raw_reading)
                # Console Output
                raw_str = f"[{raw_reading[0]:.2f}, {raw_reading[1]:.2f}, {raw_reading[2]:.2f}]"
                smooth_str = f"[{result['smoothed'][0]:.0f}, {result['smoothed'][1]:.0f}, {result['smoothed'][2]:.0f}]"
                outlier_str = "YES" if result['is_outlier'] else "NO"
                norm_x_str = f"{result['normalized'][0]:.2f}" 
                print(f"{t:<5} | {raw_str:<25} | {smooth_str:<25} | {outlier_str:<8} | {norm_x_str:<8}")
                # File Output
                writer.writerow({
                    'time_step': t,
                    'raw_x': raw_reading[0], 'raw_y': raw_reading[1], 'raw_z': raw_reading[2],
                    'smooth_x': result['smoothed'][0], 'smooth_y': result['smoothed'][1], 'smooth_z': result['smoothed'][2],
                    'is_outlier': result['is_outlier'],
                    'norm_x': result['normalized'][0], 'norm_y': result['normalized'][1], 'norm_z': result['normalized'][2]
                })
        print(f"\nProcessing complete. Results saved to {output_file}")
    except FileNotFoundError:
        print(f"Error: Could not find {input_file}. Please generate data first.")

if __name__ == "__main__":
    main()