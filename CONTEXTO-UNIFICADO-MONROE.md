# 📘 CONTEXTO UNIFICADO: Monroe Newsletter System

**Última actualización:** Diciembre 16, 2025  
**Estado:** Contexto final - Listo para implementación

---

## 🎯 VISIÓN GENERAL (El Cuadro Completo)

Monroe es un **newsletter local de eventos** con 3 componentes integrados:

```
┌──────────────────────────────────────────────────────────┐
│ monroe-newsletter (TU PC - PRIVADO)                      │
│ ✅ Extrae eventos de webs (main.py)                     │
│ ✅ Dashboard editorial con flujo Kanban                 │
│ ✅ Genera HTML newsletter (preview.html)                │
│ ✅ Historial privado (history.html)                     │
│ 🔐 Requiere autenticación (login obligatorio)           │
└──────────────────┬───────────────────────────────────────┘
                   │ Lee/Escribe
                   ↓
        PostgreSQL (Neon.tech)
                   ↑
                   │ Lee
┌──────────────────┴───────────────────────────────────────┐
│ monroe-backend-api (RENDER - PÚBLICO API)               │
│ ✅ 4 endpoints JSON read-only                           │
│ ✅ Sin dashboard, sin UI                               │
│ ✅ Sin autenticación                                    │
│ ✅ CORS habilitado para Astro                          │
└──────────────────┬───────────────────────────────────────┘
                   │ Envía JSON
                   ↓
        Astro (Frontend Público)
                   │
┌──────────────────┴───────────────────────────────────────┐
│ monroe-web (ASTRO - PÚBLICO)                            │
│ ✅ Home con carrusel de eventos                         │
│ ✅ Página /newsletter (listado de archivos)             │
│ ✅ Página /newsletter/<id> (HTML guardado)              │
│ ✅ SEO optimizado, indexado en Google                   │
└──────────────────────────────────────────────────────────┘
```

---

## 🏗️ ARQUITECTURA TÉCNICA

### monroe-newsletter (Privado - Tu PC)

**Stack:**
- Python 3.13 + Flask
- PostgreSQL 16 (Neon.tech)
- Firecrawl (scraping)
- IA: Mistral/OpenAI/Gemini (configurable)

**Rutas:**
```
/login                    → Autenticación
/editorial-dashboard      → Flujo Kanban (pending → finalizado)
/melocoton               → Preview newsletter (copia HTML)
/history                 → Archivo privado de newsletters
/logout                  → Cierra sesión
```

**Bases de datos:**
```sql
events (
  id, title, description, final_description,
  event_date, category, image_url, link,
  status (pending_revision|aprobado|pendiente_edicion|finalizado),
  is_highlight, group_title
)

newsletters (
  id, subject, content_html,
  is_published, published_at, created_at
)

users (
  id, username, password_hash, created_at
)
```

**Seguridad:**
- ✅ CSRF protection (flask_wtf)
- ✅ Rate limiting: 5/min en login (flask_limiter)
- ✅ Contraseñas hasheadas (werkzeug.security)
- ✅ Cookies seguras: SECURE, HTTPONLY, SAMESITE
- ✅ Session timeout: 1 hora

---

### monroe-backend-api (Público - Render)

**Stack:**
- Python 3.10+ + Flask
- PostgreSQL (Neon.tech - misma BD que monroe-newsletter)
- SQLAlchemy ORM

**Endpoints (READ-ONLY):**

```
GET /api/v1/events/upcoming
  Response: {
    "status": "success",
    "data": [
      {
        "id": 1,
        "title": "Cotton Stakes Classic",
        "date": "2025-09-03",
        "category": "things-to-do",
        "description": "...",
        "image_url": "...",
        "link": "https://..."
      }
    ]
  }

GET /api/v1/newsletters
  Response: {
    "status": "success",
    "total": 52,
    "page": 1,
    "per_page": 10,
    "data": [
      {
        "id": 1,
        "subject": "Monroe This Week: Sep 3-6",
        "published_at": "2025-09-01",
        "url": "/api/v1/newsletters/1"
      }
    ]
  }

GET /api/v1/newsletters/<id>
  Response: {
    "status": "success",
    "data": {
      "id": 1,
      "subject": "Monroe This Week: Sep 3-6",
      "content_html": "<h1>Hey Monroe!...</h1>",
      "published_at": "2025-09-01",
      "created_at": "2025-09-01"
    }
  }

GET /api/v1/stats
  Response: {
    "status": "ok",
    "database": "connected",
    "timestamp": "2025-12-16T03:48:00Z"
  }
```

