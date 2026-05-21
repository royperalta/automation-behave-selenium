# language: es
# ──────────────────────────────────────────────────────────────
# Feature: Proceso de Compra en SauceDemo
# Migrado de: features/compra.feature (Cucumber/JS)
#
# NOTA sobre Esquema del escenario:
#   El original usaba "Esquema del escenario" sin tabla Examples,
#   lo cual es un error en el proyecto JS (un Outline sin datos
#   se ejecuta solo una vez). En Behave se mantiene igual para
#   fidelidad, pero se documenta el comportamiento correcto.
# ──────────────────────────────────────────────────────────────

Característica: Proceso de compra en SauceDemo
  Como cliente de SauceDemo
  Quiero agregar productos al carrito y completar el proceso de compra
  Para adquirir los productos que necesito

  # ── Antecedentes: equivalente de Background en inglés ──────
  # Se ejecuta antes de cada Escenario (login previo)
  Antecedentes:
    Dado el usuario está en la página de login
    Cuando ingresa el usuario "standard_user" y la contraseña "secret_sauce"
    Y hace click en el botón Login
    Entonces debe ver la página de inventario

  # ────────────────────────────────────────
  # CASO 1 — Agregar producto al carrito
  # ────────────────────────────────────────
  @Caso_1 @smoke
  Escenario: Validar que el usuario puede agregar un producto al carrito desde la página de productos
    Cuando agrega el producto "Sauce Labs Backpack" al carrito
    Entonces el carrito debe mostrar "1" producto

  # ────────────────────────────────────────
  # CASO 2 — Ver productos en el carrito
  # ────────────────────────────────────────
  @Caso_2 @regression
  Escenario: Validar que el usuario puede ver los productos agregados en el carrito de compras
    Cuando agrega el producto "Sauce Labs Backpack" al carrito
    Y hace click en el ícono del carrito
    Entonces debe ver el producto "Sauce Labs Backpack" en el carrito

  # ────────────────────────────────────────
  # CASO 3 — Flujo completo de compra E2E
  # ────────────────────────────────────────
  @Caso_3 @regression @e2e
  Escenario: Validar que el usuario puede completar el proceso de compra hasta la confirmación
    Cuando agrega el producto "Sauce Labs Backpack" al carrito
    Y hace click en el ícono del carrito
    Y hace click en Checkout
    Y completa los datos con nombre "Roy", apellido "Peralta Barboza" y código postal "06002"
    Y hace click en Continue
    Y hace click en Finish
    Entonces debe ver el mensaje de confirmación "Thank you for your order!"

  # ────────────────────────────────────────
  # EXTRA — Esquema del escenario con tabla (parametrización real)
  # Demuestra el uso correcto de Esquema del escenario en Behave
  # ────────────────────────────────────────
  @Caso_4 @regression
  Esquema del escenario: Validar que se pueden agregar diferentes productos al carrito
    Cuando agrega el producto "<producto>" al carrito
    Entonces el carrito debe mostrar "1" producto

    Ejemplos:
      | producto                  |
      | Sauce Labs Backpack       |
      | Sauce Labs Bike Light     |
      | Sauce Labs Bolt T-Shirt   |
