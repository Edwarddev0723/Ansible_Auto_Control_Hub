# Ansible 範例環境的 Playbooks

## 先決條件
- 安裝 [Ansible](https://docs.ansible.com/)（建議使用 WSL2 在 Windows 上安裝）和 [Python](https://www.python.org/)
- 安裝 [Docker](https://www.docker.com/) 和 [docker-compose](https://docs.docker.com/compose/)，並確保執行 Playbooks 的使用者有權限使用
- **選擇性**：若需本地執行前端建置，請安裝 [Node.js](https://nodejs.org/) 和 [npm](https://www.npmjs.com/)

## Playbooks
- **`deploy_demo.yaml`**：執行以下操作：
    - 安裝前端依賴（`npm install`）
    - 建置前端（`npm run build`）
    - 建置 Docker 映像檔
    - 啟動 docker-compose 堆疊
- **`destroy_demo.yaml`**：執行以下操作：
    - 關閉 docker-compose 堆疊
    - 移除已建置的映像檔

## Playbooks 執行方式
1. 切換到目錄：
     ```bash
     cd Infra_owner_demo/infra/ansible
     ```
2. 執行 Playbook：
     ```bash
     ansible-playbook -i inventory.ini <playbook檔名>
     ```
     範例：
     ```bash
     ansible-playbook -i inventory.ini destroy_demo.yaml
     ```

## 注意事項
1. **安裝必要集合**  
     `deploy_demo.yaml` 使用了 `community.docker` 集合，請先安裝：
     ```bash
     ansible-galaxy collection install -r Infra_owner_demo/infra/ansible/requirements.yml
     ```
2. **Windows 使用者建議**  
     - 建議從 WSL 執行 Playbooks，以避免 Docker 的路徑或權限問題。
     - 或者，確保 Docker Desktop 已將守護程序暴露給 Windows，並且 Ansible 可以調用 Docker 命令。
3. **靜態檔案處理**  
     由於 Vue 打包後的 `dist` 資料夾已加入 `.gitignore`，執行 Playbooks 前需：
     - 在 `frontend` 資料夾執行打包程序：
         ```bash
         npm run build
         ```
     - 將打包後的 `dist` 資料夾內容移至 `infra/dist` 目錄下。

