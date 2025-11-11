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
from app.models import Group, Host, Inventory, Playbook, Task

def seed_groups():
    """新增 Groups"""
    db = SessionLocal()
    try:
        groups = ['webservers', 'databases', 'loadbalancers', 'all']
        for group_name in groups:
            existing = db.query(Group).filter(Group.name == group_name).first()
            if not existing:
                db.add(Group(name=group_name))
        db.commit()
        print(f"✅ 已新增 {len(groups)} 個 Groups")
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
                "name": "Ansible GUI Inventory",
                "status": ServerStatus.ON,
                "ssh_status": "Connected",
                "config": "server1 ansible_ssh_host=127.0.0.1 ansible_ssh_port=55000 ansible_ssh_pass=docker"
            },
            {
                "name": "Ansible introduction Inventory",
                "status": ServerStatus.OFF,
                "ssh_status": "Unconnected",
                "config": "[webservers]\n192.168.1.10\n192.168.1.11\n\n[databases]\n192.168.1.12"
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
        
        # Playbook 1
        pb1 = db.query(Playbook).filter(Playbook.name == "Ansible GUI").first()
        if not pb1:
            pb1 = Playbook(
                name="Ansible GUI",
                type=PlaybookType.MACHINE,
                status=ExecutionStatus.SUCCESS,
                target_type=TargetType.GROUP,
                group="webservers",
                gather_facts=False
            )
            db.add(pb1)
            db.flush()
            
            # Tasks for Playbook 1
            tasks1 = [
                Task(playbook_id=pb1.id, order=0, enabled=True, 
                     content="name: test1\ncommunity:\n  name: demo\nstate: absent"),
                Task(playbook_id=pb1.id, order=1, enabled=True, 
                     content="name: test2\nCommunity2:\n  name: demo\nstate: absent"),
                Task(playbook_id=pb1.id, order=2, enabled=False, 
                     content="name: test3\ndebug:\n  msg: \"XXX\"")
            ]
            for task in tasks1:
                db.add(task)
        
        # Playbook 2
        pb2 = db.query(Playbook).filter(Playbook.name == "Ansible introduction").first()
        if not pb2:
            pb2 = Playbook(
                name="Ansible introduction",
                type=PlaybookType.MACHINE,
                status=ExecutionStatus.NOT_START,
                target_type=TargetType.HOST,
                host="192.168.1.10",
                gather_facts=True
            )
            db.add(pb2)
            db.flush()
            
            # Tasks for Playbook 2
            tasks2 = [
                Task(playbook_id=pb2.id, order=0, enabled=True, 
                     content="name: Install nginx\napt:\n  name: nginx\n  state: present")
            ]
            for task in tasks2:
                db.add(task)
        
        db.commit()
        print("✅ 已新增 2 個 Playbooks")
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
