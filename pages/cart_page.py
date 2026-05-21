"""
pages/cart_page.py
Page Object del carrito de compras.
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CartPage(BasePage):

    # ── Localizadores ─────────────────────────────────────────────────────
    ITEMS_EN_CARRITO = (By.CSS_SELECTOR, '[data-test="inventory-item-name"]')
    BOTON_CHECKOUT   = (By.CSS_SELECTOR, '[data-test="checkout"]')

    # ── Getters ───────────────────────────────────────────────────────────

    def obtener_nombres_productos(self) -> list[str]:
        """Retorna la lista de nombres de todos los productos en el carrito."""
        return self.get_texts(self.ITEMS_EN_CARRITO)

    # ── Acciones ──────────────────────────────────────────────────────────

    def click_checkout(self):
        """Hace click en el botón Checkout."""
        self.click(self.BOTON_CHECKOUT)
