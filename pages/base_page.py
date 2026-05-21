"""
pages/base_page.py — Clase base del POM (Page Object Model)

¿Por qué existe BasePage?
  Selenium NO tiene auto-espera como Playwright.
  Si haces driver.find_element() sin esperar, el test falla
  si el elemento aún no está en el DOM.

  BasePage centraliza toda la lógica de espera explícita
  (WebDriverWait + expected_conditions) para que las páginas
  hijas NUNCA repitan este código.

  Jerarquía:
    BasePage          ← métodos genéricos con waits
      ├── LoginPage
      ├── InventoryPage
      ├── CartPage
      └── CheckoutPage

  En Playwright esto NO existía porque Playwright espera
  automáticamente. En Selenium es OBLIGATORIO.
"""
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class BasePage:
    """
    Clase padre de todos los Page Objects.
    Encapsula WebDriverWait para que las páginas hijas usen
    métodos limpios sin repetir lógica de espera.
    """

    def __init__(self, driver: WebDriver, timeout: int = 10):
        self.driver  = driver
        self.timeout = timeout
        self.wait    = WebDriverWait(driver, timeout)

    # ──────────────────────────────────────────────────────────
    # MÉTODOS DE ESPERA — el corazón de Selenium POM
    # Estos métodos BLOQUEAN hasta que el elemento esté listo
    # ──────────────────────────────────────────────────────────

    def wait_for_element(self, locator: tuple) -> WebElement:
        """
        Espera hasta que el elemento esté PRESENTE en el DOM.
        Útil para: verificar que existe antes de interactuar.

        locator = (By.CSS_SELECTOR, '[data-test="username"]')
        """
        return self.wait.until(
            EC.presence_of_element_located(locator),
            message=f"Elemento no encontrado: {locator}"
        )

    def wait_for_clickable(self, locator: tuple) -> WebElement:
        """
        Espera hasta que el elemento sea VISIBLE y CLICKEABLE.
        Usar para: botones, links, checkboxes.
        """
        return self.wait.until(
            EC.element_to_be_clickable(locator),
            message=f"Elemento no clickeable: {locator}"
        )

    def wait_for_visible(self, locator: tuple) -> WebElement:
        """
        Espera hasta que el elemento sea VISIBLE (en pantalla).
        Usar para: textos, imágenes, mensajes de error.
        """
        return self.wait.until(
            EC.visibility_of_element_located(locator),
            message=f"Elemento no visible: {locator}"
        )

    def wait_for_url_contains(self, fragment: str):
        """Espera hasta que la URL contenga el fragmento dado."""
        self.wait.until(
            EC.url_contains(fragment),
            message=f"URL no contiene '{fragment}'. URL actual: {self.driver.current_url}"
        )

    def wait_for_text_in_element(self, locator: tuple, texto: str):
        """Espera hasta que el elemento contenga el texto dado."""
        self.wait.until(
            EC.text_to_be_present_in_element(locator, texto),
            message=f"Texto '{texto}' no encontrado en {locator}"
        )

    def element_exists(self, locator: tuple) -> bool:
        """Verifica si un elemento existe en el DOM (sin espera larga)."""
        try:
            WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    # ──────────────────────────────────────────────────────────
    # MÉTODOS DE ACCIÓN — abstraen find_element + acción
    # ──────────────────────────────────────────────────────────

    def click(self, locator: tuple):
        """Espera que sea clickeable y hace click."""
        self.wait_for_clickable(locator).click()

    def fill(self, locator: tuple, texto: str):
        """Limpia el campo y escribe el texto."""
        elemento = self.wait_for_clickable(locator)
        elemento.clear()
        elemento.send_keys(texto)

    def get_text(self, locator: tuple) -> str:
        """Retorna el texto visible del elemento."""
        return self.wait_for_visible(locator).text

    def get_texts(self, locator: tuple) -> list[str]:
        """Retorna lista de textos de todos los elementos que coincidan."""
        self.wait_for_element(locator)
        elementos = self.driver.find_elements(*locator)
        return [e.text for e in elementos]

    # ──────────────────────────────────────────────────────────
    # MÉTODOS DE NAVEGACIÓN
    # ──────────────────────────────────────────────────────────

    def go_to(self, url: str):
        """Navega a una URL."""
        self.driver.get(url)

    def get_current_url(self) -> str:
        return self.driver.current_url

    def get_title(self) -> str:
        return self.driver.title

    # ──────────────────────────────────────────────────────────
    # SCREENSHOT — útil en after_scenario cuando falla
    # ──────────────────────────────────────────────────────────

    def take_screenshot(self, path: str):
        """Captura pantalla y la guarda en el path dado."""
        self.driver.save_screenshot(path)
