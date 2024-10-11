import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.db.models import Q, Value, Case, When, BooleanField
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from administration.forms import FormLinea, FormEstamento
from authentication.models import CustomUser
from notification.views import NotificationsSearchList
from poa.models import Eje, Objetivo, Linea, MedioVerificacion, Actividad, Responsable, Log
from uapa.models import Sede, TipoEstamento, Estamento, Colaborador, TableauEstamento, Tableau
from notification.models import Parametro
from notification.views import NotificationMark


class UsuariosList(View):
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    # noinspection PyMethodMayBeStatic
    def get(self, request):
        search = request.GET.get('search', '')
        users_list = CustomUser.objects.filter(
            Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(email__icontains=search))
        return render(request, "usuarios_list.html", {"users_list": users_list})

    # noinspection PyMethodMayBeStatic
    def post(self, request, *args, **kwargs):
        action = request.POST.get('action', '')
        user_id = request.POST.get('id', '')
        email = request.POST.get('email', '')
        email = email.strip()
        other_user = CustomUser.objects.filter(email=email).first()

        error = False
        if action == 'new':
            custon_user = CustomUser()
            if other_user is not None:
                error = True
        else:
            custon_user = CustomUser.objects.get(id=user_id)
            if other_user is not None and custon_user.id != other_user.id:
                error = True

        if not error:
            if action != 'delete':
                if action != 'edit':
                    custon_user.password = make_password(str(request.POST.get('password1', '')))

                if action != 'password':
                    custon_user.email = email
                    custon_user.username = request.POST.get('first_name', '').upper().strip()
                    custon_user.first_name = request.POST.get('first_name', '').upper().strip()
                    custon_user.last_name = request.POST.get('last_name', '').upper().strip()
                    if request.POST.get('is_active', None) is None:
                        custon_user.is_active = False
                    else:
                        custon_user.is_active = True
                    if request.POST.get('is_superuser', None) is None:
                        custon_user.is_superuser = False
                    else:
                        custon_user.is_superuser = True

                custon_user.save()
            else:
                custon_user.delete()
        else:
            messages.error(request, F"Ya el correo " + email + " está siendo utilizado por " + other_user.username)

        return redirect("usuarios_list")


class EjesList(View):
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    # noinspection PyMethodMayBeStatic
    def get(self, request):
        search = request.GET.get('search', '')
        ejes_list = Eje.objects.filter(eje_description__icontains=search)
        return render(request, "ejes_list.html", {"ejes_list": ejes_list})

    # noinspection PyMethodMayBeStatic
    def post(self, request, *args, **kwargs):
        action = request.POST.get('action', '')
        eje_id = request.POST.get('id', '')

        if action == 'new':
            eje = Eje()
        else:
            eje = Eje.objects.get(id=eje_id)

        if action != 'delete':
            eje.eje_description = request.POST.get('eje_description', '').strip()
            eje.save()
        else:
            eje.delete()

        return redirect("ejes_list")


class ObjetivosList(View):
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    # noinspection PyMethodMayBeStatic
    def get(self, request):
        search = request.GET.get('search', '')
        ejes_list = Eje.objects.all()
        objetivos_list = Objetivo.objects.filter(objetivo_description__icontains=search)
        return render(request, "objetivos_list.html", {"objetivos_list": objetivos_list, "ejes_list": ejes_list})

    # noinspection PyMethodMayBeStatic
    def post(self, request, *args, **kwargs):
        action = request.POST.get('action', '')
        objetivo_id = request.POST.get('id', '')

        if action == 'new':
            objetivo = Objetivo()
        else:
            objetivo = Objetivo.objects.get(id=objetivo_id)

        if action != 'delete':
            objetivo.objetivo_description = request.POST.get('objetivo_description', '').strip()
            objetivo.objetivo_eje_id = request.POST.get('objetivo_eje', '')
            objetivo.save()
        else:
            objetivo.delete()

        return redirect("objetivos_list")


class LineaSave(View):
    # noinspection PyMethodMayBeStatic
    def post(self, request, *args, **kwargs):
        action = request.POST.get('action', '')
        linea_id = request.POST.get('id', '')
        objetivo_id = request.POST.get('level2', '')

        if action == 'new':
            linea = Linea()
        else:
            linea = Linea.objects.get(id=linea_id)

        if action != 'delete':
            form = FormLinea(request.POST)
            if form.is_valid():
                linea.linea_description = request.POST.get('linea_description', '').strip()
                linea.linea_objetivo_id = objetivo_id
                linea.save()
        else:
            linea.delete()

        return redirect("lineas_list")


