// src/components/admin/Estadisticas.tsx
import { Estadisticas as EstadisticasType } from '../../services/api';

interface EstadisticasProps {
  estadisticas: EstadisticasType;
}

export const Estadisticas = ({ estadisticas }: EstadisticasProps) => {
  return (
    <div className="row text-center">
      <div className="col-md-3 mb-3">
        <div className="border rounded p-3">
          <i className="fas fa-users fa-2x text-primary mb-2"></i>
          <h4>{estadisticas.total}</h4>
          <p className="text-muted mb-0">Total Turnos</p>
        </div>
      </div>
      <div className="col-md-3 mb-3">
        <div className="border rounded p-3">
          <i className="fas fa-clock fa-2x text-warning mb-2"></i>
          <h4>{estadisticas.esperando}</h4>
          <p className="text-muted mb-0">En Espera</p>
        </div>
      </div>
      <div className="col-md-3 mb-3">
        <div className="border rounded p-3">
          <i className="fas fa-play fa-2x text-success mb-2"></i>
          <h4>{estadisticas.en_atencion}</h4>
          <p className="text-muted mb-0">En Atención</p>
        </div>
      </div>
      <div className="col-md-3 mb-3">
        <div className="border rounded p-3">
          <i className="fas fa-check fa-2x text-info mb-2"></i>
          <h4>{estadisticas.completados}</h4>
          <p className="text-muted mb-0">Completados</p>
        </div>
      </div>
    </div>
  );
};