**Configuración:**
- Acceso desde: https://api.monroe.render.com
- Base de datos: Neon.tech (misma que monroe-newsletter)
- CORS: Habilitado para meetmonroe.us
- Rate limiting: 100 req/min por IP (público)

---

### monroe-web (Público - Astro)

**Stack:**
- Astro Framework
- Tailwind CSS
- Cloudflare Pages

**Páginas:**
```
/                 → Home público (carrusel de eventos)
/events           → Listado de próximos eventos
/newsletter       → Archivo de newsletters publicadas
/newsletter/<id>  → Newsletter específica (HTML)
```

**Llamadas a API:**
```javascript
// Home: carrusel de eventos próximos
const response = await fetch('https://api.monroe.render.com/api/v1/events/upcoming');
const events = await response.json();

// Página /newsletter: listado de newsletters
const response = await fetch('https://api.monroe.render.com/api/v1/newsletters');
const newsletters = await response.json();

// Página /newsletter/<id>: newsletter específica
const response = await fetch(`https://api.monroe.render.com/api/v1/newsletters/${id}`);
const newsletter = await response.json();
// Renderiza: newsletter.data.content_html
```

---

## 🔄 FLUJO COMPLETO: De Editorial a Público

### FASE 1: Editorial (Monroe Newsletter - Tu PC)

```
TÚ:
  1. Abres http://localhost:5000/editorial-dashboard
  2. Arrastra eventos entre columnas (Kanban)
  3. Edita títulos, descripciones
  4. Genera descripciones con IA
  5. Aprueba eventos → Status: "finalizado"
```

### FASE 2: Preview (Monroe Newsletter - Tu PC)

```
TÚ:
  1. Clicas /melocoton (preview)
  2. Ves HTML bonito del newsletter
  3. Clicas "Copy HTML"
  4. HTML copiado al portapapeles
```

### FASE 3: Publicación en Kit (ConvertKit)

```
TÚ:
  1. Abres ConvertKit.com
  2. Nuevo email
  3. Pegas HTML (Ctrl+V)
  4. Añades sponsors, fotos manualmente
  5. Configuras: "Publicar Viernes 8am"
  6. Publicas a suscriptores
```

### FASE 4: Guardar en BD (Monroe Newsletter - Tu PC)

```
TÚ:
  1. Vuelves a /melocoton
  2. Clicas "Guardar en Historial"
  
APP:
  INSERT INTO newsletters (subject, content_html, is_published, published_at)
  → Se guarda en PostgreSQL
  → Aparece en /history (privado)
```

### FASE 5: Exponer vía API (Monroe Backend API)

```
monroe-backend-api:
  SELECT newsletters WHERE is_published=true
  → Expone vía GET /api/v1/newsletters
  → Expone vía GET /api/v1/newsletters/<id>
```

### FASE 6: Mostrar en Web Pública (Astro)

```
Usuario:
  1. Entra a https://meetmonroe.us
  2. Home carga eventos (GET /api/v1/events/upcoming)
  3. Clica "Newsletter Archive"
  4. Ve listado (GET /api/v1/newsletters)
  5. Clica newsletter #5
  6. Ve HTML completo (GET /api/v1/newsletters/5)
  7. Google lo indexa automáticamente
