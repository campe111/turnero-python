# Sistema de Turnos - Frontend React + Vite

Frontend moderno del Sistema de Turnos desarrollado con React, TypeScript y Vite.

## 🚀 Características

- ⚡ **Vite** - Build tool ultra rápido
- ⚛️ **React 18** - Framework moderno
- 📘 **TypeScript** - Tipado estático
- 🎨 **Bootstrap 5** - Diseño responsive
- 🔐 **JWT Authentication** - Autenticación segura
- 🔄 **React Query** - Gestión de estado del servidor
- 🍞 **React Hot Toast** - Notificaciones elegantes
- 📱 **Responsive Design** - Adaptable a todos los dispositivos

## 📋 Requisitos

- Node.js 18+ 
- npm o yarn

## 🛠️ Instalación

1. **Instalar dependencias:**
   ```bash
   npm install
   ```

2. **Configurar variables de entorno:**
   
   Crea un archivo `.env.local` en la raíz del proyecto:
   ```env
   VITE_API_URL=http://localhost:5000
   ```

3. **Iniciar servidor de desarrollo:**
   ```bash
   npm run dev
   ```

   La aplicación estará disponible en `http://localhost:3000`

## 📦 Scripts Disponibles

- `npm run dev` - Inicia el servidor de desarrollo
- `npm run build` - Construye la aplicación para producción
- `npm run preview` - Previsualiza el build de producción
- `npm run vercel-build` - Build específico para Vercel

## 🏗️ Estructura del Proyecto

```
frontend/
├── src/
│   ├── components/       # Componentes reutilizables
│   │   ├── common/       # Componentes comunes (Navbar, Footer, Loading)
│   │   ├── auth/         # Componentes de autenticación
│   │   ├── turnos/       # Componentes relacionados con turnos
│   │   └── admin/        # Componentes del panel de administración
│   ├── pages/            # Páginas principales
│   ├── services/         # Servicios API
│   ├── context/          # Context API (AuthContext)
│   ├── hooks/            # Custom hooks
│   ├── utils/            # Utilidades y helpers
│   ├── styles/           # Estilos globales
│   ├── App.tsx           # Componente principal
│   └── main.tsx          # Punto de entrada
├── public/               # Archivos estáticos
├── index.html            # HTML principal
├── vite.config.ts        # Configuración de Vite
├── tsconfig.json         # Configuración de TypeScript
└── package.json          # Dependencias del proyecto
```

## 🔌 API y Backend

Este frontend se conecta a un backend Flask que debe estar corriendo en `http://localhost:5000` (o la URL especificada en `.env.local`).

### Endpoints utilizados:

- `GET /api/categorias` - Obtener categorías
- `POST /api/turnos` - Crear turno
- `GET /api/turnos` - Obtener turnos (con filtros)
- `POST /api/auth/login` - Iniciar sesión
- `POST /api/auth/register` - Registrarse
- `GET /api/auth/me` - Obtener usuario actual
- `GET /api/estadisticas` - Obtener estadísticas (admin)
- `POST /api/iniciar_turno/:id` - Iniciar turno (admin)
- `POST /api/completar_turno/:id` - Completar turno (admin)
- `POST /api/cancelar_turno/:id` - Cancelar turno (admin)

## 🚀 Despliegue en Vercel

### Opción 1: Desde la CLI

1. **Instalar Vercel CLI:**
   ```bash
   npm i -g vercel
   ```

2. **Login:**
   ```bash
   vercel login
   ```

3. **Desplegar:**
   ```bash
   vercel
   ```

### Opción 2: Desde GitHub

1. Conecta tu repositorio con Vercel
2. Vercel detectará automáticamente que es un proyecto Vite
3. Configura las variables de entorno:
   - `VITE_API_URL` - URL de tu backend (ej: `https://tu-backend.railway.app`)

### Variables de Entorno en Vercel

En el dashboard de Vercel:
- Settings → Environment Variables
- Agrega `VITE_API_URL` con la URL de tu backend

## 🔒 Autenticación

El sistema utiliza JWT (JSON Web Tokens) para la autenticación:

- Los tokens se almacenan en `localStorage`
- Se envían automáticamente en el header `Authorization` de cada request
- Si el token expira, el usuario es redirigido al login

## 📱 Responsive Design

La aplicación está completamente optimizada para:
- 📱 Móviles
- 📱 Tablets
- 💻 Desktop

## 🎨 Personalización

Los estilos se pueden personalizar editando:
- `src/styles/globals.css` - Estilos globales
- Componentes individuales para estilos específicos

## 🐛 Troubleshooting

### Error: CORS
- Verifica que el backend tenga CORS configurado
- Revisa que la URL del backend sea correcta en `.env.local`

### Error: Variables de entorno no funcionan
- Asegúrate de usar el prefijo `VITE_` en las variables
- Reinicia el servidor de desarrollo después de cambiar `.env.local`

### Error: Build falla
- Verifica que todas las dependencias estén instaladas
- Revisa los logs de error en la consola

## 📚 Tecnologías Utilizadas

- **React** - Biblioteca UI
- **TypeScript** - Tipado estático
- **Vite** - Build tool
- **React Router** - Routing
- **React Query** - Data fetching
- **Axios** - HTTP client
- **React Hot Toast** - Notificaciones
- **Bootstrap 5** - Framework CSS
- **Font Awesome** - Iconos
- **date-fns** - Manejo de fechas

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

---

**¡Disfruta usando el Sistema de Turnos! 🎉**

