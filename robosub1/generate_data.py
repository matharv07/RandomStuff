"""AI GENERATED CODE"""
import csv
import random
import math

def generate_synthetic_data(filename="input_sensor_accelerometer.txt", num_samples=200):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['time_step', 'ax_g', 'ay_g', 'az_g']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader() 
        for t in range(num_samples):
            # Gravity on Z-axis (approx 1g)
            base_z = 1.0 
            
            # Sine wave motion on X-axis
            motion_x = 0.5 * math.sin(t * 0.2)
            
            # Random noise
            noise_x = random.gauss(0, 0.05)
            noise_y = random.gauss(0, 0.05)
            noise_z = random.gauss(0, 0.05)
            
            # Occasional outlier spike
            if random.random() < 0.05:
                noise_x += 3.0 # Spike
            
            ax = motion_x + noise_x
            ay = noise_y
            az = base_z + noise_z
            
            writer.writerow({'time_step': t, 'ax_g': f"{ax:.4f}", 'ay_g': f"{ay:.4f}", 'az_g': f"{az:.4f}"})

    print(f"Generated {num_samples} samples in {filename}")

if __name__ == "__main__":
    generate_synthetic_data()
