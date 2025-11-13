// src/pages/Home.tsx
import { useEffect, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { categoriasAPI, Categoria } from '../services/api';
import { CategoriaCard } from '../components/turnos/CategoriaCard';
import { Loading } from '../components/common/Loading';

export const Home = () => {
  const [refreshKey, setRefreshKey] = useState(0);

  const { data: categorias, isLoading, refetch } = useQuery({
    queryKey: ['categorias', refreshKey],
    queryFn: () => categoriasAPI.getAll().then((res) => res.data),
  });

  const handleTurnoCreado = () => {
    setRefreshKey((prev) => prev + 1);
  };

  if (isLoading) {
    return <Loading />;
  }

  return (
    <div className="row">
      <div className="col-lg-8 mx-auto">
        <div className="text-center mb-5">
          <h1 className="display-4 text-primary">
            <i className="fas fa-clock me-3"></i>
            Sistema de Turnos
          </h1>
          <p className="lead">
            Selecciona el tipo de atención que necesitas y obtén tu turno
          </p>
        </div>

        <div className="row g-4">
          {categorias?.map((categoria: Categoria) => (
            <CategoriaCard
              key={categoria.id}
              categoria={categoria}
              onTurnoCreado={handleTurnoCreado}
            />
          ))}
        </div>

        <div className="row mt-5">
          <div className="col-lg-8 mx-auto">
            <div className="card bg-light">
              <div className="card-body">
                <h5 className="card-title text-center mb-3">
                  <i className="fas fa-info-circle me-2"></i>
                  Información del Sistema
                </h5>
                <div className="row text-center">
                  <div className="col-md-4">
                    <i className="fas fa-clock fa-2x text-primary mb-2"></i>
                    <h6>Horario de Atención</h6>
                    <p className="small text-muted">
                      Lunes a Viernes<br />
                      8:00 - 18:00
                    </p>
                  </div>
                  <div className="col-md-4">
                    <i className="fas fa-phone fa-2x text-success mb-2"></i>
                    <h6>Contacto</h6>
                    <p className="small text-muted">
                      Tel: (123) 456-7890<br />
                      Email: info@turnero.com
                    </p>
                  </div>
                  <div className="col-md-4">
                    <i className="fas fa-map-marker-alt fa-2x text-warning mb-2"></i>
                    <h6>Ubicación</h6>
                    <p className="small text-muted">
                      Av. Principal 123<br />
                      Ciudad, País
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

