// src/components/admin/TurnoManager.tsx
import { Turno } from '../../services/api';
import { TurnoList } from '../turnos/TurnoList';

interface TurnoManagerProps {
  turnosEsperando: Turno[];
  turnosEnAtencion: Turno[];
  onIniciar: (turnoId: number) => void;
  onCompletar: (turnoId: number) => void;
  onCancelar: (turnoId: number) => void;
}

export const TurnoManager = ({
  turnosEsperando,
  turnosEnAtencion,
  onIniciar,
  onCompletar,
  onCancelar,
}: TurnoManagerProps) => {
  return (
    <div className="row">
      <div className="col-lg-6 mb-4">
        <div className="card border-success">
          <div className="card-header bg-success text-white">
            <h5 className="mb-0">
              <i className="fas fa-play-circle me-2"></i>
              En Atención
            </h5>
          </div>
          <div className="card-body">
            <TurnoList
              turnos={turnosEnAtencion}
              onCompletar={onCompletar}
              onCancelar={onCancelar}
              showActions={true}
            />
          </div>
        </div>
      </div>

      <div className="col-lg-6 mb-4">
        <div className="card border-primary">
          <div className="card-header bg-primary text-white">
            <h5 className="mb-0">
              <i className="fas fa-clock me-2"></i>
              En Espera
            </h5>
          </div>
          <div className="card-body">
            <TurnoList
              turnos={turnosEsperando}
              onIniciar={onIniciar}
              onCancelar={onCancelar}
              showActions={true}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

