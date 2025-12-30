# GEMINI.md - Reglas de Desarrollo para monroe-backend-api

## 📜 Reglas de Comunicación

* **Idioma:** Todas tus respuestas, explicaciones y comentarios en el código deben estar en **español**.

---

## 📐 Principios Fundamentales de Código

* **Responsabilidad Única (Single Responsibility):** Cada módulo debe hacer UNA SOLA COSA.
  * **app.py** = Solo Application Factory (crear app, registrar blueprints)
  * **config.py** = Solo configuración (variables, credenciales)
  * **extensions.py** = Solo inicialización de librerías (db, limiter, cors)
  * **models.py** = Solo definiciones ORM (Event, Newsletter)
  * **routes/api_routes.py** = Solo endpoints (rutas GET)
  
  Si un archivo hace 2 cosas, divídelo.

* **Límites de Tamaño Estrictos:**
  * **Archivos:** No deben exceder 300 líneas.
  * **Funciones:** Máximo 40 líneas, idealmente 20-30.
  * **Endpoints:** Cada ruta debe ser corta y legible.

* **Nombres Descriptivos y sin Ambigüedad:** Los nombres de funciones, variables y endpoints deben revelar su intención.
  * ✅ `def get_upcoming_events()`, `DATABASE_URL`, `validate_newsletter_id()`
  * ❌ `def get_data()`, `process()`, `DB_URL`

* **Evita Lógica Compleja en Rutas:** Extrae la lógica a funciones helper.
  * ✅ Ruta llama a función helper
  * ❌ 50 líneas de lógica dentro de la ruta

---

## 🔐 Reglas de Seguridad (CRÍTICO)

* **READ-ONLY Absoluto:** Solo GET. Sin POST, PUT, DELETE, PATCH.
  * ✅ `GET /api/v1/events/upcoming`
  * ❌ `POST /api/v1/events`, `PUT /api/v1/newsletters/1`

* **Sin Autenticación:** Los datos son públicos. No uses `@login_required`.
  * ✅ Cualquiera accede sin credenciales
  * ❌ No pidas usuario + contraseña

* **Error Handling Consistente:** Todos los endpoints retornan mismo formato.
  ```python
  {
    "status": "success|error",
    "data": [...],        # o null si error
    "message": "..."      # si error
  }
  ```

* **Validación de Inputs:** Valida siempre, nunca confíes en el input del usuario.
  ```python
  ✅ if not isinstance(id, int) or id < 1: return error
  ❌ return Newsletter.query.get(id).__dict__
  ```

---

## 📝 Stack y Configuración

* **Framework:** Flask (Application Factory pattern)
* **ORM:** SQLAlchemy (no raw SQL)
* **Base de Datos:** PostgreSQL (Neon.tech)
* **CORS:** Habilitado para localhost:3000 y meetmonroe.us
* **Rate Limiting:** 100 req/min por IP
* **Variables de Entorno:** DATABASE_URL, SECRET_KEY, FLASK_ENV, CORS_ORIGINS

---

## ⚠️ Reglas de Oro (No Negociables)

1. **READ-ONLY:** Si creas POST/PUT/DELETE, falla el proyecto.
2. **Sin Login:** Si usas `@login_required`, falla el proyecto.
3. **Estructura Consistente:** Todos los endpoints responden igual.
4. **Validación:** Todo input se valida antes de usarse.
5. **Sin Lógica en Rutas:** Extrae a funciones helper separadas.
