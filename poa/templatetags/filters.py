import datetime
import os
from django import template
from poa.models import ObjetivoOperativo, Meta, Actividad, Cronograma, Objetivo, Linea, POA, Evidencia, Nota
from poa.views import IsRoot, IsPOAUser, GetFormatPesos
from uapa.models import TipoEstamento, Estamento, Colaborador
from notification.models import Parametro

register = template.Library()


def MonthNewPoa():
    return int(Parametro.objects.filter(parametro_name='MES_INICIO').first().parametro_value)


@register.filter
def is_par(value):
    if value % 2 == 0:
        return True
    return False


@register.filter
def item(dictionary, key):
    return dictionary[key]


@register.filter
def inc(val):
    return int(val) + 1


@register.filter
def dec(val):
    return int(val) + 1


@register.filter
def sumar(val_1, val_2):
    return int(val_1) + int(val_2)


@register.filter
def multiplicar(val_1, val_2):
    return int(val_1) * int(val_2)


@register.filter
def get_sublist(list_org, indexs):
    indexs_arr = indexs.split(':')
    return list_org[int(indexs_arr[0]):int(indexs_arr[1])]


@register.filter
def concat(str_1, str_2):
    return str(str_1) + str(str_2)


@register.filter
def concat_linebreak(str_1, str_2):
    if str(str_1).strip() == "":
        return str(str_1) + str(str_2)
    else:
        return str(str_1) + "\n" + str(str_2)


@register.filter
def format_number(value, fmt):
    return fmt.format(value)


@register.filter
def has_poa(user):
    estamentos = Estamento.objects.filter(estamento_user=user, estamento_has_poa=True)
    if estamentos.count() > 0:
        return True
    else:
        colaboraciones = Colaborador.objects.filter(colaborador_user=user,
                                                    colaborador_estamento__estamento_has_poa=True)
        if colaboraciones.count() > 0:
            return True
        else:
            estamentos = Estamento.objects.filter(estamento_user=user)
            for estamento in estamentos:
                if is_poa_root(estamento.id):
                    return True
    return False


@register.filter
def is_poa_user(estamento_id, user):
    return IsPOAUser(estamento_id, user)


@register.filter
def is_poa_root(estamento_root_id):
    return IsRoot(estamento_root_id)


@register.filter
def clone_poa(estamento_id, poa_anno):
    current_month = datetime.date.today().month
    current_year = datetime.date.today().year
    next_year = current_year + 1
    if poa_anno == current_year or (poa_anno == next_year and current_month >= MonthNewPoa()):
        poa = POA.objects.filter(poa_estamento_id=estamento_id, poa_anno=poa_anno).first()
        if poa:
            total_objetivos = ObjetivoOperativo.objects.filter(operativo_poa=poa).count()
            if total_objetivos == 0:
                return True
        else:
            return True
    return False


@register.filter
def has_editing_poa(user):
    estamentos = Estamento.objects.filter(estamento_user=user)
    for estamento in estamentos:
        anno = datetime.date.today().year
        poas = POA.objects.filter(poa_estamento=estamento, poa_anno=anno)
        if poas.count() > 0:
            return True
    return False


@register.filter
def cronograma_atrasado(year, month):
    current_year = datetime.date.today().year
    current_month = datetime.date.today().month
    if year < current_year:
        return True
    else:
        if year == current_year and month < current_month:
            return True
    return False


@register.filter
def format_pesos(amount):
    try:
        amount_float = float(amount)
        return GetFormatPesos(amount_float)
    except ValueError:
        return "RD$ 0"


@register.filter
def format_pesos_input(amount):
    if amount != '':
        try:
            amount_float = float(amount)
            return "{:,.0f}".format(amount_float)
        except ValueError:
            return "0"
    else:
        return "0"


@register.filter
def format_int(value):
    return int(value)


@register.filter
def get_tipos_estamentos(tipos_estamentos_list):
    return TipoEstamento.objects.all()


@register.filter
def get_estamentos(estamentos_list, estamento_root_id):
    return Estamento.objects.filter(estamento_sub_id=estamento_root_id)


@register.filter
def get_objetivos(objetivos_list, eje_id):
    return Objetivo.objects.filter(objetivo_eje_id=eje_id)


@register.filter
def get_lineas(lineas_list, objetivo_id):
    return Linea.objects.filter(linea_objetivo_id=objetivo_id)


@register.filter
def count_children_estamentos(childs, estamento_root_id):
    return Estamento.objects.filter(estamento_sub_id=estamento_root_id).count()


