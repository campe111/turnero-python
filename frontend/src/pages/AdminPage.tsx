// src/pages/AdminPage.tsx
import { useEffect, useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { turnosAPI, estadisticasAPI, Turno, Estadisticas } from '../services/api';
import { TurnoManager } from '../components/admin/TurnoManager';
import { Estadisticas } from '../components/admin/Estadisticas';
import { Loading } from '../components/common/Loading';
import toast from 'react-hot-toast';

export const AdminPage = () => {
  const { isAdmin, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [reloj, setReloj] = useState(new Date().toLocaleTimeString());

  useEffect(() => {
    if (!isAuthenticated || !isAdmin) {
      navigate('/login');
      return;
    }

    const interval = setInterval(() => {
      setReloj(new Date().toLocaleTimeString());
    }, 1000);

    return () => clearInterval(interval);
  }, [isAuthenticated, isAdmin, navigate]);

  // Auto-refresh cada 30 segundos
  useEffect(() => {
    const interval = setInterval(() => {
      queryClient.invalidateQueries({ queryKey: ['turnos'] });
      queryClient.invalidateQueries({ queryKey: ['estadisticas'] });
    }, 30000);

    return () => clearInterval(interval);
  }, [queryClient]);

  const { data: turnosEsperando = [], isLoading: loadingEsperando } = useQuery({
    queryKey: ['turnos', 'esperando'],
    queryFn: () => turnosAPI.getAll({ estado: 'esperando' }).then((res) => res.data),
    refetchInterval: 30000,
  });

  const { data: turnosEnAtencion = [], isLoading: loadingEnAtencion } = useQuery({
    queryKey: ['turnos', 'en_atencion'],
    queryFn: () => turnosAPI.getAll({ estado: 'en_atencion' }).then((res) => res.data),
    refetchInterval: 30000,
  });

  const { data: estadisticas, isLoading: loadingEstadisticas } = useQuery({
    queryKey: ['estadisticas'],
    queryFn: () => estadisticasAPI.get().then((res) => res.data),
    refetchInterval: 30000,
  });

  const iniciarMutation = useMutation({
    mutationFn: (turnoId: number) => turnosAPI.iniciar(turnoId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['turnos'] });
      queryClient.invalidateQueries({ queryKey: ['estadisticas'] });
      toast.success('Turno iniciado exitosamente');
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.error || 'Error al iniciar turno');
    },
  });

  const completarMutation = useMutation({
    mutationFn: (turnoId: number) => turnosAPI.completar(turnoId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['turnos'] });
      queryClient.invalidateQueries({ queryKey: ['estadisticas'] });
      toast.success('Turno completado exitosamente');
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.error || 'Error al completar turno');
    },
  });

  const cancelarMutation = useMutation({
    mutationFn: (turnoId: number) => turnosAPI.cancelar(turnoId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['turnos'] });
      queryClient.invalidateQueries({ queryKey: ['estadisticas'] });
      toast.success('Turno cancelado exitosamente');
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.error || 'Error al cancelar turno');
    },
  });

  const handleIniciar = (turnoId: number) => {
    if (window.confirm('¿Estás seguro de que quieres iniciar este turno?')) {
      iniciarMutation.mutate(turnoId);
    }
  };

  const handleCompletar = (turnoId: number) => {
    if (window.confirm('¿Estás seguro de que quieres completar este turno?')) {
      completarMutation.mutate(turnoId);
    }
  };

  const handleCancelar = (turnoId: number) => {
    if (window.confirm('¿Estás seguro de que quieres cancelar este turno?')) {
      cancelarMutation.mutate(turnoId);
    }
  };

  if (loadingEsperando || loadingEnAtencion || loadingEstadisticas) {
    return <Loading />;
  }

  return (
    <div className="row">
      <div className="col-12">
        <div className="d-flex justify-content-between align-items-center mb-4">
          <h2>
            <i className="fas fa-cog me-2"></i>
            Panel de Administración
          </h2>
          <div className="text-muted">
            <i className="fas fa-clock me-1"></i>
            <span>{reloj}</span>
          </div>
        </div>

        <TurnoManager
          turnosEsperando={turnosEsperando}
          turnosEnAtencion={turnosEnAtencion}
          onIniciar={handleIniciar}
          onCompletar={handleCompletar}
          onCancelar={handleCancelar}
        />

        {estadisticas && (
          <div className="row mt-4">
            <div className="col-12">
              <div className="card">
                <div className="card-header">
                  <h5 className="mb-0">
                    <i className="fas fa-chart-bar me-2"></i>
                    Estadísticas del Día
                  </h5>
                </div>
                <div className="card-body">
                  <Estadisticas estadisticas={estadisticas} />
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