class LineasList(TemplateView):
    template_name = 'lineas_list.html'
    search = ''

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.search = request.GET.get('search', '')
        return super().dispatch(request, *args, **kwargs)

    # noinspection PyMethodMayBeStatic
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'load_level2':
                data = []
                for objetivo in Objetivo.objects.filter(objetivo_eje_id=request.POST['id']):
                    data.append({'id': objetivo.id, 'name': objetivo.objetivo_description})
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        form_linea_add = FormLinea(initial={'action': 'new'})
        form_linea_add.fields['level1'].initial = 0
        form_linea_add.fields['level2'].queryset = Objetivo.objects.filter(objetivo_eje_id=1)
        form_linea_add.fields['level2'].initial = 0

        lineas_list = Linea.objects.filter(linea_description__icontains=self.search)
        list_forms_lineas = []
        for linea in lineas_list:
            eje_id = linea.linea_objetivo.objetivo_eje_id
            objetivo_id = linea.linea_objetivo_id
            form_linea = FormLinea(initial={'action': 'edit', 'id': linea.id})
            form_linea.fields['level1'].initial = eje_id
            form_linea.fields['level2'].queryset = Objetivo.objects.filter(
                objetivo_eje_id=eje_id)
            form_linea.fields['level2'].initial = objetivo_id
            form_linea.fields['linea_description'].initial = linea.linea_description

            list_forms_lineas.append({'linea': linea, 'form_linea': form_linea})

        seccion_lineas = {'form_linea_add': form_linea_add, 'list_forms_lineas': list_forms_lineas}

        context = super().get_context_data(**kwargs)
        context['seccion_lineas'] = seccion_lineas

        return context


class TipoEstamentoList(View):
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    # noinspection PyMethodMayBeStatic
    def get(self, request):
        search = request.GET.get('search', '')

        tipos_estamentos_list = TipoEstamento.objects.filter(
            Q(tipo_name__icontains=search) | Q(tipo_cargo__icontains=search))
        return render(request, "tipos_estamentos_list.html", {"tipos_estamentos_list": tipos_estamentos_list})

    # noinspection PyMethodMayBeStatic
    def post(self, request, *args, **kwargs):
        action = request.POST.get('action', '')
        tipo_id = request.POST.get('id', '')

        if action == 'new':
            tipo = TipoEstamento()
        else:
            tipo = TipoEstamento.objects.get(id=tipo_id)

        if action != 'delete':
            tipo.tipo_name = request.POST.get('tipo_name', '').upper().strip()
            tipo.tipo_code = request.POST.get('tipo_code', '').upper().strip()
            tipo.tipo_cargo = request.POST.get('tipo_cargo', '').upper().strip()
            tipo.tipo_faicon = request.POST.get('tipo_faicon', '')
            tipo.save()
        else:
            tipo.delete()

        return redirect("tipos_estamentos_list")


class UpdateColaborador(View):
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # noinspection PyMethodMayBeStatic
    def post(self, request, *args, **kwargs):
        estamento_id = request.POST.get('estamento_id', '')
        colaborador_ids = request.POST.getlist('colaborador_ids[]', [])
        Colaborador.objects.filter(colaborador_estamento_id=estamento_id).exclude(
            colaborador_user_id__in=colaborador_ids).delete()
        colaboradores_existente_ids = Colaborador.objects.filter(
            colaborador_estamento_id=estamento_id
        ).values_list('colaborador_user_id', flat=True)
        colaborador_ids = set(map(int, colaborador_ids))
        colaboradores_existente_ids = set(colaboradores_existente_ids)
        nuevos_colaboradores_ids = colaborador_ids - colaboradores_existente_ids
        for colaborador_id in nuevos_colaboradores_ids:
            colaborador = Colaborador()
            colaborador.colaborador_estamento_id = estamento_id
            colaborador.colaborador_user_id = colaborador_id
            colaborador.colaborador_can_edit = True
            colaborador.save()

        return JsonResponse({'success': True})


