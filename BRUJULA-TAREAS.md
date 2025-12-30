# 🧭 BRÚJULA DE TAREAS: Monroe Newsletter Implementation

**Estado General:** 🟡 EN PROGRESO  
**Última actualización:** Diciembre 16, 2025  
**Completitud:** 0% → [Inicio]

---

## 📋 FASE 0: PREPARACIÓN (Hoy)

- [ ] **0.1** Borra contenido de `D:\Proyectos\monroe-backend-api`
  - `rm -r D:\Proyectos\monroe-backend-api\*`
  - Mantén solo `.gitignore`

- [ ] **0.2** Copia documentos a monroe-backend-api
  - [ ] CONTEXTO-UNIFICADO-MONROE.md
  - [ ] BRUJULA-TAREAS.md (este)
  - [ ] AUDITORIA-SEGURIDAD-LOGIN.md

- [ ] **0.3** Verifica estructura
  ```
  D:\Proyectos\monroe-backend-api\
  ├── CONTEXTO-UNIFICADO-MONROE.md ✅
  ├── BRUJULA-TAREAS.md ✅
  ├── AUDITORIA-SEGURIDAD-LOGIN.md ✅
  └── (todo lo demás borramos)
  ```

**Tiempo estimado:** 5 minutos  
**Estado:** ⏳ Pendiente

---

## 🚀 FASE 1: GENERAR monroe-backend-api (Hoy)

### 1.1 Abre Gemini CLI

**Ubicación:** `D:\Proyectos\monroe-backend-api`

```powershell
cd D:\Proyectos\monroe-backend-api
gemini-cli  # O tu comando equivalente
```

- [ ] Gemini CLI abierto en monroe-backend-api

### 1.2 Copia contexto en Gemini CLI

```text
He leído CONTEXTO-UNIFICADO-MONROE.md completamente.

Necesito que generes monroe-backend-api DESDE CERO con:

1. app.py (Application Factory - Flask)
2. config.py (Configuración - variables de entorno)
3. extensions.py (Inicialización de SQLAlchemy, etc)
4. models.py (ORM - Event y Newsletter models)
5. routes/
   ├── __init__.py
   └── api_routes.py (4 endpoints JSON)
6. requirements.txt
7. .env.example

ENDPOINTS requeridos:
- GET /api/v1/events/upcoming → Próximos 5 eventos (status='finalizado')
- GET /api/v1/newsletters → Listado paginado (is_published=true)
- GET /api/v1/newsletters/<id> → Newsletter específico
- GET /api/v1/stats → Health check

REQUISITOS:
✅ Framework: Flask (sin blueprints complicados)
✅ ORM: SQLAlchemy (conecta a Neon.tech PostgreSQL)
✅ READ-ONLY (sin POST, PUT, DELETE)
✅ Sin autenticación
✅ CORS habilitado (origin: meetmonroe.us)
✅ Rate limiting: 100 req/min por IP
✅ Inputs validados
✅ Error handling limpio
✅ HTTPS ready (Render)

¿Puedes generarlo completo?
```

- [ ] Gemini genera código

### 1.3 Copia código a archivos

**Gemini generará:**
- app.py
- config.py
- extensions.py
- models.py
- routes/api_routes.py
- requirements.txt
- .env.example

**TÚ HACES:**
```powershell
# Crea estructura
mkdir routes
mkdir __pycache__

# Copia cada archivo que Gemini generó
# app.py → D:\Proyectos\monroe-backend-api\app.py
# config.py → D:\Proyectos\monroe-backend-api\config.py
# ... etc
```

- [ ] Código copiado correctamente

### 1.4 Instala dependencias localmente

```powershell
cd D:\Proyectos\monroe-backend-api
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

- [ ] venv creado
- [ ] Dependencias instaladas

### 1.5 Configura .env local

```powershell
copy .env.example .env
notepad .env

