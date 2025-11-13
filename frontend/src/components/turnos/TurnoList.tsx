// src/components/turnos/TurnoList.tsx
import { Turno } from '../../services/api';
import { formatTime, getEstadoBadgeClass, getEstadoLabel } from '../../utils/helpers';

interface TurnoListProps {
  turnos: Turno[];
  onIniciar?: (turnoId: number) => void;
  onCompletar?: (turnoId: number) => void;
  onCancelar?: (turnoId: number) => void;
  showActions?: boolean;
}

export const TurnoList = ({
  turnos,
  onIniciar,
  onCompletar,
  onCancelar,
  showActions = false,
}: TurnoListProps) => {
  if (turnos.length === 0) {
    return (
      <p className="text-muted text-center py-3">No hay turnos disponibles</p>
    );
  }

  return (
    <div className="list-group">
      {turnos.map((turno) => (
        <div
          key={turno.id}
          className="list-group-item d-flex justify-content-between align-items-center"
        >
          <div>
            <h6 className="mb-1">
              Turno #{turno.numero} - {turno.categoria}
            </h6>
            <small className="text-muted">
              <span className={`badge ${getEstadoBadgeClass(turno.estado)} me-2`}>
                {getEstadoLabel(turno.estado)}
              </span>
              {turno.hora_estimada && (
                <>
                  <i className="fas fa-clock me-1"></i>
                  Hora estimada: {formatTime(turno.hora_estimada)}
                </>
              )}
            </small>
          </div>
          {showActions && (
            <div>
              {turno.estado === 'esperando' && onIniciar && (
                <button
                  className="btn btn-sm btn-success me-2"
                  onClick={() => onIniciar(turno.id)}
                >
                  <i className="fas fa-play me-1"></i>
                  Iniciar
                </button>
              )}
              {turno.estado === 'en_atencion' && onCompletar && (
                <button
                  className="btn btn-sm btn-primary me-2"
                  onClick={() => onCompletar(turno.id)}
                >
                  <i className="fas fa-check me-1"></i>
                  Completar
                </button>
              )}
              {(turno.estado === 'esperando' || turno.estado === 'en_atencion') &&
                onCancelar && (
                  <button
                    className="btn btn-sm btn-danger"
                    onClick={() => onCancelar(turno.id)}
                  >
                    <i className="fas fa-times me-1"></i>
                    Cancelar
                  </button>
                )}
            </div>
          )}
        </div>
      ))}
    </div>
  );
};

