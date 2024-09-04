import smtplib
from email.mime.text import MIMEText
from email.header import Header
from multiprocessing import Value
from django.db.models import F, Case, When, Value, CharField, Func
from django.template.loader import render_to_string
from notification.models import Notificacion, Parametro, TipoNotificacion


def SendMail(user_name, user_mail, subject, template, message, notes, firma):
    parametro = Parametro.objects.filter(parametro_name='EMAIL_HOST').first()
    host = parametro.parametro_value
    parametro = Parametro.objects.filter(parametro_name='EMAIL_PORT').first()
    port = parametro.parametro_value
    parametro = Parametro.objects.filter(parametro_name='EMAIL_HOST_USER').first()
    user = parametro.parametro_value
    parametro = Parametro.objects.filter(parametro_name='EMAIL_HOST_PASSWORD').first()
    password = parametro.parametro_value

    html_content = render_to_string(template, {
        'name': str(user_name).title(),
        'message': message,
        'notes': notes,
        'popin_url': firma
    })

    msg = MIMEText(html_content, 'html', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = user
    msg['To'] = user_mail

    server = smtplib.SMTP(host, port)
    server.starttls()
    server.login(user, password)
    server.sendmail(user, user_mail, msg.as_string())
    server.quit()


def SendNotification(notificacion_from, notificacion_user, tipo_code, notificacion_message):
    if notificacion_message != '' and notificacion_from != notificacion_user:
        notificacion = Notificacion()
        notificacion.notificacion_message = notificacion_message
        notificacion.notificacion_user = notificacion_user
        if notificacion_from:
            notificacion.notificacion_from = notificacion_from
        notificacion.notificacion_type = TipoNotificacion.objects.filter(tipo_code=tipo_code).first()
        notificacion.save()


def NotificationsList(notificacion_user):
    notificaciones = Notificacion.objects.filter(
        notificacion_user=notificacion_user
    ).annotate(
        notificacion_username=Case(
            When(notificacion_type__tipo_code__in=['msg', 'ntf'],
                 then=F('notificacion_from__username')),
            default=Value('PopIn'),
            output_field=CharField()
        ),
        notificacion_icon=Case(
            When(notificacion_read=True, then=Value('fas fa-envelope-open')),
            default=Value('fas fa-envelope'),
            output_field=CharField()
        ),
        notificacion_open=Case(
            When(notificacion_read=True, then=Value('false')),
            default=Value('true'),
            output_field=CharField()
        )
    ).annotate(
        notificacion_username=Func(F('notificacion_username'), function='initcap')
    ).values(
        'id',
        'notificacion_message',
        'notificacion_username',
        'notificacion_discharge',
        'notificacion_read',
        'notificacion_open',
        'notificacion_icon'
    )

    return list(notificaciones)


def NotificationsSearchList(notificacion_user, search):
    notificaciones = Notificacion.objects.filter(
        notificacion_user=notificacion_user, notificacion_message__icontains=search
    ).annotate(
        notificacion_username=Case(
            When(notificacion_type__tipo_code__in=['msg', 'ntf'],
                 then=F('notificacion_from__username')),
            default=Value('PopIn'),
            output_field=CharField()
        ),
        notificacion_icon=Case(
            When(notificacion_read=True, then=Value('fas fa-envelope-open')),
            default=Value('fas fa-envelope'),
            output_field=CharField()
        ),
        notificacion_open=Case(
            When(notificacion_read=True, then=Value('false')),
            default=Value('true'),
            output_field=CharField()
        )
    ).annotate(
        notificacion_username=Func(F('notificacion_username'), function='initcap')
    ).values(
        'id',
        'notificacion_message',
        'notificacion_username',
        'notificacion_discharge',
        'notificacion_read',
        'notificacion_open',
        'notificacion_icon'
    )

    return list(notificaciones)


def NotificationsUnreadList(notificacion_user):
    notificaciones = Notificacion.objects.filter(
        notificacion_user=notificacion_user,
        notificacion_read=False
    ).annotate(
        notificacion_username=Case(
            When(notificacion_type__tipo_code__in=['msg', 'ntf'],
                 then=F('notificacion_from__username')),
            default=Value('PopIn'),
            output_field=CharField()
        ),
        notificacion_icon=Case(
            When(notificacion_read=True, then=Value('fas fa-envelope-open')),
            default=Value('fas fa-envelope'),
            output_field=CharField()
        ),
        notificacion_open=Case(
            When(notificacion_read=True, then=Value('false')),
            default=Value('true'),
            output_field=CharField()
        )
    ).annotate(
        notificacion_username=Func(F('notificacion_username'), function='initcap')
    ).values(
        'id',
        'notificacion_message',
        'notificacion_username',
        'notificacion_discharge',
        'notificacion_read',
        'notificacion_open',
        'notificacion_icon'
    )

    return list(notificaciones)


def NotificationsCountList(notificacion_user, notificacion_count=5):
    notificaciones = Notificacion.objects.filter(
        notificacion_user=notificacion_user
    ).annotate(
        notificacion_username=Case(
            When(notificacion_type__tipo_code__in=['msg', 'ntf'],
                 then=F('notificacion_from__username')),
            default=Value('PopIn'),
            output_field=CharField()
        ),
        notificacion_icon=Case(
            When(notificacion_read=True, then=Value('fas fa-envelope-open')),
            default=Value('fas fa-envelope'),
            output_field=CharField()
        ),
        notificacion_open=Case(
            When(notificacion_read=True, then=Value('false')),
            default=Value('true'),
            output_field=CharField()
        )
    ).annotate(
        notificacion_username=Func(F('notificacion_username'), function='initcap')
    ).values(
        'id',
        'notificacion_message',
        'notificacion_username',
        'notificacion_discharge',
        'notificacion_read',
        'notificacion_open',
        'notificacion_icon'
    ).order_by('-notificacion_discharge')[:notificacion_count]

    return list(notificaciones)


def NotificationMarkAll(notificacion_user, notificacion_read):
    Notificacion.objects.filter(notificacion_user=notificacion_user).update(notificacion_read=notificacion_read)


def NotificationMark(notificacion_id, notificacion_read):
    notificacion = Notificacion.objects.filter(id=notificacion_id).first()
    if notificacion:
        notificacion.notificacion_read = notificacion_read
        notificacion.save()


def GetURL(request):
    if 'https' in request.META.get('HTTP_REFERER', ''):
        protocol = "https"
    else:
        protocol = "http"
    domain = f"{protocol}://{request.META['HTTP_HOST']}"
    return domain
