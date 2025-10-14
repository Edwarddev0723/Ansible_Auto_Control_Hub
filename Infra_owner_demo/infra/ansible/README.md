Ansible 範例環境的 Playbooks

先決條件
- Ansible（建議使用 WSL2 在 Windows 上安裝）和 Python
- 已安裝 Docker 和 docker-compose，並且可供執行 Playbooks 的使用者使用
- 選擇性：如果本地執行前端建置，需安裝 Node.js 和 npm

Playbooks
- deploy_demo.yaml：建置前端（npm install, npm run build）、建置 Docker 映像檔，並啟動 docker-compose 堆疊。
- destroy_demo.yaml：關閉 docker-compose 堆疊並移除已建置的映像檔。

Playbooks執行方式
- ansible-playbook -i inventory.ini destroy_demo.yaml(playbook檔名)

注意事項(要先處理)
- deploy playbook 使用了 community.docker 集合（requirements.yml）。安裝方式：
    ansible-galaxy collection install -r Infra_owner_demo\infra\ansible\requirements.yml
- 在 Windows 上，建議從 WSL 執行 Playbooks，以避免 Docker 的路徑/權限問題。或者，確保 Docker Desktop 將守護程序暴露給 Windows，並且 Ansible 可以調用 Docker 命令。
