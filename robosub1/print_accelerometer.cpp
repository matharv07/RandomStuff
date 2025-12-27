#include <algorithm>
#include <exception>
#include <fstream>
#include <iomanip>.
#include <iostream>
#include <map>
#include <sstream>
#include <string>
#include <vector>

using namespace std;

struct RawReading {
  int time_step;
  double ax, ay, az;
};

struct ProcessedReading {
  int time_step;
  double raw_x, raw_y, raw_z;
  double smooth_x, smooth_y, smooth_z;
  string is_outlier;
  double norm_x, norm_y, norm_z;
};

vector<RawReading> read_input_file(const string &filename) {
  vector<RawReading> data;
  ifstream file(filename);
  string line;

  if (!file.is_open()) {
    cerr << "Error opening input file: " << filename << endl;
    return data;
  }

  // Skip header
  getline(file, line);

  int line_num = 1;
  while (getline(file, line)) {
    line_num++;
    stringstream ss(line);
    string segment;
    RawReading reading;
    vector<string> row;

    while (getline(ss, segment, ',')) {
      row.push_back(segment);
    }

    if (row.size() >= 4) {
      try {
        reading.time_step = stoi(row[0]);
        reading.ax = stod(row[1]);
        reading.ay = stod(row[2]);
        reading.az = stod(row[3]);
        data.push_back(reading);
      } catch (const exception &e) {
        cerr << "Error parsing line " << line_num << " in " << filename << ": "
             << e.what() << endl;
      }
    }
  }
  return data;
}

map<int, ProcessedReading> read_output_file(const string &filename) {
  map<int, ProcessedReading> data;
  ifstream file(filename);
  string line;

  if (!file.is_open()) {
    cerr << "Error opening output file: " << filename << endl;
    return data;
  }

  // Skip header
  getline(file, line);

  int line_num = 1;
  while (getline(file, line)) {
    line_num++;
    stringstream ss(line);
    string segment;
    ProcessedReading reading;
    vector<string> row;

    while (getline(ss, segment, ',')) {
      row.push_back(segment);
    }

    // Expected fields: time_step, raw_x, raw_y, raw_z, smooth_x, smooth_y,
    // smooth_z, is_outlier, norm_x, norm_y, norm_z
    if (row.size() >= 11) {
      try {
        reading.time_step = stoi(row[0]);
        // Skip raw values in output file for now, we'll use input file for raw
        reading.smooth_x = stod(row[4]);
        reading.smooth_y = stod(row[5]);
        reading.smooth_z = stod(row[6]);
        reading.is_outlier = row[7];
        reading.norm_x = stod(row[8]);
        reading.norm_y = stod(row[9]);
        reading.norm_z = stod(row[10]);
        data[reading.time_step] = reading;
      } catch (const exception &e) {
        cerr << "Error parsing line " << line_num << " in " << filename << ": "
             << e.what() << endl;
      }
    }
  }
  return data;
}

int main() {
  string input_filename = "input_sensor_accelerometer.txt";
  string output_filename = "output_sensor_accelerometer.txt";

  vector<RawReading> raw_data = read_input_file(input_filename);
  map<int, ProcessedReading> processed_data = read_output_file(output_filename);

  if (raw_data.empty() || processed_data.empty()) {
    cerr << "Failed to read data." << endl;
    return 1;
  }

  // Print Header
  cout << left << setw(10) << "INDEX" << setw(25) << "RAW_INPUT (ax, ay, az)"
       << setw(30) << "PROCESSED_OUTPUT (smooth_x)" << endl;
  cout << string(65, '-') << endl;

  for (const auto &raw : raw_data) {
    if (processed_data.find(raw.time_step) != processed_data.end()) {
      const auto &proc = processed_data[raw.time_step];
      stringstream raw_ss;
      raw_ss << "[" << fixed << setprecision(2) << raw.ax << ", " << raw.ay
             << ", " << raw.az << "]";

      stringstream proc_ss;
      proc_ss << fixed << setprecision(2) << proc.smooth_x;
      if (proc.is_outlier == "True" || proc.is_outlier == "true") {
        proc_ss << " (OUTLIER)";
      }

      cout << left << setw(10) << raw.time_step << setw(25) << raw_ss.str()
           << setw(30) << proc_ss.str() << endl;
    } else {
      cerr << "Warning: No processed data for time step " << raw.time_step
           << endl;
    }
  }

  return 0;
}
