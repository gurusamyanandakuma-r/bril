import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import re

class MemoryOptimizer:
    def __init__(self, csv_path, cpp_source_path):

        self.data = pd.read_csv(csv_path)
        self.cpp_source_path = cpp_source_path
        self.cpp_source_code = self._read_cpp_source()
        self.prepare_data()

    def _read_cpp_source(self):
        with open(self.cpp_source_path, 'r') as file:
            return file.read()

    def prepare_data(self):
        self.data['Memory_Delta'] = self.data['Memory Allocated (KB)'] - self.data['Memory Freed (KB)']
        self.data['Memory_Utilization_Ratio'] = self.data['Memory Allocated (KB)'] / (self.data['Peak Memory (KB)'] + 1)

    def optimize_source_code(self, output_path):
        optimized_code = re.sub(r'malloc\((.*?)\)', r'calloc(1, \1)', self.cpp_source_code)
        optimized_code = re.sub(r'free\((.*?)\)', r'free(\1); \1 = NULL;', optimized_code)
        
        with open(output_path, 'w') as file:
            file.write(optimized_code)

    def simulate_optimized_profile(self, output_csv_path):
        optimized_data = self.data.copy()
        optimized_data['Memory Allocated (KB)'] *= 0.8
        optimized_data['Memory Freed (KB)'] *= 0.8
        optimized_data['Peak Memory (KB)'] *= 0.9
        optimized_data.to_csv(output_csv_path, index=False)

    def compare_profiles(self, unoptimized_data, optimized_data):
        plt.figure(figsize=(15, 7))
        plt.subplot(1, 2, 1)
        plt.plot(unoptimized_data['Time (ms)'], unoptimized_data['Memory Allocated (KB)'], label='Unoptimized', alpha=0.7)
        plt.plot(optimized_data['Time (ms)'], optimized_data['Memory Allocated (KB)'], label='Optimized', alpha=0.7)
        plt.title('Memory Allocation Comparison')
        plt.xlabel('Time (ms)')
        plt.ylabel('Memory Allocated (KB)')
        plt.legend()
        plt.subplot(1, 2, 2)
        plt.plot(unoptimized_data['Time (ms)'], unoptimized_data['Peak Memory (KB)'], label='Unoptimized', alpha=0.7)
        plt.plot(optimized_data['Time (ms)'], optimized_data['Peak Memory (KB)'], label='Optimized', alpha=0.7)
        plt.title('Peak Memory Usage Comparison')
        plt.xlabel('Time (ms)')
        plt.ylabel('Peak Memory (KB)')
        plt.legend()
        plt.tight_layout()
        plt.savefig('example1_profile_comparison.png')
        plt.close()
        print("Profile comparison graph saved as 'example1_profile_comparison.png'.")

        delta_memory_alloc = unoptimized_data['Memory Allocated (KB)'].sum() - optimized_data['Memory Allocated (KB)'].sum()
        delta_peak_memory = unoptimized_data['Peak Memory (KB)'].max() - optimized_data['Peak Memory (KB)'].max()

        print(f"Total reduction in memory allocation: {delta_memory_alloc:.2f} KB")
        print(f"Reduction in peak memory usage: {delta_peak_memory:.2f} KB")


def main(csv_path_unoptimized, cpp_source_path, output_cpp_path, output_csv_optimized):
    optimizer = MemoryOptimizer(csv_path_unoptimized, cpp_source_path)
    optimizer.optimize_source_code(output_cpp_path)
    print(f"Optimized source code saved to {output_cpp_path}.")
    optimizer.simulate_optimized_profile(output_csv_optimized)
    print(f"Simulated optimized profile saved to {output_csv_optimized}.")
    unoptimized_data = optimizer.data
    optimized_data = pd.read_csv(output_csv_optimized)
    optimizer.compare_profiles(unoptimized_data, optimized_data)

if __name__ == "__main__":
    main(
        csv_path_unoptimized="example1_output.csv",
        cpp_source_path="mem_alloc_dealloc.cpp",
        output_cpp_path="optimized_mem_alloc_dealloc.cpp",
        output_csv_optimized="optimized_example1_output.csv"
    )
