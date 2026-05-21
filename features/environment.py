"""
features/environment.py — Hooks de Behave para Selenium WebDriver.

Ciclo de vida:
  before_all      → leer config de behave.ini
  before_scenario → lanzar Chrome + instanciar Page Objects
  after_scenario  → screenshot si falló + cerrar driver
  after_all       → limpieza final

Diferencia clave vs Playwright (environment.py anterior):
  Playwright: sync_playwright().start() → una instancia global
  Selenium:   webdriver.Chrome() por cada scenario
              (más aislamiento, cada test empieza con browser limpio)

webdriver-manager descarga ChromeDriver automáticamente —
NO hace falta tener chromedriver.exe en el PATH.
"""
import sys
import os
import datetime

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _ROOT)

from selenium import webdriver
from selenium.webdriver.chrome.service  import Service  as ChromeService
from selenium.webdriver.firefox.service import Service  as FirefoxService
from selenium.webdriver.chrome.options  import Options  as ChromeOptions
from selenium.webdriver.firefox.options import Options  as FirefoxOptions
from webdriver_manager.chrome   import ChromeDriverManager
from webdriver_manager.firefox  import GeckoDriverManager

from pages.login_page     import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page      import CartPage
from pages.checkout_page  import CheckoutPage


# ──────────────────────────────────────────────
# BEFORE_ALL
# ──────────────────────────────────────────────

def before_all(context):
    """Lee la configuración de behave.ini una sola vez."""
    ud = context.config.userdata

    context.base_url           = ud.get("base_url", "https://www.saucedemo.com")
    context.headless           = ud.get("headless", "true").lower() == "true"
    context.wait_timeout       = int(ud.get("wait_timeout", 10))
    context.screenshot_on_fail = ud.get("screenshot_on_fail", "true").lower() == "true"
    context.browser_name       = ud.get("browser", "chrome").lower()

    os.makedirs("screenshots", exist_ok=True)
    os.makedirs("reports",     exist_ok=True)

    print(f"\n🚀 Suite iniciada")
    print(f"   Browser  : {context.browser_name}")
    print(f"   Headless : {context.headless}")
    print(f"   Timeout  : {context.wait_timeout}s")
    print(f"   URL      : {context.base_url}")


def after_all(context):
    print("\n✅ Suite finalizada.")


# ──────────────────────────────────────────────
# BEFORE/AFTER FEATURE
# ──────────────────────────────────────────────

def before_feature(context, feature):
    print(f"\n📄 Feature: {feature.name}")


def after_feature(context, feature):
    estado = "✅ PASS" if feature.status == "passed" else "❌ FAIL"
    print(f"   {estado} — {feature.name}")


# ──────────────────────────────────────────────
# BEFORE_SCENARIO — Arrancar el driver
# ──────────────────────────────────────────────

def before_scenario(context, scenario):
    """
    Por cada Scenario:
      1. Construye las opciones del browser (headless, tamaño, etc.)
      2. Descarga y lanza ChromeDriver con webdriver-manager
      3. Instancia todos los Page Objects pasando el driver
    """
    print(f"\n  🔹 Scenario: {scenario.name}")

    driver = _crear_driver(
        nombre   = context.browser_name,
        headless = context.headless,
        timeout  = context.wait_timeout,
    )

    context.driver = driver

    # ── Instanciar Page Objects ───────────────────────────────────────────
    # Cada PO recibe el driver Y el timeout de la config
    # BasePage usa ese timeout para WebDriverWait
    context.login_page     = LoginPage    (driver, context.wait_timeout)
    context.inventory_page = InventoryPage(driver, context.wait_timeout)
    context.cart_page      = CartPage     (driver, context.wait_timeout)
    context.checkout_page  = CheckoutPage (driver, context.wait_timeout)


# ──────────────────────────────────────────────
# AFTER_SCENARIO — Screenshot + cerrar driver
# ──────────────────────────────────────────────

def after_scenario(context, scenario):
    """
    Por cada Scenario:
      1. Screenshot si falló (con nombre descriptivo)
      2. driver.quit() — SIEMPRE, aunque el test pase
    """
    if hasattr(context, "driver") and context.driver:

        if scenario.status == "failed" and context.screenshot_on_fail:
            nombre_limpio = scenario.name.replace(" ", "_").replace("/", "-")[:60]
            timestamp     = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            ruta          = f"screenshots/{nombre_limpio}_{timestamp}.png"
            try:
                context.driver.save_screenshot(ruta)
                print(f"\n  📸 Screenshot: {ruta}")
            except Exception as e:
                print(f"\n  ⚠️  No se pudo capturar screenshot: {e}")

        try:
            context.driver.quit()        # cierra browser + proceso del driver
        except Exception:
            pass

    estado = "✅ PASÓ" if scenario.status == "passed" else "💥 FALLÓ"
    print(f"  {estado}: {scenario.name}")


# ──────────────────────────────────────────────
# HELPER — Crear WebDriver según el browser
# ──────────────────────────────────────────────

def _crear_driver(nombre: str, headless: bool, timeout: int):
    """
    Crea y retorna el WebDriver configurado.
    webdriver-manager descarga el driver automáticamente.

    Soporta: chrome | firefox
    """
    if nombre == "firefox":
        opciones = FirefoxOptions()
        if headless:
            opciones.add_argument("--headless")
        service = FirefoxService(GeckoDriverManager().install())
        driver  = webdriver.Firefox(service=service, options=opciones)

    else:  # chrome (default)
        opciones = ChromeOptions()

        if headless:
            opciones.add_argument("--headless=new")   # nuevo modo headless de Chrome

        # Opciones necesarias para correr en CI (Linux sin GPU)
        opciones.add_argument("--no-sandbox")
        opciones.add_argument("--disable-dev-shm-usage")
        opciones.add_argument("--disable-gpu")
        opciones.add_argument("--window-size=1280,720")

        # Silenciar logs de ChromeDriver
        opciones.add_experimental_option("excludeSwitches", ["enable-logging"])

        service = ChromeService(ChromeDriverManager().install())
        driver  = webdriver.Chrome(service=service, options=opciones)

    # Timeout implícito como red de seguridad (la espera explícita tiene prioridad)
    driver.implicitly_wait(3)
    driver.set_page_load_timeout(timeout * 2)

    return driver
