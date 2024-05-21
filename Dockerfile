# Use the official Python image as the base image
FROM ubuntu:latest

# Install necessary packages (e.g., curl, jq, etc.) for setting up Trivy
RUN apt-get update && \
    apt-get install -y --no-install-recommends ca-certificates wget curl jq && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Trivy
RUN wget -qO - https://github.com/aquasecurity/trivy/releases/download/v0.20.0/trivy_0.20.0_Linux-64bit.tar.gz | tar -xz -C /usr/local/bin trivy \
    && chmod +x /usr/local/bin/trivy

# Set the working directory in the container
WORKDIR /app

# Copy the local file into the container at /app
COPY TechniquesAndCVEs.txt /app/

# Create a script file with the commands you want to run
RUN echo '#!/bin/bash' > run_commands.sh && \
    echo 'trivy k8s --report all pod | grep -o "CVE-[0-9]\{4\}-[0-9]\{4,9\}" > trivy_cves.txt' >> run_commands.sh && \
    echo 'grep -wFf trivy_cves.txt TechniquesAndCVEs.txt | sort > matched_cves.txt' >> run_commands.sh && \
    chmod +x run_commands.sh

# Execute the script as the CMD
CMD ["./run_commands.sh"]