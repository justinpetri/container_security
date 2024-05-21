# mitre-map

I want to thank Garrett Wegmann and Austin Mason for working with me on this project. Mitre Map serves as a tool to scan and identify vulnerabilities in containers using Trivy (https://trivy.dev). It goes a step further by pointing the CVEs identified to specific techniques in the MITRE ATT&CK framework. It is worth noting this requires additional work as the mapping of CVEs to MITRE Techniques is not fully complete. The python file is supposed to be run on a kubernetes host that already has Trivy installed and a series of running pods.

The mitremap.py file REQUIRES the use of "TechniquesAndCVEs.txt" which manually maps CVEs to ATT&CK techniques. It then runs a series of Trivy scans on the local kubernetes cluster, uses regex to find matches against the TechniquesAndCVEs.txt file, then stores the output neatly in output.json.

The attached "output.json" file is an example of the mappings identified in a test scenario.
