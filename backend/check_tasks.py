from app.database import SessionLocal, engine
from app.models import Playbook, Task
from sqlalchemy import inspect

inspector = inspect(engine)
print('Database tables:', inspector.get_table_names())

db = SessionLocal()
playbooks = db.query(Playbook).all()
print(f'\nTotal Playbooks: {len(playbooks)}')

for p in playbooks[:3]:
    tasks = db.query(Task).filter(Task.playbook_id == p.id).all()
    print(f'\nPlaybook #{p.id}: {p.name}')
    print(f'  Type: {p.type}, Status: {p.status}')
    print(f'  Tasks count: {len(tasks)}')
    for t in tasks[:3]:
        print(f'    - Task #{t.id}: order={t.order}, enabled={t.enabled}')
        print(f'      Content: {t.content[:80]}...')

db.close()