@register.filter
def get_estamento_id(estamento_id, user):
    if estamento_id == '' or estamento_id == 0:
        estamentos_list = Estamento.objects.filter(estamento_user=user, estamento_has_poa=True)
        if estamentos_list.count() > 0:
            estamento_id = FisrtEstamentoList(estamentos_list)
        else:
            colaborador = Colaborador.objects.filter(colaborador_user=user,
                                                     colaborador_estamento__estamento_has_poa=True).first()
            if colaborador:
                estamento_id = colaborador.colaborador_estamento_id
            else:
                estamentos_list = []
                estamentos = Estamento.objects.filter(estamento_user=user)
                for estamento in estamentos:
                    if is_poa_root(estamento.id):
                        estamentos_list.append(estamento)

                if len(estamentos_list) > 0:
                    estamento_id = FisrtEstamentoList(estamentos_list)

    return estamento_id


def FisrtEstamentoList(estamentos_list):
    estamento_level_list = []
    for estamento in estamentos_list:
        level = EstamentoLevel(estamento.id)
        estamento_level_list.append({"level": level, "estamento_id": estamento.id})

    if len(estamento_level_list) > 0:
        estamento_level_list.sort(key=GetLevel)
        estamento_level = estamento_level_list[0]
        return estamento_level["estamento_id"]

    return 0


def EstamentoLevel(estamento_id):
    level = 0
    estamento = Estamento.objects.get(id=estamento_id)
    if estamento is not None:
        if estamento.estamento_sub_id is not None:
            level = EstamentoLevel(estamento.estamento_sub_id) + 1

    return level


def GetLevel(level):
    return level['level']


@register.filter
def get_poa_anno(poa_anno):
    current_month = datetime.date.today().month
    current_year = datetime.date.today().year
    next_year = current_year + 1
    if (poa_anno == '') or (poa_anno < 2022) or (poa_anno > next_year) or (
            poa_anno == next_year and current_month < MonthNewPoa()):
        poa_anno = current_year

    return poa_anno


@register.filter
def get_anno(anno):
    if (anno == '') or (anno == 0):
        anno = datetime.date.today().year

    return anno


@register.filter
def is_anno_editable(anno):
    current_year = datetime.date.today().year
    if (anno == current_year) or (anno == current_year + 1):
        return True
    return False


@register.filter
def get_evidencias(evidencias_list, evidencia_cronograma_id):
    return Evidencia.objects.filter(evidencia_cronograma_id=evidencia_cronograma_id)


@register.filter
def get_evidencia(evidencia, evidencia_cronograma_id):
    return Evidencia.objects.filter(evidencia_cronograma_id=evidencia_cronograma_id).first()


@register.filter
def count_actividades(objetivo_operativo_id):
    count = 0
    metas = Meta.objects.filter(meta_operativo_id=objetivo_operativo_id)
    for meta in metas:
        count += Actividad.objects.filter(actividad_meta=meta).count()

    return count


@register.filter
def count_lineas(linea_id):
    count = 0
    objetivos_operativos = ObjetivoOperativo.objects.filter(operativo_linea_id=linea_id)
    for objetivo_operativo in objetivos_operativos:
        count += Meta.objects.filter(meta_operativo=objetivo_operativo).count()

    return count


@register.filter
def count_objetivos(objetivo_id):
    count = 0
    lineas = Linea.objects.filter(linea_objetivo_id=objetivo_id)
    for linea in lineas:
        objetivos_operativos = ObjetivoOperativo.objects.filter(operativo_linea=linea)
        for objetivo_operativo in objetivos_operativos:
            count += Meta.objects.filter(meta_operativo=objetivo_operativo).count()

    return count


@register.filter
def get_presupuesto_disponible(presupuesto_disponible, actividad_id):
    actividad = Actividad.objects.get(id=actividad_id)
    cronogramas_terminados = Cronograma.objects.filter(cronograma_actividad=actividad, cronograma_cumplimiento=True)
    presupuesto_disponible = actividad.actividad_presupuesto
    for cronograma in cronogramas_terminados:
        presupuesto_disponible -= cronograma.cronograma_presupuesto

    return presupuesto_disponible


@register.filter
def get_evidencia_name(evidencia_name):
    return evidencia_name.replace('evidencias/', '')


