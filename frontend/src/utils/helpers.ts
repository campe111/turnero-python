// src/utils/helpers.ts
import { format } from 'date-fns';
import { es } from 'date-fns/locale';

export const formatTime = (dateString: string | null): string => {
  if (!dateString) return 'N/A';
  try {
    return format(new Date(dateString), 'HH:mm', { locale: es });
  } catch {
    return 'N/A';
  }
};

export const formatDateTime = (dateString: string | null): string => {
  if (!dateString) return 'N/A';
  try {
    return format(new Date(dateString), 'dd/MM/yyyy HH:mm', { locale: es });
  } catch {
    return 'N/A';
  }
};

export const getEstadoBadgeClass = (estado: string): string => {
  const classes: Record<string, string> = {
    esperando: 'bg-primary',
    en_atencion: 'bg-success',
    completado: 'bg-info',
    cancelado: 'bg-danger',
  };
  return classes[estado] || 'bg-secondary';
};

export const getEstadoLabel = (estado: string): string => {
  const labels: Record<string, string> = {
    esperando: 'En Espera',
    en_atencion: 'En Atención',
    completado: 'Completado',
    cancelado: 'Cancelado',
  };
  return labels[estado] || estado;
};