```

---

## 📊 DIFERENCIAS CLAVE

| Aspecto | monroe-newsletter | monroe-backend-api | monroe-web |
|---------|-------------------|--------------------|-----------|
| **Acceso** | 🔐 Privado (login) | 🌍 Público (API) | 🌍 Público (web) |
| **Autenticación** | ✅ User + Pass | ❌ Ninguna | ❌ Ninguna |
| **Dashboard** | ✅ Editorial UI | ❌ Solo JSON | ✅ Web bonita |
| **Lee/Escribe** | ✅ Lee/Escribe | ✅ Solo Lee | ❌ No accede DB |
| **URL** | http://localhost:5000 | https://api.monroe.render.com | https://meetmonroe.us |

---

## 🔐 SEGURIDAD

### monroe-newsletter (Privado)

**Checklist (ver AUDITORIA-SEGURIDAD-LOGIN.md):**
- [ ] CSRF Protection (flask_wtf)
- [ ] Rate Limiting 5/min (flask_limiter)
- [ ] Error messages genéricos ("Credenciales inválidas")
- [ ] Contraseñas hasheadas (werkzeug.security)
- [ ] Cookies seguras (SECURE, HTTPONLY, SAMESITE)
- [ ] Session timeout 1 hora

### monroe-backend-api (Público)

**Security:**
- ✅ READ-ONLY (sin CREATE, UPDATE, DELETE)
- ✅ Sin autenticación requerida (datos públicos)
- ✅ CORS controlado (solo meetmonroe.us)
- ✅ Rate limiting público (100 req/min)
- ✅ Inputs validados
- ✅ SQL injection prevenido (SQLAlchemy ORM)

---

## 🗄️ BASE DE DATOS (PostgreSQL - Neon.tech)

**Una sola BD compartida por ambos proyectos:**

```sql
-- TABLA: events (escrita por monroe-newsletter, leída por monroe-backend-api)
CREATE TABLE events (
  id SERIAL PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  final_description TEXT,
  event_date TIMESTAMP,
  category VARCHAR(50),
  image_url VARCHAR(500),
  link VARCHAR(500),
  status ENUM('pending_revision', 'aprobado_para_generacion', 'pendiente_edicion_final', 'finalizado'),
  is_highlight BOOLEAN DEFAULT false,
  group_title VARCHAR(255),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- TABLA: newsletters (escrita por monroe-newsletter, leída por monroe-backend-api)
CREATE TABLE newsletters (
  id SERIAL PRIMARY KEY,
  subject VARCHAR(255) NOT NULL,
  content_html TEXT,
  is_published BOOLEAN DEFAULT false,
  published_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- TABLA: users (para monroe-newsletter auth)
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(80) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 🚀 STACK FINAL

```
FRONTEND PÚBLICO:
  Astro (Cloudflare Pages) → meetmonroe.us
  Llama: GET /api/v1/events/upcoming, /newsletters, /newsletters/<id>

BACKEND EDITORIAL:
  monroe-newsletter (Tu PC o Render) → Privado con login
  Extrae eventos, edita, genera HTML

BACKEND API:
  monroe-backend-api (Render) → API pública JSON
  Read-only, sirve datos a Astro

BASE DE DATOS:
  PostgreSQL (Neon.tech) → Una sola BD central
  Compartida por monroe-newsletter y monroe-backend-api

EMAIL:
  ConvertKit → Kit.com
  Editora publica newsletters desde aquí

NEWSLETTER PÚBLICO:
  meetmonroe.us/newsletter → Indexado en Google
  Mostramos HTML guardado en BD via API
```

---

## 📋 RESUMEN OPERATIVO

**Tarea diaria (TÚ):**
```
1. Lunes: python main.py monroe (extrae eventos)
2. Mar-Jue: /editorial-dashboard (edita eventos)
3. Viernes 7am:
   - /melocoton (preview)
   - Copy HTML
   - Paste en ConvertKit
   - Añade sponsors + fotos
   - Publica a suscriptores
4. Viernes 7:30am:
   - /melocoton "Guardar en Historial"
   - Newsletter aparece en meetmonroe.us/newsletter
5. Usuarios públicos ven en /newsletter archive
6. Google lo indexa automáticamente
```

**Datos para configuración:**

```
DATABASE_URL = postgresql://user:pass@db.neon.tech/dbname
SECRET_KEY = algo-aleatorio-muy-largo-y-seguro
RENDER_URL = https://api.monroe.render.com
NEON_URL = https://db.neon.tech
```

---

## ⚠️ NOTAS IMPORTANTES

1. **No es automático:** TÚ debes guardar manualmente en BD (o configurar webhook de Kit)
2. **Mismo BD:** monroe-newsletter y monroe-backend-api usan MISMA PostgreSQL
3. **Public API:** monroe-backend-api NO tiene autenticación (datos son públicos)
4. **Private Editorial:** monroe-newsletter requiere login (CRÍTICO auditar seguridad)
5. **SEO:** Los newsletters en /newsletter/<id> son públicos e indexables

---

## 📚 DOCUMENTOS RELACIONADOS

- **BRUJULA-TAREAS.md** → Checklist de ejecución y progreso
- **AUDITORIA-SEGURIDAD-LOGIN.md** → Auditoría de seguridad para monroe-newsletter
