# 階段 1: 使用輕量級 Nginx 映像檔
FROM nginx:alpine

# 移除預設的 Nginx 歡迎頁
RUN rm -rf /usr/share/nginx/html/*

# 複製 Nginx 設定檔
# 使用專門的設定來服務單頁應用 (SPA) 和映射端口
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 將 Vue 靜態檔案複製到 Nginx 的服務目錄
# 假設 frontend/dist/ 是 Vue 專案編譯後的靜態檔案
COPY dist /usr/share/nginx/html/

# 容器內部 Nginx 預設運行在 80 端口
EXPOSE 80

# Nginx 預設 CMD 保持不變