import time
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By


class TestE2E(unittest.TestCase):

    def setUp(self):
        # Configuration de Chrome (mode sans tête optionnel)
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless') # Décommenter pour ne pas voir la fenêtre
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(5) # Attente implicite
        self.base_url = "http://localhost:5000"

    def tearDown(self):
        self.driver.quit()

    def test_full_flow(self):
        driver = self.driver
        
        # 1. Aller sur la page de login (ou register)
        driver.get(f"{self.base_url}/register")
        
        # Générer un user unique pour éviter les conflits si on relance le test
        unique_user = f"user_{int(time.time())}"
        
        # 2. Remplir le formulaire d'inscription
        driver.find_element(By.NAME, "username").send_keys(unique_user)
        driver.find_element(By.NAME, "password").send_keys("secret")
        driver.find_element(By.NAME, "confirm").send_keys("secret")
        driver.find_element(By.TAG_NAME, "form").submit()
        
        # 3. Connexion (si redirection vers login)
        # Vérifie si on est sur /login ou déjà connecté selon ton app
        if "login" in driver.current_url:
            driver.find_element(By.NAME, "username").send_keys(unique_user)
            driver.find_element(By.NAME, "password").send_keys("secret")
            driver.find_element(By.TAG_NAME, "form").submit()

if __name__ == '__main__':
    unittest.main()