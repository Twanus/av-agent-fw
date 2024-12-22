# av-agent-fw

## CI Workflow

### dev merge-into-main action when security-checks action is success

[![Current dev build is: ](https://github.com/Twanus/av-agent-fw/actions/workflows/branch-ci.yml/badge.svg)](https://github.com/Twanus/av-agent-fw/actions/workflows/branch-ci.yml)

[Advanced Security Report](adv-sec_verslag.md)

## Overview

The `av-agent-fw` is a flexible system-agent framework developed in Python. It integrates with GitHub to autonomously fetch and execute management tasks from a repository. The framework is designed to automate system administration tasks, ensuring consistency, real-time monitoring, scalability, and security.

## Features

- **Automation**: Reduces manual intervention in routine tasks like backups, system updates, and monitoring.
- **GitHub Integration**: Fetches modules and configurations from a GitHub repository.
- **Security**: Implements best practices such as encrypted communication, authentication, and input validation.
- **Modular Design**: Supports plug-ins for specific tasks, allowing easy extension and customization.

## Requirements

- Python 3.10+
- pip
- git

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/Twanus/av-agent-fw.git
   cd av-agent-fw
   ```

2. Set up a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure the environment variables:

   - Create a `.env` file in the root directory.
   - Add necessary environment variables such as
     - `AV_AGENT_SUDO_PASSWORD` this tool needs sudo access to update and install packages
     - `AV_AGENT_GITHUB_TOKEN`for github CI integration

5. Add the host key to the known_hosts file:

   - this is a security compliance of bandit (SAST tool)

   - On Linux/macOS, you can use the bash script:

   ```bash
   ./util/add_to_known_hosts.sh <hostname>
   ```

   - On Windows, you can use the PowerShell script:

     ```powershell
     .\util\add_to_known_hosts.ps1 -Hostname <hostname>
     ```

   - These scripts use the default path for the known_hosts file (~/.ssh/known_hosts)

## Usage

- Run the main agent script:

  ```bash
  python main.py
  ```

- The agent will execute tasks based on the modules configured in `config/config.yaml`.

## Contributing

Contributions are welcome! Please follow the standard GitHub workflow for submitting pull requests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or issues, please contact the repository owner via GitHub.