# Edita:
DATABASE_URL=postgresql://user:pass@db.neon.tech/dbname
SECRET_KEY=algo-aleatorio-muy-largo
FLASK_ENV=development
CORS_ORIGINS=http://localhost:3000,https://meetmonroe.us
```

- [ ] .env configurado con datos de Neon.tech

### 1.6 Prueba localmente

```powershell
# Terminal 1:
flask run

# Terminal 2:
curl http://localhost:5000/api/v1/stats
# Debe responder: {"status":"ok","database":"connected"}
```

- [ ] API arranca sin errores
- [ ] GET /api/v1/stats responde correctamente
- [ ] GET /api/v1/events/upcoming devuelve JSON
- [ ] GET /api/v1/newsletters devuelve JSON

**Tiempo estimado:** 45 minutos  
**Estado:** ⏳ Pendiente  
**Completitud:** 0% → 20%

---

## 🔐 FASE 2: AUDITORÍA DE SEGURIDAD (monroe-newsletter)

### 2.1 Lee AUDITORIA-SEGURIDAD-LOGIN.md

- [ ] Leído completamente

### 2.2 Abre Gemini CLI en monroe-newsletter

```powershell
cd "D:\Proyectos cursor\Monroe newsletter"
gemini-cli
```

- [ ] Gemini CLI abierto en monroe-newsletter

### 2.3 Audita con Gemini

```text
Leo AUDITORIA-SEGURIDAD-LOGIN.md

Necesito que audites mi app/app.py:

1. ¿Tiene CSRF protection? (flask_wtf)
2. ¿Tiene rate limiting 5/min? (flask_limiter)
3. ¿Error messages genéricos? ("Credenciales inválidas")
4. ¿Contraseñas hasheadas? (werkzeug.security)
5. ¿Cookies seguras? (SECURE, HTTPONLY, SAMESITE)
6. ¿Session timeout? (PERMANENT_SESSION_LIFETIME)

Mi app/app.py:
[PEGA CONTENIDO COMPLETO]

Mi config.py:
[PEGA CONTENIDO COMPLETO]

¿Qué me falta? ¿Cómo lo arreglo?
```

- [ ] Gemini audita código

### 2.4 Arregla lo que falte

**Gemini te dirá qué añadir.**

Ejemplos:
```python
# Si falta CSRF:
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(app)

# Si falta rate limiting:
from flask_limiter import Limiter
limiter = Limiter(app, key_func=get_remote_address)
@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    ...

# Si falta cookies seguras (config.py):
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Strict'
PERMANENT_SESSION_LIFETIME = 3600
```

- [ ] CSRF protection añadido (si falta)
- [ ] Rate limiting añadido (si falta)
- [ ] Error messages genéricos (si falta)
- [ ] Contraseñas hasheadas verificadas
- [ ] Cookies seguras configuradas
- [ ] Session timeout configurado

### 2.5 Verifica login local

```powershell
cd "D:\Proyectos cursor\Monroe newsletter"
flask run

# Prueba en http://localhost:5000/login
# Intenta login con credenciales falsas
# Debe decir: "Credenciales inválidas" (genérico)
# Intenta 6 veces en 1 minuto
# Debe bloquear: "Too many attempts"
```

- [ ] Login funciona correctamente
- [ ] Rate limiting funciona (5/min)
- [ ] Mensajes son genéricos

**Tiempo estimado:** 30 minutos  
**Estado:** ⏳ Pendiente  
**Completitud:** 20% → 50%

---

## 🔗 FASE 3: CONECTAR BASES DE DATOS

### 3.1 Verifica conexión a Neon.tech

**En monroe-backend-api:**

```powershell
# Prueba conexión
python -c "
from config import DATABASE_URL
import psycopg2
conn = psycopg2.connect(DATABASE_URL)
print('✅ Conexión exitosa a Neon.tech')
conn.close()
"
```

- [ ] Conexión a Neon.tech verificada

### 3.2 Verifica tablas existen

```powershell
# En psql o similar:
psql $DATABASE_URL

