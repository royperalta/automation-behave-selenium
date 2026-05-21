"""
features/steps/login_steps.py

Comparación directa de los 3 frameworks:

  Playwright/JS (original):          Playwright/Python:         Selenium/Python (este):
  ─────────────────────────────────────────────────────────────────────────────────────
  await this.loginPage.abrirPagina() context.login_page         context.login_page
                                     .abrir_pagina()             .abrir_pagina()

  expect(this.page).toHaveURL(...)   expect(context.page)       context.login_page
                                     .to_have_url(re.compile)    .wait_for_url_contains
                                                                  ("inventory.html")

  await this.loginPage               context.login_page          context.login_page
    .obtenerMensajeError()            .obtener_mensaje_error()    .obtener_mensaje_error()

El código de los steps es casi idéntico entre Playwright/Python y Selenium/Python.
La diferencia está DENTRO de los Page Objects (BasePage con WebDriverWait).
"""
import re
from behave import given, when, then


# ──────────────────────────────────────────────
# GIVEN
# ──────────────────────────────────────────────

@given('el usuario está en la página de login')
def step_abrir_login(context):
    context.login_page.abrir_pagina()


@given('que el usuario se encuentra en la página de login')
def step_abrir_login_alt(context):
    context.login_page.abrir_pagina()


@given('se valida el texto de la página de login')
def step_validar_texto_login(context):
    context.login_page.validar_texto_login()


# ──────────────────────────────────────────────
# WHEN
# ──────────────────────────────────────────────

@when('ingresa el usuario "{usuario}" y la contraseña "{contrasena}"')
def step_ingresar_credenciales(context, usuario, contrasena):
    context.login_page.ingresar_credenciales(usuario, contrasena)


@when('el usuario ingresa su usuario "{usuario}" y su contraseña "{contrasena}"')
def step_ingresar_credenciales_alt(context, usuario, contrasena):
    context.login_page.ingresar_credenciales(usuario, contrasena)


@when('hace click en el botón Login')
def step_click_login(context):
    context.login_page.click_login()


# ──────────────────────────────────────────────
# THEN
# ──────────────────────────────────────────────

@then('debe ver la página de inventario')
def step_ver_inventario(context):
    """
    Selenium no tiene to_have_url() automático.
    Usamos wait_for_url_contains() de BasePage
    que internamente usa: WebDriverWait + EC.url_contains()
    """
    context.login_page.wait_for_url_contains("inventory.html")
    titulo = context.inventory_page.obtener_titulo_app()
    assert titulo == "Swag Labs", \
        f"Título esperado 'Swag Labs', obtenido '{titulo}'"


@then('debe ver el mensaje de error "{mensaje_esperado}"')
def step_ver_error(context, mensaje_esperado):
    mensaje_actual = context.login_page.obtener_mensaje_error()
    assert mensaje_esperado in mensaje_actual, \
        f"Error esperado: '{mensaje_esperado}'\nError obtenido: '{mensaje_actual}'"


@then('el usuario debe ver la página de inventario con el header visible')
def step_ver_header_inventario(context):
    context.login_page.obtener_header()
