"""
pages/inventory_page.py
Page Object de la página de inventario (lista de productos).
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class InventoryPage(BasePage):

    # ── Localizadores ─────────────────────────────────────────────────────
    APP_LOGO    = (By.CSS_SELECTOR, '.app_logo')
    CART_BADGE  = (By.CSS_SELECTOR, '[data-test="shopping-cart-badge"]')
    CART_LINK   = (By.CSS_SELECTOR, '[data-test="shopping-cart-link"]')

    # ── Helpers ───────────────────────────────────────────────────────────

    def _locator_boton_agregar(self, nombre_producto: str) -> tuple:
        """
        Genera el locator dinámico del botón 'Add to cart' de un producto.
        'Sauce Labs Backpack' → [data-test='add-to-cart-sauce-labs-backpack']
        """
        id_producto = nombre_producto.lower().replace(" ", "-")
        selector    = f'[data-test="add-to-cart-{id_producto}"]'
        return (By.CSS_SELECTOR, selector)

    # ── Acciones ──────────────────────────────────────────────────────────

    def agregar_producto_al_carrito(self, nombre_producto: str):
    """Hace click en 'Add to cart' y espera que el badge aparezca."""
    locator = self._locator_boton_agregar(nombre_producto)
    self.click(locator)
    # Esperar que el badge aparezca en el DOM después del click
    self.wait_for_element(self.CART_BADGE)



    def ir_al_carrito(self):
        """Hace click en el ícono del carrito."""
        self.click(self.CART_LINK)

    # ── Getters ───────────────────────────────────────────────────────────

    def obtener_cantidad_carrito(self) -> str:
    """Retorna el número del badge — espera que sea visible."""
    # presence primero, luego visible (más robusto en headless)
    self.wait_for_element(self.CART_BADGE)
    return self.get_text(self.CART_BADGE)

    def obtener_titulo_app(self) -> str:
        """Retorna el texto del logo ('Swag Labs')."""
        return self.get_text(self.APP_LOGO)

    def esta_en_inventario(self) -> bool:
        return "inventory.html" in self.get_current_url()
