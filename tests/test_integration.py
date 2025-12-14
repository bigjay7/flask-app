import unittest

from app import create_app
from extensions import db
from models import Task, User


class TestIntegration(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        # On force la config pour utiliser SQLite en mémoire
        self.app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    # --- Helper pour se connecter ---
    def login(self, username, password):
        return self.client.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    # --- Test 1 : Inscription et Login ---
    def test_register_and_login(self):
        # 1. Inscription
        response = self.client.post('/register', data=dict(
            username='newuser',
            password='password123',
            confirm='password123'
        ), follow_redirects=True)
        
        self.assertIn(b'Registration successful', response.data)

        # 2. Connexion
        response = self.login('newuser', 'password123')
        self.assertIn(b'Logged in successfully', response.data)

    # --- Test 2 : Création de tâche ---
    def test_create_task(self):
        # Il faut d'abord créer un user et se connecter
        self.client.post('/register', data=dict(
            username='taskuser', password='pwd', confirm='pwd'
        ), follow_redirects=True)
        self.login('taskuser', 'pwd')

        # Création de la tâche
        response = self.client.post('/tasks/new', data=dict(
            title='Integration Task',
            description='Test description',
            due_date='2025-12-31'
        ), follow_redirects=True)

        self.assertIn(b'Task created', response.data)
        self.assertIn(b'Integration Task', response.data)

    # --- Test 3 : Toggle Tâche (Compléter) ---
    def test_toggle_task(self):
        # Setup User + Task
        with self.app.app_context():
            u = User(username='toggleuser')
            u.set_password('pwd')
            db.session.add(u)
            db.session.commit()
            
            t = Task(title='To Toggle', user_id=u.id)
            db.session.add(t)
            db.session.commit()
            task_id = t.id

        self.login('toggleuser', 'pwd')

        # Action : Toggle
        response = self.client.post(f'/tasks/{task_id}/toggle', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Vérification en base
        #0
        with self.app.app_context():
            task = Task.query.get(task_id)
            self.assertTrue(task.is_completed)

if __name__ == '__main__':
    unittest.main()