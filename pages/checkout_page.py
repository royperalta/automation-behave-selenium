"""
pages/checkout_page.py
Page Object del proceso de checkout (2 pasos + confirmación).
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CheckoutPage(BasePage):

    # ── Localizadores — Paso 1: Datos personales ──────────────────────────
    FIRST_NAME_INPUT  = (By.CSS_SELECTOR, '[data-test="firstName"]')
    LAST_NAME_INPUT   = (By.CSS_SELECTOR, '[data-test="lastName"]')
    POSTAL_CODE_INPUT = (By.CSS_SELECTOR, '[data-test="postalCode"]')
    BOTON_CONTINUE    = (By.CSS_SELECTOR, '[data-test="continue"]')

    # ── Localizadores — Paso 2: Resumen y confirmación ────────────────────
    BOTON_FINISH         = (By.CSS_SELECTOR, '[data-test="finish"]')
    MENSAJE_CONFIRMACION = (By.CSS_SELECTOR, '[data-test="complete-header"]')

    # ── Acciones ──────────────────────────────────────────────────────────

    def completar_datos_personales(self, nombre: str, apellido: str, codigo_postal: str):
        """Rellena el formulario del paso 1 del checkout."""
        self.fill(self.FIRST_NAME_INPUT,  nombre)
        self.fill(self.LAST_NAME_INPUT,   apellido)
        self.fill(self.POSTAL_CODE_INPUT, codigo_postal)

    def click_continue(self):
        self.click(self.BOTON_CONTINUE)

    def click_finish(self):
        self.click(self.BOTON_FINISH)

    # ── Getters ───────────────────────────────────────────────────────────

    def obtener_mensaje_confirmacion(self) -> str:
        return self.get_text(self.MENSAJE_CONFIRMACION)
