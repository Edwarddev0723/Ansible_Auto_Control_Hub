"""
建立或更新使用者的腳本（開發/測試用）。

用法範例（在專案根目錄、啟動虛擬環境後執行）：

PowerShell:
    python scripts/create_user.py --email admin@example.com --password YourPass123 --role admin

參數:
  --email    使用者 email
  --password 明文密碼（腳本會自動雜湊）
  --role     admin|developer|viewer (預設 viewer)
  --force    若使用者已存在則覆寫密碼與角色

注意: 此腳本直接寫入資料庫，請僅在開發或受信任的環境中使用。
"""

import argparse
import sys

from app.db.base import SessionLocal
from app.db import models
from app.core.security import get_password_hash


def main():
    parser = argparse.ArgumentParser(description="Create or update a user in the ansible_api DB")
    parser.add_argument("--email", required=True, help="User email")
    parser.add_argument("--password", required=True, help="Plain password")
    parser.add_argument("--role", default="viewer", choices=["admin", "developer", "viewer"], help="User role")
    parser.add_argument("--force", action="store_true", help="If set, overwrite existing user")

    args = parser.parse_args()

    session = SessionLocal()
    try:
        existing = session.query(models.User).filter(models.User.email == args.email).first()

        # bcrypt 原生有 72 bytes 的限制；若使用原生 bcrypt 會失敗。
        # 我們在此做保護性檢查：若密碼超過 72 bytes，則截斷成安全 utf-8 邊界的前 72 bytes
        # 並提示使用者。專案的 `app/core/security.py` 已改為 bcrypt_sha256，會自動處理較長密碼，
        # 但此處多做一層保險以相容不同環境。
        pw_bytes = args.password.encode('utf-8')
        if len(pw_bytes) > 72:
            print("警告: 密碼超過 72 bytes，將截斷到 72 bytes 以相容 bcrypt 限制。建議改用較短密碼或確認使用 bcrypt_sha256。")
            truncated = pw_bytes[:72]
            try:
                args.password = truncated.decode('utf-8')
            except UnicodeDecodeError:
                # 若截斷造成不完整 utf-8，忽略尾部不完整字元
                args.password = truncated.decode('utf-8', 'ignore')

        hashed = get_password_hash(args.password)

        # convert role string to enum
        try:
            role_enum = models.UserRole(args.role)
        except Exception:
            print(f"Invalid role: {args.role}")
            sys.exit(2)

        if existing:
            if not args.force:
                print(f"User with email {args.email} already exists. Use --force to overwrite.")
                return
            existing.hashed_password = hashed
            existing.role = role_enum
            session.add(existing)
            session.commit()
            print(f"Updated existing user {args.email} with new password and role {args.role}.")
            return

        user = models.User(email=args.email, hashed_password=hashed, role=role_enum)
        session.add(user)
        session.commit()
        print(f"Created user {args.email} with role {args.role}.")

    except Exception as e:
        print("Error creating/updating user:", e)
        raise
    finally:
        session.close()


if __name__ == "__main__":
    main()
