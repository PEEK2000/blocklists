import requests
import os
import csv
import re

# Define paths
BASE_DIR = os.path.dirname(__file__)
OUTPUT_DIR = os.path.join(BASE_DIR, "blocklists_converted")
CSV_DIR = os.path.join(BASE_DIR, "AdGuard_blocklists.csv")

# Fetch blocklist data from the AdGuard_blocklists.csv file
def fetch_blocklist(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text.splitlines()

# Add disclaimer and convert blocklist to HOSTS format and extract whitelisted domains
def convert_to_hosts_format(blocklist, url):
    disclaimer = [
        "# This blocklist was converted to HOSTS syntax to allow it being used with Pi-Hole.",
        f"# All credits go to the original repository: {url}\n"
    ]
    
    domain_pattern = re.compile(r'\|\|([^|^]+)\^')  # Extract domains between "||" and "^"
    
    hosts_lines = []
    
    for line in blocklist:
        # Ignore comments and empty lines
        if line.startswith(('!', '#', '@')) or not line:
            continue

        # Check for regular blocklist domain and add to hosts_lines if found
        if domain_match := domain_pattern.search(line):
            hosts_lines.append(f"0.0.0.0 {domain_match.group(1).strip()}")

    return disclaimer + hosts_lines

# Save list of lines to the specified directory
def save_to_file(lines, filename):
    output_path = os.path.join(OUTPUT_DIR, f"{filename}.txt")
    os.makedirs(OUTPUT_DIR, exist_ok=True)  # Ensure output directory exists
    with open(output_path, 'w') as file:
        file.write("\n".join(lines))
    print(f"Blocklist saved to {output_path}")

def main():
    try:
        with open(CSV_DIR, newline='') as csvfile:
            for url, output_filename in csv.reader(csvfile):
                blocklist = fetch_blocklist(url)
                hosts_lines = convert_to_hosts_format(blocklist, url)
                save_to_file(hosts_lines, output_filename)
    except Exception as e:
        print(f"An error occurred: {e}")  # Print Error-message if necessary

if __name__ == "__main__":
    main()
    print("Conversion completed.")