class EstamentoSave(View):
    tipo_code = ''

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.tipo_code = kwargs.get('tipo_code')
        return super().dispatch(request, *args, **kwargs)

    # noinspection PyMethodMayBeStatic
    def post(self, request, *args, **kwargs):
        tipo_code = self.tipo_code
        estamento_id = int(request.POST.get('id', '0'))
        estamento_sub_id = int(request.POST.get(f'selectlevel2_{estamento_id}', '0'))
        action = request.POST.get('action', '')

        if action == 'new':
            estamento = Estamento()
        else:
            estamento = Estamento.objects.get(id=estamento_id)

        if action != 'delete':
            form = FormEstamento(request.POST)
            if form.is_valid() or estamento_id == 1:
                estamento_name = request.POST.get('estamento_name', '').upper().strip()
                estamento_sede_id = request.POST.get('estamento_sede', '')
                estamento_exists = Estamento.objects.filter(estamento_name=estamento_name,
                                                            estamento_sede_id=estamento_sede_id).exclude(
                    id=estamento_id).first()
                if estamento_exists is None:
                    list_roots = []
                    if estamento_sub_id:
                        estamento.estamento_sub_id = estamento_sub_id
                        estamento_roots = GetRoots(estamento_sub_id, '')
                        estamento.estamento_roots = estamento_roots
                        list_roots = list(map(int, estamento_roots.split(',')))

                    if estamento_id not in list_roots:
                        estamento.estamento_name = estamento_name
                        estamento.estamento_sede_id = estamento_sede_id
                        estamento.estamento_user_id = request.POST.get('estamento_user', '')
                        estamento.estamento_tipo_id = request.POST.get('estamento_tipo', '')
                        if request.POST.get('estamento_has_poa', None) is None:
                            estamento.estamento_has_poa = False
                        else:
                            estamento.estamento_has_poa = True
                        estamento.save()
                    else:
                        nombres = ', '.join([estamento.estamento_name for estamento in
                                             Estamento.objects.filter(id__in=list_roots).order_by('-id')])
                        messages.error(request, F"{estamento_name} está dentro de la lista de sus "
                                                F"superiores {nombres}")
                else:
                    messages.error(request, F"Ya existe {estamento_name}")
        else:
            estamento.delete()

        return redirect("estamentos_list", tipo_code=tipo_code)


class EstamentoList(TemplateView):
    template_name = 'estamentos_list.html'
    search = ''

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.search = request.GET.get('search', '')
        return super().dispatch(request, *args, **kwargs)

    # noinspection PyMethodMayBeStatic
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'tableros':
                estamento_id = request.POST['id']
                tablero_ids = [int(key.replace('tablero_', '')) for key in request.POST if key.startswith('tablero_')]
                tableros_list = TableauEstamento.objects.filter(tablero_estamento_id=estamento_id)
                new_tableros_ids = set(tablero_ids) - set(tableros_list.values_list('tablero_tableau_id', flat=True))
                for new_tableros_id in new_tableros_ids:
                    TableauEstamento.objects.create(tablero_estamento_id=estamento_id,
                                                    tablero_tableau_id=new_tableros_id)
                tableros_list.exclude(tablero_tableau_id__in=tablero_ids).delete()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        tipo_code = kwargs.get('tipo_code')
        estamento_tipo = TipoEstamento.objects.filter(tipo_code=tipo_code).first()

        form_estamento_add = FormEstamento(initial={'action': 'new', 'estamento_tipo': estamento_tipo.id})
        form_estamento_add.fields['estamento_has_poa'].initial = True

        estamentos = Estamento.objects.filter(
            Q(estamento_tipo=estamento_tipo) & Q(estamento_name__icontains=self.search))
        list_forms_estamentos = []
        for estamento in estamentos:
            form_estamento = FormEstamento(
                initial={'action': 'edit', 'id': estamento.id, 'estamento_tipo': estamento_tipo.id})
            form_estamento.fields['estamento_name'].initial = estamento.estamento_name
            form_estamento.fields['estamento_sede'].initial = estamento.estamento_sede_id
            form_estamento.fields['estamento_user'].initial = estamento.estamento_user_id
            form_estamento.fields['estamento_has_poa'].initial = estamento.estamento_has_poa

            users = CustomUser.objects.filter(is_active=True)
            colaboradores = Colaborador.objects.filter(colaborador_estamento=estamento)
            colaboradores_ids = [colaborador.colaborador_user_id for colaborador in colaboradores]
            colaboradores_list = []
            for user in users:
                username = user.username.capitalize()
                selected = user.id in colaboradores_ids
                colaboradores_list.append({'id': user.id, 'username': username, 'selected': selected})

            tableaus = TableauEstamento.objects.filter(tablero_estamento=estamento).values_list('tablero_tableau',
                                                                                                flat=True)
            tableros_list = Tableau.objects.annotate(
                tableau_checked=Case(
                    When(id__in=tableaus, then=Value(True)),
                    default=Value(False),
                    output_field=BooleanField()
                )
            )

            tableros_annos = list(range(datetime.datetime.now().year + 1, 2022))
            list_forms_estamentos.append(
                {'estamento': estamento, 'form_estamento': form_estamento, 'colaboradores_list': colaboradores_list,
                 'tableros_list': tableros_list, 'tableros_annos': tableros_annos})

        seccion_estamentos = {'form_estamento_add': form_estamento_add, 'list_forms_estamentos': list_forms_estamentos}

        if estamento_tipo.tipo_name[-2:] == "ÓN":
            tipo = {"single": estamento_tipo.tipo_name, "plural": estamento_tipo.tipo_name[0:-2] + "ONES",
                    "cargo": estamento_tipo.tipo_cargo, "code": tipo_code}
        else:
            if estamento_tipo.tipo_name[-1:] == "D":
                tipo = {"single": estamento_tipo.tipo_name, "plural": estamento_tipo.tipo_name + "ES",
                        "cargo": estamento_tipo.tipo_cargo, "code": tipo_code}
            else:
                tipo = {"single": estamento_tipo.tipo_name, "plural": estamento_tipo.tipo_name + "S",
                        "cargo": estamento_tipo.tipo_cargo, "code": tipo_code}

        tipos_list = TipoEstamento.objects.all()
        estamento_tipos = []
        estamento_subs = Estamento.objects.all()
        for estamento_tipo in tipos_list:
            estamentos_options = ','.join([str(estamento.id) for estamento in Estamento.objects.filter(estamento_tipo=estamento_tipo)])
            estamento_tipos.append(
                {"estamento_tipo": estamento_tipo, "estamentos_options": estamentos_options})

        context = super().get_context_data(**kwargs)
        context['seccion_estamentos'] = seccion_estamentos
        context['estamento_tipos'] = estamento_tipos
        context['estamento_subs'] = estamento_subs
        context['tipo'] = tipo

        return context


