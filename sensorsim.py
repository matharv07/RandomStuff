import random
import math
import collections
import statistics

class SensorSimulator:
    def __init__(self, base_value=20.0, noise_level=2.0, outlier_prob=0.05):
        self.base_value = base_value
        self.noise_level = noise_level
        self.outlier_prob = outlier_prob
        self.time_step = 0

    def generate_reading(self):
        self.time_step += 1
        # Base signal: Sine wave
        signal = self.base_value + 5 * math.sin(self.time_step * 0.1)
        
        # Add random noise
        noise = random.gauss(0, self.noise_level)
        
        # Inject outlier
        if random.random() < self.outlier_prob:
            # Outlier is a large spike
            outlier_sign = 1 if random.random() > 0.5 else -1
            noise += outlier_sign * (self.noise_level * 5)
            
        return signal + noise

class NoiseFilter:
    def __init__(self, window_size=5):
        self.window = collections.deque(maxlen=window_size)

    def update(self, value):
        self.window.append(value)
        return sum(self.window) / len(self.window)

class OutlierDetector:
    def __init__(self, window_size=20, threshold=2.5):
        self.history = collections.deque(maxlen=window_size)
        self.threshold = threshold

    def check(self, value):
        if len(self.history) < 2:
            self.history.append(value)
            return False # Not enough data

        mean = statistics.mean(self.history)
        stdev = statistics.stdev(self.history)
        
        self.history.append(value)

        if stdev == 0:
            return False

        z_score = (value - mean) / stdev
        return abs(z_score) > self.threshold

def main():
    sensor = SensorSimulator(base_value=25.0, noise_level=1.0, outlier_prob=0.1)
    noise_filter = NoiseFilter(window_size=5)
    outlier_detector = OutlierDetector(window_size=15, threshold=3.0)

    print(f"{'Time':<5} | {'Raw':<10} | {'Filtered':<10} | {'Status':<10}")
    print("-" * 45)

    for t in range(1, 51):
        raw_val = sensor.generate_reading()
        filtered_val = noise_filter.update(raw_val)
        is_outlier = outlier_detector.check(raw_val)
        
        status = "OUTLIER" if is_outlier else "OK"
        print(f"{t:<5} | {raw_val:<10.2f} | {filtered_val:<10.2f} | {status:<10}")

if __name__ == "__main__":
    main()
