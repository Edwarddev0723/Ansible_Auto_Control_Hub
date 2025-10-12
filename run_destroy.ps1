<#
PowerShell wrapper：使用 Ansible 執行銷毀 playbook。
#>
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$ansibleDir = Join-Path $scriptDir "Infra_owner_demo\infra\ansible"

Write-Host "Running destroy playbook..."
ansible-playbook -i "$ansibleDir\inventory.ini" "$ansibleDir\destroy_demo.yaml" -v

Read-Host -Prompt "Press Enter to finish"
