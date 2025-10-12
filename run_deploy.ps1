<#
PowerShell wrapper：使用 Ansible 執行部署 playbook。
前提：已安裝 Ansible（Windows 下可使用 WSL2 或透過 pip 安裝），以及已安裝 Docker 與 docker-compose，並允許 PowerShell 存取 Docker。
#>

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$ansibleDir = Join-Path $scriptDir "Infra_owner_demo\infra\ansible"

Write-Host "Installing Ansible collections (community.docker) if not present..."
ansible-galaxy collection install -r "$ansibleDir\requirements.yml"

Write-Host "Running deploy playbook..."
ansible-playbook -i "$ansibleDir\inventory.ini" "$ansibleDir\deploy_demo.yaml" -v

Read-Host -Prompt "Press Enter to finish"
