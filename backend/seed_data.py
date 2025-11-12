#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
資料庫初始化種子資料
"""
import sys
import io

# 設置標準輸出為 UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from app.database import SessionLocal
from app.models import Group, Host, Inventory, Playbook, Task, PlaybookExtraField

def seed_groups():
    """新增 Groups"""
    db = SessionLocal()
    try:
        groups_data = [
            {'name': 'webservers'},
            {'name': 'databases'},
            {'name': 'loadbalancers'},
            {'name': 'all'}
        ]
        for group_data in groups_data:
            existing = db.query(Group).filter(Group.name == group_data['name']).first()
            if not existing:
                db.add(Group(**group_data))
        db.commit()
        print(f"✅ 已新增 {len(groups_data)} 個 Groups")
    finally:
        db.close()

def seed_hosts():
    """新增 Hosts"""
    db = SessionLocal()
    try:
        hosts = [
            '192.168.1.10',
            '192.168.1.11',
            '192.168.1.12',
            'server1.example.com',
            'server2.example.com'
        ]
        for host_addr in hosts:
            existing = db.query(Host).filter(Host.address == host_addr).first()
            if not existing:
                db.add(Host(address=host_addr))
        db.commit()
        print(f"✅ 已新增 {len(hosts)} 個 Hosts")
    finally:
        db.close()

def seed_inventories():
    """新增 Inventories"""
    db = SessionLocal()
    try:
        from app.models import ServerStatus
        inventories = [
            {
                "name": "test_inventor",
                "status": ServerStatus.ON,
                "ssh_status": "Connected",
                "group": "databases",
                "config": "eason ansible_ssh_host=127.0.0.1 ansible_ssh_port=22 ansible_ssh_user=eason ansible_ssh_pass=ansible123"
            },
            {
                "name": "web_server_1",
                "status": ServerStatus.OFF,
                "ssh_status": "Unconnected",
                "group": "webservers",
                "config": "web1 ansible_ssh_host=192.168.1.10 ansible_ssh_port=22 ansible_ssh_user=admin ansible_ssh_pass=admin123"
            }
        ]
        
        for inv_data in inventories:
            existing = db.query(Inventory).filter(Inventory.name == inv_data["name"]).first()
            if not existing:
                db.add(Inventory(**inv_data))
        db.commit()
        print(f"✅ 已新增 {len(inventories)} 個 Inventories")
    finally:
        db.close()

def seed_playbooks():
    """新增 Playbooks"""
    db = SessionLocal()
    try:
        from app.models import PlaybookType, ExecutionStatus, TargetType
        import json
        
        # Playbook 1: Deploy Demo
        pb1 = db.query(Playbook).filter(Playbook.name == "test").first()
        if not pb1:
            pb1 = Playbook(
                name="test",
                type=PlaybookType.MACHINE,
                status=ExecutionStatus.SUCCESS,
                target_type=TargetType.GROUP,
                group="databases",
                gather_facts=False
            )
            db.add(pb1)
            db.flush()
            
            # Tasks for Deploy Demo Playbook
            tasks1 = [
                Task(
                    playbook_id=pb1.id, 
                    order=0, 
                    enabled=True,
                    content="""name: 11111
shell: |
  source ~/.nvm/nvm.sh
  npm install
args:
  chdir: "{{ playbook_dir }}/../../frontend"
  executable: /bin/bash
register: npm_install"""
                ),
                Task(
                    playbook_id=pb1.id, 
                    order=1, 
                    enabled=True,
                    content="""name: 22222222222
shell: |
  source ~/.nvm/nvm.sh
  npm run build
args:
  chdir: "{{ playbook_dir }}/../../frontend"
  executable: /bin/bash
register: npm_build"""
                ),
                Task(
                    playbook_id=pb1.id, 
                    order=2, 
                    enabled=True,
                    content="""name: 3333333333
community.docker.docker_compose_v2:
  project_src: "{{ playbook_dir }}/.."
  build: always
  state: present
register: compose_up"""
                ),
                Task(
                    playbook_id=pb1.id, 
                    order=3, 
                    enabled=True,
                    content="""name: 44444444
debug:
  msg: "Compose result: {{ compose_up }}" """
                )
            ]
            for task in tasks1:
                db.add(task)
            
            # 新增 working_directory 到 extra_fields
            from app.models import PlaybookExtraField
            extra_field = PlaybookExtraField(
                playbook_id=pb1.id,
                field_value=json.dumps({
                    "working_directory": "C:\\Users\\user\\Desktop\\school_work\\internet_wesly\\Infra_owner_demo\\infra\\ansible"
                })
            )
            db.add(extra_field)
        
        # Playbook 2: Destroy Demo
        pb2 = db.query(Playbook).filter(Playbook.name == "destroy_demo").first()
        if not pb2:
            pb2 = Playbook(
                name="destroy_demo",
                type=PlaybookType.MACHINE,
                status=ExecutionStatus.NOT_START,
                target_type=TargetType.GROUP,
                group="databases",
                gather_facts=False
            )
            db.add(pb2)
            db.flush()
            
            # Tasks for Destroy Demo Playbook
            tasks2 = [
                Task(
                    playbook_id=pb2.id, 
                    order=0, 
                    enabled=True,
                    content="""name: 停止並移除 Docker Compose 服務
community.docker.docker_compose_v2:
  project_src: "{{ playbook_dir }}/.."
  state: absent
register: compose_down"""
                ),
                Task(
                    playbook_id=pb2.id, 
                    order=1, 
                    enabled=True,
                    content="""name: 刪除 Docker 映像檔
community.docker.docker_image:
  name: vue-static-demo
  tag: latest
  state: absent
  force_absent: true
register: image_removed"""
                ),
                Task(
                    playbook_id=pb2.id, 
                    order=2, 
                    enabled=True,
                    content="""name: 顯示結果
debug:
  msg: "Compose down: {{ compose_down }}, image removed: {{ image_removed }}" """
                )
            ]
            for task in tasks2:
                db.add(task)
            
            # 新增 working_directory 到 extra_fields
            extra_field2 = PlaybookExtraField(
                playbook_id=pb2.id,
                field_value=json.dumps({
                    "working_directory": "C:\\Users\\user\\Desktop\\school_work\\internet_wesly\\Infra_owner_demo\\infra\\ansible"
                })
            )
            db.add(extra_field2)
        
        db.commit()
        print("✅ 已新增 2 個 Playbooks (含 working_directory)")
    finally:
        db.close()

if __name__ == "__main__":
    print("開始初始化資料庫...")
    print("-" * 50)
    
    seed_groups()
    seed_hosts()
    seed_inventories()
    seed_playbooks()
    
    print("-" * 50)
    print("✅ 資料庫初始化完成！")