class SedesList(View):
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    # noinspection PyMethodMayBeStatic
    def get(self, request):
        search = request.GET.get('search', '')
        sedes_list = Sede.objects.filter(sede_name__icontains=search)
        return render(request, "sedes_list.html", {"sedes_list": sedes_list})

    # noinspection PyMethodMayBeStatic
    def post(self, request, *args, **kwargs):
        action = request.POST.get('action', '')
        sede_id = request.POST.get('id', '')

        if action == 'new':
            sede = Sede()
        else:
            sede = Sede.objects.get(id=sede_id)

        if action != 'delete':
            sede.sede_name = request.POST.get('sede_name', '').upper().strip()
            sede.save()
        else:
            sede.delete()

        return redirect("sedes_list")


class IndicadoresList(View):
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    # noinspection PyMethodMayBeStatic
    def get(self, request):
        search = request.GET.get('search', '')
        user = request.user
        medios_list = MedioVerificacion.objects.filter(medio_user=user, medio_description__icontains=search)
        return render(request, "indicadores_list.html", {"medios_list": medios_list})

    # noinspection PyMethodMayBeStatic
    def post(self, request, *args, **kwargs):
        action = request.POST.get('action', '')
        medio_id = request.POST.get('id', '')

        if action == 'new':
            medio = MedioVerificacion()
            medio.medio_user = request.user
        else:
            medio = MedioVerificacion.objects.get(id=medio_id)

        if action != 'delete':
            medio.medio_description = request.POST.get('medio_description', '')
            medio.save()
        else:
            actividades = Actividad.objects.filter(actividad_medio=medio)
            if actividades.count() == 0:
                medio.delete()
            else:
                messages.error(request, F"El responsable está medio utilizado en una actividad")

        return redirect("indicadores_list")


