import pytest
from selenium import webdriver
from Seccion3.login_page import LoginPage # Usando el modelo POM que creamos antes

@pytest.fixture
def driver():
 """Configuración inicial del navegador (Fixture)"""
 driver = webdriver.Chrome()
 driver.implicitly_wait(10)
 yield driver
 driver.quit()

def test_login_fallido(driver):
 """Prueba de usuario bloqueado"""
 driver.get("https://saucedemo.com")
 login = LoginPage(driver)

 login.ingresar_credenciales("locked_out_user", "secret_sauce")
 login.click_login()

 assert "no ingresó" in login.obtener_error()
 
def test_login_exitoso(driver):
 """Prueba de login correcto"""
 driver.get("https://saucedemo.com")
 login = LoginPage(driver)

 login.ingresar_credenciales("standard_user", "secret_sauce")
 login.click_login()

 assert "inventory.html" in driver.current_url