# Comando:
\dt

# Debe mostrar:
# - events
# - newsletters
# - users
```

- [ ] Tabla `events` existe
- [ ] Tabla `newsletters` existe
- [ ] Tabla `users` existe

### 3.3 Verifica datos de prueba

```powershell
# Query:
SELECT COUNT(*) FROM events WHERE status='finalizado';
SELECT COUNT(*) FROM newsletters WHERE is_published=true;

# Debe retornar números (ej: 5 eventos finalizados, 2 newsletters)
```

- [ ] Datos existen en DB

**Tiempo estimado:** 15 minutos  
**Estado:** ⏳ Pendiente  
**Completitud:** 50% → 65%

---

## ✅ FASE 4: TESTING COMPLETO (Local)

### 4.1 Prueba todos los endpoints

```powershell
# En otra terminal mientras flask run está activo:

# Test 1: GET /api/v1/stats
curl http://localhost:5000/api/v1/stats
# Response: {"status":"ok","database":"connected"}

# Test 2: GET /api/v1/events/upcoming
curl http://localhost:5000/api/v1/events/upcoming
# Response: {"status":"success","data":[{...}]}

# Test 3: GET /api/v1/newsletters
curl http://localhost:5000/api/v1/newsletters
# Response: {"status":"success","total":X,"page":1,"data":[...]}

# Test 4: GET /api/v1/newsletters/1
curl http://localhost:5000/api/v1/newsletters/1
# Response: {"status":"success","data":{...}}
```

- [ ] GET /api/v1/stats ✅
- [ ] GET /api/v1/events/upcoming ✅
- [ ] GET /api/v1/newsletters ✅
- [ ] GET /api/v1/newsletters/1 ✅

### 4.2 Prueba CORS

```powershell
# Desde navegador:
# Abre Developer Tools (F12)
# Console:

fetch('http://localhost:5000/api/v1/stats')
  .then(r => r.json())
  .then(data => console.log(data))

# Debe funcionar sin errores CORS
```

- [ ] CORS funciona

### 4.3 Prueba rate limiting

```powershell
# Haz 101 requests rapidísimo:
for ($i=1; $i -le 101; $i++) {
    curl http://localhost:5000/api/v1/stats
}

# Después del 100 debe retornar: 429 Too Many Requests
```

- [ ] Rate limiting funciona

**Tiempo estimado:** 20 minutos  
**Estado:** ⏳ Pendiente  
**Completitud:** 65% → 80%

---

## 🚀 FASE 5: DEPLOY A RENDER

### 5.1 Prepara repo Git

```powershell
cd D:\Proyectos\monroe-backend-api

# Si no tiene git:
git init
git add .
git commit -m "Initial commit: monroe-backend-api"

# Si ya tiene:
git add .
git commit -m "Clean rebuild with context"
git push origin main
```

- [ ] Repo actualizado en GitHub

### 5.2 Configura Render

1. Ve a https://render.com
2. Nuevo "Web Service"
3. Conecta repo `monroe-backend-api`
4. Configuración:
   ```
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn app:app
   ```
5. Environment Variables:
   ```
   DATABASE_URL = (de Neon.tech)
   SECRET_KEY = (genera uno aleatorio)
   FLASK_ENV = production
   CORS_ORIGINS = https://meetmonroe.us,https://www.meetmonroe.us
   ```

- [ ] Render conectado
- [ ] Build command configurado
- [ ] Start command configurado
- [ ] Environment variables añadidas
- [ ] Deploy inicia

### 5.3 Espera deploy (5-10 min)

```
Status: Deploying... → Live ✅
```

- [ ] Deploy completado exitosamente

### 5.4 Prueba endpoint en producción

```powershell
curl https://api.monroe.render.com/api/v1/stats
# Debe responder con status: ok
```

- [ ] Endpoint /api/v1/stats responde
- [ ] URL es: https://api.monroe.render.com

**Tiempo estimado:** 20 minutos  
**Estado:** ⏳ Pendiente  
**Completitud:** 80% → 95%

---

## 🎯 FASE 6: CONECTAR ASTRO (monroe-web)

### 6.1 Actualiza Astro para usar API

**En `src/pages/events.astro` (o similar):**

```javascript
// Antes (datos hardcoded):
const events = [...]

