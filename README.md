# Route53UpdateIP

This script automatically updates an AWS Route53 DNS record with your current public IP address.

## Prerequisites

- Python 3.6+
- AWS account with Route53 access
- Hosted zone in Route53 for your domain

## Installation

1. Clone this repository:

   ```
   git clone https://github.com/yourusername/Route53UpdateIP.git
   cd Route53UpdateIP
   ```

2. Install required packages:

   ```
   pip install -r requirements.txt
   ```

3. Copy `Route53UpdateIP.conf.example` to `Route53UpdateIP.conf` and fill in your AWS credentials and FQDN:
   ```
   cp Route53UpdateIP.conf.example Route53UpdateIP.conf
   nano Route53UpdateIP.conf
   ```

## Usage

Run the script manually:

```
python Route53UpdateIP.py
```

To set up automatic updates, add a cron job:

1. Open your crontab file:

   ```
   crontab -e
   ```

2. Add the following line to run the script every 15 minutes:

   ```
   */15 * * * * /usr/bin/python3 /path/to/Route53UpdateIP.py
   ```

3. Save and exit the editor.

## Running with Dev Containers in VS Code (Ubuntu Jammy 22.04 LTS)

If you're using the Dev Containers extension in VS Code with an Ubuntu Jammy 22.04 LTS container, follow these steps to set up and run the application:

1. Ensure you have the Dev Containers extension installed in VS Code.

2. Create a `.devcontainer` folder in your project root and add a `devcontainer.json` file with the following content:

   ```json
   {
     "name": "Ubuntu",
     "image": "ubuntu:22.04",
     "features": {
       "ghcr.io/devcontainers/features/python:1": {
         "version": "3.10"
       }
     },
     "postCreateCommand": "bash .devcontainer/setup.sh"
   }
   ```

3. Create a `setup.sh` file in the `.devcontainer` folder with the following content:

   ```bash
   #!/bin/bash
   set -e

   # Update package list and install dependencies
   sudo apt update
   sudo apt install -y python3-pip

   # Install project dependencies
   pip install -r requirements.txt

   # Set up the configuration file
   cp Route53UpdateIP.conf.example Route53UpdateIP.conf
   echo "Please update Route53UpdateIP.conf with your AWS credentials and FQDN."
   ```

4. Make the setup script executable:

   ```
   chmod +x .devcontainer/setup.sh
   ```

5. Reopen the project in a Dev Container:

   - Press `F1` or `Ctrl+Shift+P` to open the command palette
   - Type "Reopen in Container" and select the option

6. Once the container is built and running, open a terminal in VS Code.

7. Update the `Route53UpdateIP.conf` file with your AWS credentials and FQDN:

   ```
   nano Route53UpdateIP.conf
   ```

8. Run the script:

   ```
   python3 Route53UpdateIP.py
   ```

## Security Note

Ensure that your `Route53UpdateIP.conf` file has restricted permissions:

```
chmod 600 Route53UpdateIP.conf
```

Never share your AWS credentials or commit them to version control.

## License

This project is licensed under the MIT License.
