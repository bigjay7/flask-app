import os
import unittest
from datetime import date, timedelta
from unittest.mock import patch

# Assure-toi que l'import correspond à ton arborescence
from app import _build_postgres_uri
from models import Task, User


class TestUnitaires(unittest.TestCase):

    # --- Test 1 : Logique de l'URI (Demandé par le TP) ---
    def test_build_postgres_uri(self):
        """Vérifie la construction de l'URL Postgres si DATABASE_URL est absent."""
        # On simule des variables d'environnement
        env_vars = {
            "POSTGRES_USER": "testuser",
            "POSTGRES_PASSWORD": "password",
            "POSTGRES_HOST": "localhost",
            "POSTGRES_PORT": "5432",
            "POSTGRES_DB": "testdb"
        }
        
        # On patch os.environ pour simuler l'absence de DATABASE_URL
        with patch.dict(os.environ, env_vars, clear=True):
             # clear=True enlève temporairement DATABASE_URL s'il existe
            uri = _build_postgres_uri()
            expected = "postgresql+psycopg2://testuser:password@localhost:5432/testdb"
            self.assertEqual(uri, expected)

    # --- Test 2 : Modèle User (Hashage mot de passe) ---
    def test_user_password(self):
        u = User(username='testunit')
        u.set_password('monMotDePasse')
        
        # Vérifie que le hash n'est pas le mot de passe en clair
        self.assertNotEqual(u.password_hash, 'monMotDePasse')
        # Vérifie que la vérification fonctionne
        self.assertTrue(u.check_password('monMotDePasse'))
        self.assertFalse(u.check_password('mauvaisPass'))

    # --- Test 3 : Modèle Task (Logique is_overdue) ---
    def test_task_is_overdue(self):
        # Cas 1: Date passée, non complétée -> En retard
        hier = date.today() - timedelta(days=1)
        t1 = Task(title="Retard", due_date=hier, is_completed=False)
        self.assertTrue(t1.is_overdue())

        # Cas 2: Date future -> Pas en retard
        demain = date.today() + timedelta(days=1)
        t2 = Task(title="Futur", due_date=demain, is_completed=False)
        self.assertFalse(t2.is_overdue())

        # Cas 3: Date passée mais complétée -> Pas en retard
        t3 = Task(title="Fini", due_date=hier, is_completed=True)
        self.assertFalse(t3.is_overdue())
if __name__ == '__main__':
    unittest.main()