# language: es
# ──────────────────────────────────────────────────────────────
# Feature: Login en SauceDemo
# Migrado de: features/login.feature (Cucumber/JS)
# Herramienta: Behave (Python)
# App bajo prueba: https://www.saucedemo.com
# ──────────────────────────────────────────────────────────────

Característica: Login en SauceDemo
  Como un cliente de Sauce Demo
  Quiero poder iniciar sesión en la aplicación
  Para acceder al inventario de productos

  # ────────────────────────────────────────
  # CASO 1 — Login exitoso con usuario válido
  # ────────────────────────────────────────
  @Caso_1 @smoke
  Escenario: Validar el inicio de sesión con credenciales válidas
    Dado el usuario está en la página de login
    Cuando ingresa el usuario "standard_user" y la contraseña "secret_sauce"
    Y hace click en el botón Login
    Entonces debe ver la página de inventario

  # ────────────────────────────────────────
  # CASO 2 — Login fallido con credenciales inválidas
  # ────────────────────────────────────────
  @Caso_2 @regression
  Escenario: Validar que el usuario no pueda iniciar sesión con credenciales inválidas
    Dado el usuario está en la página de login
    Cuando ingresa el usuario "usuario_invalido" y la contraseña "clave_incorrecta"
    Y hace click en el botón Login
    Entonces debe ver el mensaje de error "Epic sadface: Username and password do not match any user in this service"

  # ────────────────────────────────────────
  # CASO 3 — Usuario bloqueado
  # ────────────────────────────────────────
  @Caso_3 @regression
  Escenario: Validar que el usuario no pueda iniciar sesión con usuario bloqueado
    Dado el usuario está en la página de login
    Cuando ingresa el usuario "locked_out_user" y la contraseña "secret_sauce"
    Y hace click en el botón Login
    Entonces debe ver el mensaje de error "Epic sadface: Sorry, this user has been locked out."

  # ────────────────────────────────────────
  # CASO 4 — Login con visual_user (rol especial)
  # ────────────────────────────────────────
  @Caso_4 @regression
  Escenario: Validar login con el rol visual_user
    Dado que el usuario se encuentra en la página de login
    Y se valida el texto de la página de login
    Cuando el usuario ingresa su usuario "visual_user" y su contraseña "secret_sauce"
    Y hace click en el botón Login
    Entonces el usuario debe ver la página de inventario con el header visible