// Después (desde API):
const response = await fetch('https://api.monroe.render.com/api/v1/events/upcoming')
const data = await response.json()
const events = data.data || []
```

- [ ] Página /events llama API
- [ ] Página /newsletter llama API /newsletters
- [ ] Página /newsletter/<id> llama API /newsletters/<id>

### 6.2 Prueba Astro localmente

```powershell
cd D:\Proyectos\monroe-web
npm run dev

# Abre http://localhost:3000
# Verifica que los eventos cargan desde la API
```

- [ ] Carrusel de eventos muestra datos de API
- [ ] Página /newsletter lista newsletters
- [ ] Página /newsletter/1 muestra HTML

### 6.3 Deploy Astro a Cloudflare Pages

```powershell
# Si no está deployado:
npm run build
# Sube build/ a Cloudflare Pages
```

- [ ] Astro deployado
- [ ] URL: https://meetmonroe.us

**Tiempo estimado:** 15 minutos  
**Estado:** ⏳ Pendiente  
**Completitud:** 95% → 100%

---

## ✨ FASE 7: VALIDACIÓN FINAL

- [ ] **7.1** Editora en monroe-newsletter
  - [ ] Editorial dashboard funciona
  - [ ] Preview genera HTML
  - [ ] Copy HTML funciona
  - [ ] Guardar en BD funciona

- [ ] **7.2** Publica en Kit
  - [ ] Newsletter publicada
  - [ ] Se ve en ConvertKit

- [ ] **7.3** Guarda en BD
  - [ ] Click "Guardar" en /melocoton
  - [ ] Aparece en /history privado

- [ ] **7.4** Verifica API pública
  - [ ] GET /api/v1/newsletters retorna la newsletter
  - [ ] GET /api/v1/newsletters/X muestra HTML

- [ ] **7.5** Verifica web pública
  - [ ] https://meetmonroe.us/newsletter muestra listado
  - [ ] https://meetmonroe.us/newsletter/1 muestra HTML
  - [ ] Google puede indexarlo (sin login)

- [ ] **7.6** Prueba desde otro navegador
  - [ ] Sin estar logueado en monroe-newsletter
  - [ ] Puede ver /newsletter y /newsletter/<id>
  - [ ] No puede ver /history (es privado)

**Tiempo estimado:** 10 minutos  
**Estado:** ⏳ Pendiente  
**Completitud:** 100% ✅

---

## 📊 RESUMEN DE TIEMPO

| Fase | Tiempo | Status |
|------|--------|--------|
| 0: Preparación | 5 min | ⏳ |
| 1: Generar API | 45 min | ⏳ |
| 2: Auditar seguridad | 30 min | ⏳ |
| 3: Conectar BD | 15 min | ⏳ |
| 4: Testing | 20 min | ⏳ |
| 5: Deploy Render | 20 min | ⏳ |
| 6: Conectar Astro | 15 min | ⏳ |
| 7: Validación final | 10 min | ⏳ |
| **TOTAL** | **~3.5 horas** | ⏳ |

---

## 📝 NOTAS

- **No saltes fases:** Cada una depende de la anterior
- **Guarda evidencia:** Captura de pantallas de cada paso ✅
- **Documenta errores:** Si algo falla, guarda el error y cuéntamelo
- **Usa este documento:** Actualiza cada ☑️ mientras avanzas

---

## 🆘 SOPORTE

Si algo falla:
1. Lee el error completamente
2. Busca en qué FASE estabas
3. Vuelve a ese paso
4. Si no sabes, cuéntamelo CON EL ERROR EXACTO

**Estoy aquí para cada paso.** 💪
