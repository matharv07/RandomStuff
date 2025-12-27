Just a quick project to simulate and process 3D accelerometer data.

## Files

- **generate_data.py**: Run this first! It creates `input_sensor_accelerometer.txt` with some synthetic raw values (sine wave motion + gravity + random noise).
- **simulate_accelerometer.py**: This is the main processor. It reads the raw input, applies a moving average filter, checks for outliers (Z-score), and normalizes everything. Saves the results to `output_sensor_accelerometer.txt`.
- **print_accelerometer.cpp**: A little C++ helper I wrote to read both the input and output files and print them side-by-side in the terminal. Good for a quick sanity check.

## How to Run

1. Generate the data:
   ```bash
   python3 generate_data.py
   ```

2. Process it:
   ```bash
   python3 simulate_accelerometer.py
   ```

3. (Optional) Check the results with C++:
   ```bash
   g++ print_accelerometer.cpp -o print_accelerometer
   ./print_accelerometer
   ```

That's pretty much it. The "outliers" are just random spikes I injected to make sure the detector works.