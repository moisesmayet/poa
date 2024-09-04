from django.urls import path
from .views import *

urlpatterns = [
    path('usuarios_list', UsuariosList.as_view(), name="usuarios_list"),
    path('sedes_list', SedesList.as_view(), name="sedes_list"),
    path('tipos_estamentos_list', TipoEstamentoList.as_view(), name="tipos_estamentos_list"),
    path('estamento_save/<str:tipo_code>', EstamentoSave.as_view(), name="estamento_save"),
    path('estamentos_list/<str:tipo_code>', EstamentoList.as_view(), name="estamentos_list"),
    path('ejes_list', EjesList.as_view(), name="ejes_list"),
    path('objetivos_list', ObjetivosList.as_view(), name="objetivos_list"),
    path('lineas_save', LineaSave.as_view(), name="linea_save"),
    path('lineas_list', LineasList.as_view(), name="lineas_list"),
    path('indicadores_list', IndicadoresList.as_view(), name="indicadores_list"),
    path('responsables_list', ResponsablesList.as_view(), name="responsables_list"),
    path('parametros_list', ParametrosList.as_view(), name="parametros_list"),
    path('notificaciones_list', NotificacionesList.as_view(), name="notificaciones_list"),
    path('logs_list', LogsList.as_view(), name="logs_list"),
    path('update_colaborador', UpdateColaborador.as_view(), name="update_colaborador"),
    path('tableros_list', TablerosList.as_view(), name="tableros_list"),
    path('test', Test, name="test"),
]
