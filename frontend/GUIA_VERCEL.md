# 🚀 Guía de Despliegue en Vercel

## ⚠️ Problemas Comunes y Soluciones

### 1. Root Directory NO Configurado

**Síntoma:** Vercel no encuentra el `package.json` o falla el build.

**Solución:**
1. Ve a Vercel Dashboard → Tu Proyecto → **Settings** → **General**
2. Busca **Root Directory**
3. Configura: `frontend`
4. Guarda los cambios
5. Vercel hará un nuevo deployment automáticamente

### 2. Build Command Incorrecto

**Síntoma:** El build falla con errores.

**Solución:**
En Vercel Dashboard → Settings → General → Build & Development Settings:
- **Build Command:** `npm run build` (o dejar vacío, Vercel lo detecta automáticamente)
- **Output Directory:** `dist` (o dejar vacío)
- **Install Command:** `npm install` (o dejar vacío)

### 3. Variables de Entorno Faltantes

**Síntoma:** La app carga pero no se conecta al backend.

**Solución:**
1. Ve a **Settings** → **Environment Variables**
2. Agrega:
   - **Name:** `VITE_API_URL`
   - **Value:** URL de tu backend (ej: `https://tu-backend.railway.app`)
   - **Environment:** Production, Preview, Development (marca todos)
3. Guarda y haz un nuevo deployment

### 4. Framework Detection

Vercel debería detectar automáticamente que es un proyecto Vite, pero si no:
- Ve a **Settings** → **General**
- **Framework Preset:** Selecciona **Vite**

### 5. Verificar el Deployment

**Pasos para verificar:**
1. Ve a la pestaña **Deployments**
2. Haz clic en el último deployment
3. Revisa los **Build Logs**
4. Si hay errores, cópialos y revísalos

## 📋 Checklist de Configuración

- [ ] Root Directory configurado como `frontend`
- [ ] Build Command: `npm run build` (o vacío)
- [ ] Output Directory: `dist` (o vacío)
- [ ] Framework Preset: **Vite**
- [ ] Variable de entorno `VITE_API_URL` configurada
- [ ] El repositorio está conectado correctamente
- [ ] La rama de producción es `main` (o la que uses)

## 🔍 Verificar Build Local

Antes de desplegar, verifica que el build funciona localmente:

```bash
cd frontend
npm install
npm run build
```

Si el build funciona localmente pero falla en Vercel, revisa los logs en Vercel Dashboard.

## 🆘 Errores Comunes

### Error: "Cannot find module"
- **Causa:** Dependencias no instaladas
- **Solución:** Verifica que `package.json` tenga todas las dependencias

### Error: "Build failed"
- **Causa:** Error en el código TypeScript/React
- **Solución:** Revisa los logs de build en Vercel

### Error: "404 Not Found" en rutas
- **Causa:** Rewrites no configurados
- **Solución:** El `vercel.json` ya tiene los rewrites configurados

## 📞 Si Nada Funciona

1. **Elimina el proyecto en Vercel** y vuelve a conectarlo
2. **Verifica que el repositorio esté actualizado** (push reciente)
3. **Revisa los logs completos** en Vercel Dashboard
4. **Prueba con un deployment manual** desde GitHub

