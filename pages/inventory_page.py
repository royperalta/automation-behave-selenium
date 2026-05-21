from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class InventoryPage(BasePage):

    APP_LOGO   = (By.CSS_SELECTOR, '.app_logo')
    CART_BADGE = (By.CSS_SELECTOR, '[data-test="shopping-cart-badge"]')
    CART_LINK  = (By.CSS_SELECTOR, '[data-test="shopping-cart-link"]')

    def _locator_boton_agregar(self, nombre_producto: str) -> tuple:
        id_producto = nombre_producto.lower().replace(" ", "-")
        selector    = f'[data-test="add-to-cart-{id_producto}"]'
        return (By.CSS_SELECTOR, selector)

    def agregar_producto_al_carrito(self, nombre_producto: str):
        """Hace click en Add to cart y espera que el badge aparezca."""
        locator = self._locator_boton_agregar(nombre_producto)
        self.click(locator)
        self.wait_for_element(self.CART_BADGE)

    def ir_al_carrito(self):
        """Hace click en el ícono del carrito."""
        self.click(self.CART_LINK)

    def obtener_cantidad_carrito(self) -> str:
        """Retorna el número del badge."""
        self.wait_for_element(self.CART_BADGE)
        return self.get_text(self.CART_BADGE)

    def obtener_titulo_app(self) -> str:
        """Retorna el texto del logo."""
        return self.get_text(self.APP_LOGO)

    def esta_en_inventario(self) -> bool:
        return "inventory.html" in self.get_current_url()