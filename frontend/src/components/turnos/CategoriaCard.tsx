// src/components/turnos/CategoriaCard.tsx
import { useState } from 'react';
import { turnosAPI, Categoria } from '../../services/api';
import toast from 'react-hot-toast';
import { formatTime } from '../../utils/helpers';
import { ICONOS_CATEGORIAS, COLORES_CATEGORIAS } from '../../utils/constants';

interface CategoriaCardProps {
  categoria: Categoria;
  onTurnoCreado?: () => void;
}

export const CategoriaCard = ({ categoria, onTurnoCreado }: CategoriaCardProps) => {
  const [loading, setLoading] = useState(false);

  const handleSacarTurno = async () => {
    setLoading(true);
    try {
      const response = await turnosAPI.create(categoria.id);
      const turno = response.data;
      
      const horaEstimada = formatTime(turno.hora_estimada);

      toast.success(
        `Turno #${turno.numero} generado exitosamente. Hora estimada: ${horaEstimada}`,
        { duration: 5000 }
      );

      onTurnoCreado?.();
    } catch (error: any) {
      toast.error(
        error.response?.data?.error || 'Error al generar el turno'
      );
    } finally {
      setLoading(false);
    }
  };

  const icono = ICONOS_CATEGORIAS[categoria.nombre] || 'clock';
  const color = COLORES_CATEGORIAS[categoria.nombre] || 'primary';

  return (
    <div className="col-md-6 col-lg-4 mb-4">
      <div className="card h-100 shadow-sm border-0">
        <div className="card-body text-center">
          <div className="mb-3">
            <i className={`fas fa-${icono} fa-3x text-${color}`}></i>
          </div>
          <h5 className="card-title">{categoria.nombre}</h5>
          <p className="card-text text-muted">{categoria.descripcion}</p>
          <p className="card-text">
            <small className="text-muted">
              <i className="fas fa-clock me-1"></i>
              Tiempo estimado: {categoria.tiempo_estimado} min
            </small>
          </p>
          <button
            type="button"
            className={`btn btn-${color} w-100`}
            onClick={handleSacarTurno}
            disabled={loading}
          >
            {loading ? (
              <>
                <span className="spinner-border spinner-border-sm me-2"></span>
                Procesando...
              </>
            ) : (
              <>
                <i className="fas fa-ticket-alt me-2"></i>
                Sacar Turno
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
};

