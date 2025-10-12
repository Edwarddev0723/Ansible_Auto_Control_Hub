Ansible playbooks for demo environment

Pre-requisites
- Ansible (recommended via WSL2 on Windows) and Python
- Docker and docker-compose installed and available to the user running playbooks
- Optional: Node.js and npm if you run frontend build locally

Playbooks
- deploy_demo.yaml: Builds the frontend (npm install, npm run build), builds docker image and brings up the docker-compose stack.
- destroy_demo.yaml: Tears down the docker-compose stack and removes the built image.

Usage (PowerShell)
From repository root:
    .\run_deploy.ps1
    .\run_destroy.ps1

Notes
- The deploy playbook uses the community.docker collection (requirements.yml). Install via:
    ansible-galaxy collection install -r Infra_owner_demo\infra\ansible\requirements.yml
- On Windows, run the playbooks from WSL if possible to avoid path/permission issues with Docker. Alternatively ensure Docker Desktop exposes daemon to Windows and Ansible can call docker commands.
