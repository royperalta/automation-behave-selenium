"""
pages/login_page.py
Page Object de la pantalla de Login de SauceDemo.

Hereda de BasePage → usa wait_for_clickable, fill, click, etc.
Los steps NUNCA usan driver.find_element directamente.
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):

    URL = "https://www.saucedemo.com/"

    # ── Localizadores (By.CSS_SELECTOR es preferido sobre By.XPATH) ──────
    # Se definen como constantes de clase para fácil mantenimiento.
    # Si SauceDemo cambia un selector, solo se cambia aquí.

    USERNAME_INPUT  = (By.CSS_SELECTOR, '[data-test="username"]')
    PASSWORD_INPUT  = (By.CSS_SELECTOR, '[data-test="password"]')
    LOGIN_BUTTON    = (By.CSS_SELECTOR, '[data-test="login-button"]')
    ERROR_MESSAGE   = (By.CSS_SELECTOR, '[data-test="error"]')
    LOGIN_LOGO      = (By.CSS_SELECTOR, '.login_logo')
    PRIMARY_HEADER  = (By.CSS_SELECTOR, '[data-test="primary-header"]')

    # ── Acciones ──────────────────────────────────────────────────────────

    def abrir_pagina(self):
        """Navega a SauceDemo. Equivalente a: await this.loginPage.abrirPagina()"""
        self.go_to(self.URL)

    def ingresar_credenciales(self, usuario: str, contrasena: str):
        """Rellena usuario y contraseña usando BasePage.fill() (con clear + send_keys)."""
        self.fill(self.USERNAME_INPUT, usuario)
        self.fill(self.PASSWORD_INPUT, contrasena)

    def click_login(self):
        """Click en el botón Login usando BasePage.click() (con espera explícita)."""
        self.click(self.LOGIN_BUTTON)

    def login(self, usuario: str, contrasena: str):
        """Acción compuesta para el Background: abrir + credenciales + submit."""
        self.abrir_pagina()
        self.ingresar_credenciales(usuario, contrasena)
        self.click_login()

    # ── Getters / Aserciones ──────────────────────────────────────────────

    def obtener_mensaje_error(self) -> str:
        """Retorna el texto del mensaje de error visible."""
        return self.get_text(self.ERROR_MESSAGE)

    def validar_texto_login(self):
        """Verifica que el título sea 'Swag Labs'."""
        texto = self.get_text(self.LOGIN_LOGO)
        assert texto == "Swag Labs", \
            f"Título esperado 'Swag Labs', obtenido '{texto}'"

    def obtener_header(self):
        """Verifica que el header principal sea visible tras login."""
        self.wait_for_visible(self.PRIMARY_HEADER)
