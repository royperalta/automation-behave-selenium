"""
features/steps/compra_steps.py
Steps del flujo de compra — idénticos en estructura a la versión Playwright.
La diferencia está encapsulada en BasePage (WebDriverWait vs auto-wait).
"""
from behave import when, then


# ──────────────────────────────────────────────
# WHEN — Inventario
# ──────────────────────────────────────────────

@when('agrega el producto "{nombre_producto}" al carrito')
def step_agregar_producto(context, nombre_producto):
    context.inventory_page.agregar_producto_al_carrito(nombre_producto)


@when('hace click en el ícono del carrito')
def step_click_carrito(context):
    context.inventory_page.ir_al_carrito()


# ──────────────────────────────────────────────
# WHEN — Cart
# ──────────────────────────────────────────────

@when('hace click en Checkout')
def step_click_checkout(context):
    context.cart_page.click_checkout()


# ──────────────────────────────────────────────
# WHEN — Checkout
# ──────────────────────────────────────────────

@when('completa los datos con nombre "{nombre}", apellido "{apellido}" y código postal "{codigo}"')
def step_completar_datos(context, nombre, apellido, codigo):
    context.checkout_page.completar_datos_personales(nombre, apellido, codigo)


@when('hace click en Continue')
def step_click_continue(context):
    context.checkout_page.click_continue()


@when('hace click en Finish')
def step_click_finish(context):
    context.checkout_page.click_finish()


# ──────────────────────────────────────────────
# THEN
# ──────────────────────────────────────────────

@then('el carrito debe mostrar "{cantidad}" producto')
def step_cantidad_carrito(context, cantidad):
    cantidad_actual = context.inventory_page.obtener_cantidad_carrito()
    assert cantidad_actual == cantidad, \
        f"Carrito esperado: '{cantidad}', obtenido: '{cantidad_actual}'"


@then('debe ver el producto "{nombre_producto}" en el carrito')
def step_ver_producto_carrito(context, nombre_producto):
    productos = context.cart_page.obtener_nombres_productos()
    assert nombre_producto in productos, \
        f"'{nombre_producto}' no encontrado en carrito. Productos: {productos}"


@then('debe ver el mensaje de confirmación "{mensaje_esperado}"')
def step_mensaje_confirmacion(context, mensaje_esperado):
    mensaje_actual = context.checkout_page.obtener_mensaje_confirmacion()
    assert mensaje_esperado in mensaje_actual, \
        f"Confirmación esperada: '{mensaje_esperado}'\nObtenida: '{mensaje_actual}'"
