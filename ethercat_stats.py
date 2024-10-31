import subprocess
import time
import re

def run_ethercat_master():
    result = subprocess.run(['ethercat', 'master'], capture_output=True, text=True)
    return result.stdout

def extract_frame_rates(output):
    tx_match = re.search(r'Tx frame rate \[1/s\]:\s+(\d+)', output)
    rx_match = re.search(r'Rx frame rate \[1/s\]:\s+(\d+)', output)
    
    if tx_match and rx_match:
        tx_rate = int(tx_match.group(1))
        rx_rate = int(rx_match.group(1))
        return tx_rate, rx_rate
    else:
        return None, None

def main():
    tx_total = 0
    rx_total = 0
    valid_runs = 0

    print("Starting measurement...")
    for i in range(10):
        print(f"Collecting data: {i+1}/10")
        output = run_ethercat_master()
        tx_rate, rx_rate = extract_frame_rates(output)
        
        if tx_rate is not None and rx_rate is not None:
            valid_runs += 1
            tx_total += tx_rate
            rx_total += rx_rate
        else:
            print("  Warning: Failed to extract data from this run.")
        
        time.sleep(1)

    print("Measurement complete. Calculating results...")

    if valid_runs > 0:
        tx_avg = round(tx_total / valid_runs, 2)
        rx_avg = round(rx_total / valid_runs, 2)
        
        print(f"\nResults based on {valid_runs} valid measurements:")
        print(f"Average TX Frame rate [1/s]: {tx_avg}")
        print(f"Average RX Frame rate [1/s]: {rx_avg}")
    else:
        print("\nError: No valid data was collected.")

if __name__ == "__main__":
    main()
