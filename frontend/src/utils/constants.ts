// src/utils/constants.ts

export const ESTADOS_TURNO = {
  ESPERANDO: 'esperando',
  EN_ATENCION: 'en_atencion',
  COMPLETADO: 'completado',
  CANCELADO: 'cancelado',
} as const;

export const ICONOS_CATEGORIAS: Record<string, string> = {
  'Atencion General': 'users',
  'Pagos': 'credit-card',
  'Reclamos': 'exclamation-triangle',
  'Informes': 'file-alt',
};

export const COLORES_CATEGORIAS: Record<string, string> = {
  'Atencion General': 'primary',
  'Pagos': 'success',
  'Reclamos': 'warning',
  'Informes': 'info',
};

