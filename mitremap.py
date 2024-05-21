import subprocess
import json
import os
import sys

# Specify the filename to check
file_to_check = "TechniquesAndCVEs.txt"

# Check if the file exists in the current directory
if not os.path.exists(file_to_check):
    print(f"The file '{file_to_check}' does not exist in the current directory.")
    sys.exit(1)  # Exit the program with a non-zero status code

# Continue with the rest of your program logic here if the file exists
print(f"The file '{file_to_check}' exists in the current directory.")

print("Running Trivy scan...")
run_trivy_scan = "trivy k8s --report all pod | grep -o 'CVE-[0-9]\{4\}-[0-9]\{4,9\}' > trivy_cves.txt"
get_trivy_cves = subprocess.run(run_trivy_scan, shell=True, text=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print("Outputted results into trivy_cves.txt")

compare_trivy_mitre = "grep -wFf trivy_cves.txt TechniquesAndCVEs.txt | sort > matched_cves.txt"
compare_cves = subprocess.run(compare_trivy_mitre, shell=True, text=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print("Matched CVEs and stored in matched_cves.txt")

# Read the mapped CVEs from the file
with open('matched_cves.txt', 'r') as matched_cves_file:
    matched_cves = matched_cves_file.readlines()

# Function to generate technique URL
def get_technique_url(technique):
    return f"https://attack.mitre.org/techniques/{technique}"

cve_data = []

# Loop through each line of matched CVEs
for line in matched_cves:
    # Split the line into CVE ID and techniques
    parts = line.split(' ', 1)
    cve_id = parts[0]
    techniques = parts[1].split()

    # Create a dictionary for each CVE and its techniques
    cve_info = {
        'CVE': cve_id,
        'Techniques': [{'Technique': technique, 'Website': f"https://attack.mitre.org/techniques/{technique}"} for technique in techniques]
    }

    # Append CVE info to the list
    cve_data.append(cve_info)

# Specify the output JSON file
output_json_file = 'output.json'

# Write the processed data to a JSON file
with open(output_json_file, 'w') as json_file:
    json.dump(cve_data, json_file, indent=4)

print(f"Processed data has been stored in {output_json_file} in clean JSON format.")

# Comment out these lines if you don't want to remove the results from the scan and the compare
file_cleanup = "rm matched_cves.txt trivy_cves.txt"
get_trivy_cves = subprocess.run(file_cleanup, shell=True, text=True)