@register.filter
def get_evidencia_icon(evidencia_icon, evidencia_id):
    evidencia = Evidencia.objects.get(id=evidencia_id)
    evidencia_icon = ''
    if evidencia is not None:
        extension = os.path.splitext(evidencia.evidencia_file.name)[1]
        if extension.lower() in '.jpg,.jpeg,.gif,.png,.tiff,.tif,.RAW,.bmp,.psd,.eps,.pic':
            evidencia_icon = 'images/icons/imagen.png'
        else:
            if extension.lower() in '.avi,.wmv,.asf,.mov,.flv,.rm,.rmvb,.mp4,.mkv,.mks,.3gpp,.mpg':
                evidencia_icon = 'images/icons/video.png'
            else:
                if extension.lower() in '.mp3,.wav,.cda,.midi,.mp3.ogg,.wma':
                    evidencia_icon = 'images/icons/audio.png'
                else:
                    if extension.lower() in '.doc,.docx,.docm,.dotx,.dotm,.odt ':
                        evidencia_icon = 'images/icons/word.png'
                    else:
                        if extension.lower() in '.xls,.xlsx,.xlsm,.xltx,.xltm,.xlsb,.xlam,.ods ':
                            evidencia_icon = 'images/icons/excel.png'
                        else:
                            if extension.lower() in '.ppt,.pptx,.pptm,.potx,.potm,.ppam,.ppsx,.ppsm,.sldx,.sldm,.thmx,.odp':
                                evidencia_icon = 'images/icons/ppt.png'
                            else:
                                if extension.lower() in '.zip,.gz,.gzip,.rar,.tar,.tgz,.zip,.iso':
                                    evidencia_icon = 'images/icons/rar.png'
                                else:
                                    if extension.lower() == '.pdf':
                                        evidencia_icon = 'images/icons/pdf.png'
                                    else:
                                        if extension.lower() == '.txt':
                                            evidencia_icon = 'images/icons/texto.png'
                                        else:
                                            evidencia_icon = 'images/icons/otro.png'

    return evidencia_icon


@register.filter
def is_evidencia_image(evidencia_id):
    is_image = False
    evidencia = Evidencia.objects.get(id=evidencia_id)
    if evidencia is not None:
        extension = os.path.splitext(evidencia.evidencia_file.name)[1]
        if extension.lower() in '.jpg,.jpeg,.gif,.png,.tiff,.tif,.RAW,.bmp,.psd,.eps,.pic':
            is_image = True

    return is_image


@register.filter
def is_evidencia_video(evidencia_id):
    is_video = False
    evidencia = Evidencia.objects.get(id=evidencia_id)
    if evidencia is not None:
        extension = os.path.splitext(evidencia.evidencia_file.name)[1]
        if extension.lower() in '.avi,.wmv,.asf,.mov,.flv,.rm,.rmvb,.mp4,.mkv,.mks,.3gpp,.mpg':
            is_video = True

    return is_video


@register.filter
def is_evidencia_audio(evidencia_id):
    is_audio = False
    evidencia = Evidencia.objects.get(id=evidencia_id)
    if evidencia is not None:
        extension = os.path.splitext(evidencia.evidencia_file.name)[1]
        if extension.lower() in '.mp3,.wav,.cda,.midi,.mp3.ogg,.wma':
            is_audio = True

    return is_audio


@register.filter
def is_evidencia_pdf(evidencia_id):
    is_pdf = False
    evidencia = Evidencia.objects.get(id=evidencia_id)
    if evidencia is not None:
        extension = os.path.splitext(evidencia.evidencia_file.name)[1]
        if extension.lower() == '.pdf':
            is_pdf = True

    return is_pdf


@register.filter
def is_evidencia_office(evidencia_id):
    is_office = False
    evidencia = Evidencia.objects.get(id=evidencia_id)
    if evidencia is not None:
        extension = os.path.splitext(evidencia.evidencia_file.name)[1]
        if extension.lower() in '.doc,.docx,.docm,.dotx,.dotm,.odt,.xls,.xlsx,.xlsm,.xltx,.xltm,.xlsb,.xlam,.ods,.ppt,.pptx,.pptm,.potx,.potm,.ppam,.ppsx,.ppsm,.sldx,.sldm,.thmx,.odp':
            is_office = True

    return is_office


@register.filter
def cronograma_desfasado(cronograma_id):
    mes_actual = datetime.date.today().month
    cronograma = Cronograma.objects.get(id=cronograma_id)
    if cronograma:
        if (cronograma.cronograma_mes_id != cronograma.cronograma_cumplimiento_mes_id) \
                or (
                not cronograma.cronograma_cumplimiento and cronograma.cronograma_cumplimiento_mes_id != mes_actual):
            return True
    return False


@register.filter
def exists_file(evidencia):
    if evidencia and evidencia.evidencia_file != '':
        if os.path.exists(evidencia.evidencia_file.path):
            return True
    return False


@register.filter
def get_nota_componente(nota_id):
    nota = Nota.objects.filter(id=nota_id, nota_itemid__gt=0).first()
    nota_order = ''
    if nota:
        if nota.nota_itemname == 'objetivo':
            objetivo = ObjetivoOperativo.objects.filter(id=nota.nota_itemid).first()
            if objetivo:
                nota_order = f'[objetivo {objetivo.operativo_order}] '
        elif nota.nota_itemname == 'meta':
            meta = Meta.objects.filter(id=nota.nota_itemid).first()
            if meta:
                nota_order = f'[meta {meta.meta_operativo.operativo_order}.{meta.meta_order}] '
        elif nota.nota_itemname == 'actividad':
            actividad = Actividad.objects.filter(id=nota.nota_itemid).first()
            if actividad:
                nota_order = f'[actividad {actividad.actividad_meta.meta_operativo.operativo_order}.{actividad.actividad_meta.meta_order}.{actividad.actividad_order}] '
    return nota_order
