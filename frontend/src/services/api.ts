// src/services/api.ts
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

// Crear instancia de axios
const apiClient = axios.create({
  baseURL: `${API_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para agregar token de autenticación
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor para manejar errores
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expirado o inválido
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Tipos
export interface Categoria {
  id: number;
  nombre: string;
  descripcion: string;
  tiempo_estimado: number;
}

export interface Turno {
  id: number;
  numero: number;
  categoria_id: number;
  categoria: string;
  estado: 'esperando' | 'en_atencion' | 'completado' | 'cancelado';
  fecha_creacion: string;
  hora_estimada: string | null;
  hora_inicio: string | null;
  hora_fin: string | null;
}

export interface User {
  id: number;
  nombre: string;
  email: string;
  es_admin: boolean;
}

export interface Estadisticas {
  total: number;
  esperando: number;
  en_atencion: number;
  completados: number;
  cancelados: number;
}

// API de Categorías
export const categoriasAPI = {
  getAll: () => apiClient.get<Categoria[]>('/categorias'),
  getById: (id: number) => apiClient.get<Categoria>(`/categorias/${id}`),
};

// API de Turnos
export const turnosAPI = {
  getAll: (params?: { estado?: string; categoria_id?: number }) => 
    apiClient.get<Turno[]>('/turnos', { params }),
  create: (categoriaId: number) => 
    apiClient.post<Turno>('/turnos', { categoria_id: categoriaId }),
  getById: (id: number) => 
    apiClient.get<Turno>(`/turnos/${id}`),
  iniciar: (turnoId: number) => 
    apiClient.post(`/iniciar_turno/${turnoId}`),
  completar: (turnoId: number) => 
    apiClient.post(`/completar_turno/${turnoId}`),
  cancelar: (turnoId: number) => 
    apiClient.post(`/cancelar_turno/${turnoId}`),
};

// API de Autenticación
export const authAPI = {
  login: (email: string, password: string) =>
    apiClient.post<{ access_token: string; user: User }>('/auth/login', { email, password }),
  register: (nombre: string, email: string, password: string) =>
    apiClient.post<{ access_token: string; user: User }>('/auth/register', { nombre, email, password }),
  me: () =>
    apiClient.get<User>('/auth/me'),
  logout: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    return Promise.resolve();
  },
};

// API de Estadísticas
export const estadisticasAPI = {
  get: () => apiClient.get<Estadisticas>('/estadisticas'),
};

export default apiClient;