class ResponsablesList(View):
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    # noinspection PyMethodMayBeStatic
    def get(self, request):
        search = request.GET.get('search', '')
        user = request.user
        responsables_list = Responsable.objects.filter(responsable_user=user, responsable_description__icontains=search)
        return render(request, "responsables_list.html", {"responsables_list": responsables_list})

    # noinspection PyMethodMayBeStatic
    def post(self, request, *args, **kwargs):
        action = request.POST.get('action', '')
        responsable_id = request.POST.get('id', '')

        if action == 'new':
            responsable = Responsable()
            responsable.responsable_user = request.user
        else:
            responsable = Responsable.objects.get(id=responsable_id)

        if action != 'delete':
            responsable.responsable_description = request.POST.get('responsable_description', '')
            responsable.save()
        else:
            actividades = Actividad.objects.filter(actividad_responsable=responsable)
            if actividades.count() == 0:
                responsable.delete()
            else:
                messages.error(request, F"El responsable está siendo utilizado en una actividad")

        return redirect("responsables_list")


class ParametrosList(View):
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    # noinspection PyMethodMayBeStatic
    def get(self, request):
        search = request.GET.get('search', '')
        parametros_list = Parametro.objects.filter(parametro_name__icontains=search)
        return render(request, "parametros_list.html", {"parametros_list": parametros_list})

    # noinspection PyMethodMayBeStatic
    def post(self, request, *args, **kwargs):
        action = request.POST.get('action', '')
        parametro_id = request.POST.get('id', '')

        if action == 'new':
            parametro = Parametro()
        else:
            parametro = Parametro.objects.get(id=parametro_id)

        if action != 'delete':
            parametro.parametro_name = request.POST.get('parametro_name', '').upper().strip()
            parametro.parametro_value = request.POST.get('parametro_value', '').strip()
            parametro.save()
        else:
            parametro.delete()

        return redirect("parametros_list")


class NotificacionesList(View):
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    # noinspection PyMethodMayBeStatic
    def get(self, request):
        search = request.GET.get('search', '')
        notificaciones_list = NotificationsSearchList(request.user, search)
        return render(request, "notificaciones_list.html", {"notificaciones_list": notificaciones_list})

    # noinspection PyMethodMayBeStatic
    def post(self, request, *args, **kwargs):
        action = request.POST.get('action', '')
        notificacion_id = request.POST.get('id', '')
        if action == 'read':
            NotificationMark(notificacion_id, True)
        else:
            NotificationMark(notificacion_id, False)

        return redirect("notificaciones_list")


class LogsList(View):
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    # noinspection PyMethodMayBeStatic
    def get(self, request):
        search = request.GET.get('search', '')
        logs_list = Log.objects.filter(Q(log_description__icontains=search) |
                                       Q(log_username__icontains=search) |
                                       Q(log_poaname__icontains=search))
        return render(request, "logs_list.html", {"logs_list": logs_list})


class TablerosList(View):
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    # noinspection PyMethodMayBeStatic
    def get(self, request):
        search = request.GET.get('search', '')
        tableros_list = Tableau.objects.filter(tableau_description__icontains=search)
        tableros_annos = list(range(2022, datetime.datetime.now().year + 1))
        tableros_annos.sort(reverse=True)
        return render(request, "tableros_list.html", {"tableros_list": tableros_list, "tableros_annos": tableros_annos})

    # noinspection PyMethodMayBeStatic
    def post(self, request, *args, **kwargs):
        action = request.POST.get('action', '')
        tableau_id = request.POST.get('id', '')

        if action == 'new':
            tableau = Tableau()
        else:
            tableau = Tableau.objects.get(id=tableau_id)

        if action != 'delete':
            tableau.tableau_anno = request.POST.get('tableau_anno', '').strip()
            tableau.tableau_title = request.POST.get('tableau_title', '').strip()
            tableau.tableau_url = request.POST.get('tableau_url', '').strip()
            tableau.tableau_description = request.POST.get('tableau_description', '').strip()
            tableau.save()
        else:
            tableau.delete()

        return redirect("tableros_list")


def GetRoots(estamento_id, root_list):
    if estamento_id == 1:
        root_list += '1'
        return root_list

    root_list += f'{estamento_id},'
    estamento = Estamento.objects.get(id=estamento_id)
    estamento_sub_id = estamento.estamento_sub_id
    return GetRoots(estamento_sub_id, root_list)


def GetAllRoots():
    estamentos = Estamento.objects.filter(id__gt=1).order_by('estamento_sub_id')
    for estamento in estamentos:
        estamento.estamento_roots = GetRoots(estamento.estamento_sub_id, '')
        estamento.save()


def Test(request):
    value = "http://" + request.META['HTTP_HOST']
    return HttpResponse('Result: ' + value)
