# Local Market - Aplicación Flask de Marketplace

Plataforma de marketplace que conecta clientes con emprendedores. Incluye carrito de compras, gestión de órdenes, facturas PDF y reportes.

## Tabla de Contenidos

- [Configuración Local](#configuración-local)
- [Despliegue en Render](#despliegue-en-render)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Variables de Entorno](#variables-de-entorno)
- [Troubleshooting](#troubleshooting)

## Configuración Local

### 1. Crear y Activar el Entorno Virtual

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate.bat

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto (copia desde `.env.example`):

```bash
# Contenido ejemplo de .env
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=tu_clave_secreta_aqui
DATABASE_URL=mysql+pymysql://root:@localhost/local_market
```

Para generar una `SECRET_KEY` segura:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 4. Crear la Base de Datos (MySQL Local)

```bash
# MySQL CLI
CREATE DATABASE IF NOT EXISTS local_market;
USE local_market;
```

### 5. Ejecutar Migraciones

```bash
# Inicializar migraciones (solo primera vez)
flask db init

# Crear migraciones
flask db migrate -m "Initial schema"

# Aplicar migraciones
flask db upgrade
```

### 6. Insertar Datos de Prueba (Opcional)

```bash
python create_tables.py
python inyectar_productos.py
python inyectar_pedidos.py
```

### 7. Ejecutar el Servidor Local

```bash
python run.py
```

La aplicación estará disponible en `http://127.0.0.1:5000`

---

## Despliegue en Render

### Requisitos Previos

1. **Cuenta en Render.com** - Regístrate en https://render.com
2. **Repositorio en GitHub** - Sube el código a GitHub
3. **Python 3.10+** - La versión se especifica en `runtime.txt`

### Paso 1: Preparar el Repositorio para GitHub

```bash
# Inicializar git (si no lo has hecho)
git init

# Agregar archivos
git add .

# Hacer commit
git commit -m "Initial commit: Local Market app ready for deployment"

# Agregar remote
git remote add origin https://github.com/TU_USUARIO/local-market.git

# Push a main/master
git branch -M main
git push -u origin main
```

**IMPORTANTE**: Los siguientes archivos ya están preparados en el repositorio:
- `Procfile` - Configuración para ejecutar con Gunicorn
- `runtime.txt` - Versión de Python (3.10.13)
- `requirements.txt` - Todas las dependencias incluidas
- `build.sh` - Script de construcción

### Paso 2: Crear Base de Datos PostgreSQL en Render

1. Ve a https://dashboard.render.com
2. Click en "New +" y selecciona "PostgreSQL"
3. Configura:
   - **Name**: `local-market-db`
   - **Database**: `local_market`
   - **User**: `postgres` (por defecto)
   - **Region**: Elige la más cercana
   - **Plan**: Free tier
4. Click "Create Database"
5. Espera a que se provee (2-3 minutos)
6. Copia la **Internal Database URL** (formato: `postgresql://user:password@host:port/database`)

### Paso 3: Crear Servicio Web en Render

1. En el Dashboard, click "New +" → "Web Service"
2. Selecciona "Deploy an existing repository"
3. Conecta tu repositorio de GitHub (autoriza Render si es necesario)
4. Configuración:
   - **Name**: `local-market` (o tu nombre preferido)
   - **Runtime**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn -w 4 -b 0.0.0.0:$PORT --timeout 120 run:app`
   - **Plan**: Free tier
5. Click "Create Web Service"

### Paso 4: Configurar Variables de Entorno

En el Dashboard del servicio web que acabas de crear:

1. Ve a la pestaña **Environment**
2. Haz click en "Add Environment Variable"
3. Agrega las siguientes variables:

| Variable | Valor | Descripción |
|----------|-------|-------------|
| `FLASK_APP` | `run.py` | Entrada de la aplicación |
| `FLASK_ENV` | `production` | Modo producción |
| `SECRET_KEY` | [GENERAR] | Ver comando abajo |
| `DATABASE_URL` | [DEL PASO 2] | URL de PostgreSQL de Render |
| `JWT_SECRET_KEY` | [GENERAR] | Ver comando abajo |

**Para generar SECRET_KEY y JWT_SECRET_KEY** (ejecuta localmente):
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

**Nota**: Copia la URL de PostgreSQL (Internal Database URL del paso anterior) en la variable `DATABASE_URL`.

### Paso 5: Aplicar Migraciones (Automático)

El Procfile incluye:
```
release: flask db upgrade
```

Esto ejecutará automáticamente las migraciones cuando se desplegue.

**Para verificar que las migraciones corrieron**:
1. En el Dashboard de Render, ve a la pestaña **Logs**
2. Busca líneas que digan "alembic - Running upgrade" o "Done"

### Paso 6: Acceder a la Aplicación

Una vez que el despliegue termine (indicará "Deployed"), la aplicación estará en:
```
https://local-market.onrender.com
```

O la URL que Render te proporcione.

### Paso 7: Inyectar Datos de Prueba (Opcional)

Para inyectar productos y datos de prueba:

1. **Vía CLI en Render** (Shell):
   - En el Dashboard, ve a la pestaña **Shell**
   - Ejecuta:
   ```bash
   python create_tables.py
   python inyectar_productos.py
   ```

2. **O crea un script** y agrégalo al build.sh (si lo deseas automático).

---

## Estructura del Proyecto

```
local_market/
├── app/
│   ├── __init__.py                 # Factory pattern para crear app
│   ├── extensions.py               # SQLAlchemy, LoginManager
│   ├── models/                     # Modelos ORM
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── order.py
│   │   ├── category.py
│   │   └── ...
│   ├── routes/                     # Blueprints de rutas
│   │   ├── auth.py
│   │   ├── client.py
│   │   ├── entrepreneur.py
│   │   ├── admin.py
│   │   └── api.py
│   ├── services/                   # Lógica de negocio
│   │   ├── auth_service.py
│   │   ├── product_service.py
│   │   ├── pdf_service.py
│   │   ├── report_service.py
│   │   └── ...
│   ├── static/                     # Archivos estáticos (CSS, JS, imágenes)
│   └── templates/                  # Templates HTML
├── migrations/                     # Migraciones con Alembic
├── config.py                       # Configuración de la aplicación
├── run.py                          # Entry point
├── requirements.txt                # Dependencias Python
├── Procfile                        # Configuración para Render
├── runtime.txt                     # Versión de Python
├── build.sh                        # Script de construcción
├── .env.example                    # Variables de entorno (ejemplo)
├── .gitignore                      # Archivos a ignorar en git
└── README.md                       # Este archivo
```

## Variables de Entorno

### Desarrollo (`.env`)
```bash
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=dev-secret-key-change-in-production
DATABASE_URL=mysql+pymysql://root:@localhost/local_market
DEBUG=True
```

### Producción (Render Dashboard)
```bash
FLASK_APP=run.py
FLASK_ENV=production
SECRET_KEY=<generated-secret-key>
DATABASE_URL=postgresql://user:pass@host:port/database
JWT_SECRET_KEY=<generated-jwt-key>
DEBUG=False
```

## Archivos PDFs en Producción

Los PDFs de facturas (`static/invoices/`) y reportes (`static/reports/`) se generan dinámicamente:

### Comportamiento Actual
- Se generan en memoria y se envían directamente al usuario (descarga)
- **Ventaja**: No requiere almacenamiento persistente
- **Comportamiento**: Cada vez que se genera, es temporal

### Si necesitas Persistencia (Futuro)
Considera usar **AWS S3** o **Google Cloud Storage**:
1. Instala `boto3` para AWS S3
2. Modifica `pdf_service.py` para subir a S3
3. Genera URLs públicas para descargas

---

## Troubleshooting

### Error: "ModuleNotFoundError: No module named 'psycopg2'"
**Solución**: `psycopg2-binary` debe estar en `requirements.txt` y instalarse automáticamente.

### Error: "DATABASE_URL is not set"
**Solución**: Asegúrate de que en Render, en Environment Variables, está configurado `DATABASE_URL` con la URL de PostgreSQL.

### Error: "relation does not exist"
**Solución**: Las migraciones no se ejecutaron. Verifica los logs en Render (pestaña Logs) y busca errores de migraciones.

### La aplicación se reinicia constantemente
**Solución**: Revisa los logs. Puede ser por:
- Error de conexión a base de datos
- Variable de entorno faltante
- Error en el código

### Los archivos estáticos no se cargan (CSS, JS)
**Solución**: Asegúrate de que `static/` esté en el repositorio:
```bash
git add app/static/
git commit -m "Add static files"
git push
```

---

## Notas de Seguridad

- ✅ Las cookies de sesión son seguras (HTTPS only)
- ✅ `SECRET_KEY` debe ser única y fuerte (generada con `secrets`)
- ✅ `DEBUG=False` en producción
- ✅ CSRF protección habilitada

---

## Próximos Pasos

1. ✅ Probar la aplicación localmente
2. ✅ Subir a GitHub
3. ✅ Crear BD PostgreSQL en Render
4. ✅ Configurar Web Service en Render
5. ✅ Establecer variables de entorno
6. ✅ Desplegar
7. ✅ Verificar logs

---

## Soporte

Para más información:
- [Render Docs](https://render.com/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Alembic Migrations](https://alembic.sqlalchemy.org/)

