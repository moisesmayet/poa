
// Mostrar modal para mensajes
function showModal(message) {
    var messageModalDiv = $('body').find('#message_modal');
    if (messageModalDiv.length > 0) {
        messageModalDiv.text(message);
        $('#error_modal').modal('show');
    }
}

// Ocultar y mostrar en los modals
function ShowAndHide(section_name) {
    var section_view = document.getElementById(section_name + '_view');
    var section_hide = document.getElementById(section_name + '_edit');

    if (section_view.style.display === 'none') {
        section_view.style.display = 'block';
        section_hide.style.display = 'none';
    } else {
        section_view.style.display = 'none';
        section_hide.style.display = 'block';
    }
}

// Ocultar y mostrar tarjetas cuando son seleccionadas
function SelectShowAndHide(section_name) {
    try {
        var radioIdPrefix = "select_" + section_name;
        var checkedRadio = document.querySelector(`input[type="radio"][id="${radioIdPrefix}"]:checked`);
        var radioId = localStorage.getItem(checkedRadio.name);
        if (radioId != checkedRadio.id) {
            localStorage.setItem(checkedRadio.name, checkedRadio.id);

            var url_parts = section_name.split('_');
            var url = `/poa_edit_update/${url_parts[url_parts.length - 2]}/${url_parts[url_parts.length - 1]}`;
            $.post(url)
            .done(function(response) {
                if (response.success) {
                    var lastUnderscoreIndex = section_name.lastIndexOf('_');
                    var section_hide = section_name.substring(0, lastUnderscoreIndex + 1);
                    var hideIdPrefix = "add_" + section_name;
                    var showIdPrefix = "add_" + section_hide;
                    var portlet_hide = document.querySelector(`div[id="${hideIdPrefix}"]`);
                    var portlet_show = document.querySelector(`div[id^="${showIdPrefix}"][style*="display: none"]`);
                    portlet_hide.style.display = "none";
                    portlet_show.style.display = "block";

                    hideSections(section_hide);
                    showSections(section_name + '_')
                    var nodeCheckedRadio = document.querySelector(`input[type="radio"][id^="${radioIdPrefix}_"]:checked`);
                    if (nodeCheckedRadio) {
                        showSections(nodeCheckedRadio.value + '_');
                    }

                    var add_actividad_button = document.querySelector(`div[id="modal_add_actividad_button"]`);
                    if (response.exists_metas) {
                        add_actividad_button.style.display = "block";
                    } else {
                        add_actividad_button.style.display = "none";
                    }
                } else {
                    showModal("Error al actualizar meta_selected");
                }
            })
            .fail(function() {
                showModal("Error en la solicitud AJAX");
            });
        }
    } catch (error) {
        showModal("Ocurrió un error, por favor refrescar la página");
    }
}

function hideSections(section_name) {
    try {
        var sectionsToHide = document.querySelectorAll(`div[id^="${section_name}"]`);
        sectionsToHide.forEach(function(section) {
            var sectionNumber = section.id.replace(section_name, '');
            if (isNaN(sectionNumber)) {
                section.style.display = "none";
            }
        });
    } catch (error) {
        showModal("Ocurrió un error, por favor refrescar la página");
    }
}

function showSections(section_name) {
    try {
        var sectionsToShow = document.querySelectorAll(`div[id^="${section_name}"]`);
        sectionsToShow.forEach(function(section) {
            var sectionNumber = section.id.replace(section_name, '');
            var segments = sectionNumber.split('_');
            if (segments.length === 2 && !isNaN(segments[1])) {
                section.style.display = "block";
            }
        });
    } catch (error) {
        showModal("Ocurrió un error, por favor refrescar la página");
    }
}

$(function() {
    function handleUpdate(event, ui, columnType, orderElementPrefix) {
        try {
            var visibleItems = ui.item.parent().children(':visible');
            var newPosition = visibleItems.index(ui.item) + 1;
            var draggedItem = ui.item.attr("id");
            var targetColumn = ui.item.parent().attr("id");
            var estamento_id = ui.item.data(`${columnType}-estamento-id`);
            var poa_anno = ui.item.data(`${columnType}-poa-anno`);
            var order_update = `/poa_edit/${estamento_id}/${poa_anno}`;

            if (targetColumn.startsWith("add_")) {
                var totalDivId = $(`#${targetColumn}`).find(`[id^="total_"]`).attr('id');
                var totalLastUnderscoreIndex = totalDivId.lastIndexOf('_');
                if (totalLastUnderscoreIndex !== -1) {
                    newPosition = parseInt(totalDivId.substring(totalLastUnderscoreIndex + 1)) || 0;
                }
                $(`#${draggedItem}`).remove();
            }

            $.post(order_update, { dragged_item: draggedItem, target_column: targetColumn, new_position: newPosition, action: "order" }, function(response) {
                if (response.updated_values && response.updated_values.length > 0) {
                    $.each(response.updated_values, function(index, updatedValue) {
                        $(`span[id^="${orderElementPrefix}"]`).each(function() {
                            if ($(this).attr('id') === orderElementPrefix + updatedValue.id) {
                                $(this).text(updatedValue.value);
                            }
                        });
                    });
                } else {
                    location.reload();
                }
            });
        } catch (error) {
            showModal("Ocurrió un error, por favor refrescar la página");
        }
    }

    // Configuración para la columna de objetivos
    $(".column-objetivo").sortable({
        connectWith: ".column-objetivo",
        handle: ".portlet-header",
        cancel: ".portlet-toggle",
        placeholder: {
            element: function(currentItem) {
                return $("<div class='portlet-placeholder ui-corner-all'></div>").height(currentItem.innerHeight()).css({'border': 'none !important'});
            },
            update: function(container, p) {
                return;
            }
        },
        update: function(event, ui) {
            handleUpdate(event, ui, 'objetivo', 'objetivo_order_');
            $("#addMeta").empty();
        }
    });

    // Configuración para la columna de metas
    $(".column-meta").sortable({
        connectWith: ".column-meta",
        handle: ".portlet-header",
        cancel: ".portlet-toggle",
        placeholder: {
            element: function(currentItem) {
                return $("<div class='portlet-placeholder ui-corner-all'></div>").height(currentItem.innerHeight()).css({'border': 'none !important'});
            },
            update: function(container, p) {
                return;
            }
        },
        update: function(event, ui) {
            handleUpdate(event, ui, 'meta', 'meta_order_');
            $("#addActividad").empty();
        }
    });

    // Configuración para la columna de actividades
    $(".column-actividad").sortable({
        connectWith: ".column-actividad",
        handle: ".portlet-header",
        cancel: ".portlet-toggle",
        placeholder: {
            element: function(currentItem) {
                return $("<div class='portlet-placeholder ui-corner-all'></div>").height(currentItem.innerHeight()).css({'border': 'none !important'});
            },
            update: function(container, p) {
                return;
            }
        },
        update: function(event, ui) {
            handleUpdate(event, ui, 'actividad', 'actividad_order_');
        }
    });

    // Configuración para la columna de planificadas
    $(".column-planificada").sortable({
        connectWith: ".column-planificada",
        handle: ".portlet-header",
        cancel: ".portlet-toggle",
        placeholder: {
            element: function(currentItem) {
                return $("<div class='portlet-placeholder ui-corner-all'></div>").height(currentItem.innerHeight()).css({'border': 'none !important'});
            },
            update: function(container, p) {
                return;
            }
        },
        update: function(event, ui) {
            handleUpdate(event, ui, 'planificada', 'planificada_order_');
        }
    });

    // Configuración para la columna de realizadas
    $(".column-realizada").sortable({
        connectWith: ".column-realizada",
        handle: ".portlet-header",
        cancel: ".portlet-toggle",
        placeholder: {
            element: function(currentItem) {
                return $("<div class='portlet-placeholder ui-corner-all'></div>").height(currentItem.innerHeight()).css({'border': 'none !important'});
            },
            update: function(container, p) {
                return;
            }
        },
        update: function(event, ui) {
            handleUpdate(event, ui, 'realizada', 'realizada_order_');
        }
    });

    $(".portlet")
        .addClass("ui-widget ui-widget-content ui-helper-clearfix ui-corner-all")
        .find(".portlet-header")
        .addClass("ui-widget-header ui-corner-all");

    $(".portlet-toggle").click(function() {
        var icon = $(this);
        icon.toggleClass("ui-icon-minusthick ui-icon-plusthick");
        icon.closest(".portlet").find(".portlet-content").toggle();
    });
});

function createIcon(evidencia_uploaded, evidencia_del_view, evidencia_icon, evidencia_name) {
    var ico = '<img src="' + evidencia_icon + '" style="height: 25px; margin-left: 80px;">'
    evidencia_uploaded.html(ico);
    evidencia_uploaded.show();
    evidencia_del_view.html(ico+'<span>'+evidencia_name+'</span>');
    evidencia_del_view.show();
}

function UpdateColaboradores(estamentoId, colaboradorIds) {
    var modal = document.getElementById('modal_colaboradores_' + estamentoId);
    $(modal).modal('hide');
    $.ajax({
        url: '/update_colaborador',
        method: 'POST',
        data: { colaborador_ids: colaboradorIds, estamento_id: estamentoId },
        success: function(response) {
            console.log('Usuarios actualizados:', response);
        },
        error: function(xhr, status, error) {
            console.error('Error al actualizar colaborador:', error);
        }
    });
}

$(document).ready(function() {
    // Poner el scrollbar al final del modal de notas
    $('[id^="modal_form_nota_poa_"]').on('shown.bs.modal', function () {
        var modalId = $(this).attr('id');
        var containerId = 'container_' + modalId;
        var notasContainer = $('#' + containerId);
        notasContainer.scrollTop(notasContainer[0].scrollHeight);
    });

    // mostrar cuadro notificaciones
    document.addEventListener('click', function(event) {
        var dropdownMenu = document.getElementById('dropdown-menu');
        var dropdownTrigger = document.getElementById('dropdown-trigger');
        if (!dropdownMenu.contains(event.target) && !dropdownTrigger.contains(event.target)) {
            dropdownMenu.classList.remove('show');
            dropdownMenu.classList.remove('active');
        }
    });

    document.getElementById('dropdown-trigger').addEventListener('click', function() {
        var dropdownMenu = document.getElementById('dropdown-menu');
        dropdownMenu.classList.toggle('show');
        dropdownMenu.classList.toggle('active');
        dropdownMenu.style = "position: absolute; transform: translate3d(-149px, 50px, 0px); top: 0px; left: 0px; will-change: transform;";
    });

    $('[id^="modal_colaboradores_"]').on('shown.bs.modal', function() {
        var selectDiv = $('.dropdown.bootstrap-select.show-tick.form-control');
        if (selectDiv.find('li').length === 0) {
            $('.btn.dropdown-toggle.btn-light').click();
            var dataId = $('.btn.dropdown-toggle.btn-light').data('id');
            $('#'+dataId).blur();
        }
    });

    // procesar formularios ajax
    $('.ajax-form').on('submit', function(e) {
        e.preventDefault();
        var $form = $(this);
        var formId = $form.attr('id');
        if (formId.startsWith('form_modal_colaboradores_')) {
            UpdateColaboradores($('#'+formId+'_id').val(), $('#'+formId+'_select').val());
        }
        else {
            if (formId.startsWith('section_objetivo_')) {
                Loading(formId, ' el objetivo');
            } else if (formId.startsWith('section_meta_')) {
                Loading(formId, ' la meta');
            } else if (formId.startsWith('section_actividad_')) {
                Loading(formId, ' la actividad');
            }
            else {
                var cronograma_id = $form.find('#id').val();
                var event_action = $form.find('#action').val();
                var modal = document.getElementById('modal_edit_' + cronograma_id + '_' + event_action);
                $(modal).modal('hide');
            }
            $.ajax({
                url: $form.attr('action'),
                type: $form.attr('method'),
                data: new FormData($form[0]),
                processData: false,
                contentType: false,
                success: function(response) {
                    if (response.success) {
                        var cronograma_id = response.cronograma_id;
                        var evidencia_uploaded = $('#file-upload-image-saved-' + cronograma_id);

                        switch (response.event_action) {
                            case "eliminar":
                                $('#cronograma-evidencia-' + cronograma_id).hide();
                                $('#cronograma-iconos-eliminar-' + cronograma_id).hide();
                                evidencia_uploaded.empty()
                                break;
                            case "evidencia":
                                $('#cronograma-evidencia-' + cronograma_id).show();
                                $('#cronograma-iconos-eliminar-' + cronograma_id).show();
                                if (response.evidencia_preview) {
                                    $('#cronograma-evidencia-modal-' + cronograma_id).show();
                                    $('#cronograma-evidencia-download-' + cronograma_id).hide();
                                    $('#cronograma-evidencia-imagen-' + cronograma_id).attr('src', response.evidencia_icon);
                                    $('#cronograma-evidencia-view-download-' + cronograma_id).attr('href', response.evidencia_url).attr('download', response.evidencia_name);
                                    var evidencia_view = $('#cronograma-evidencia-view-' + cronograma_id);
                                    var evidencia_del_view = $('#cronograma-evidencia-eliminar-' + cronograma_id);
                                    evidencia_uploaded.empty();
                                    evidencia_view.show();
                                    evidencia_view.empty();
                                    evidencia_del_view.show();
                                    evidencia_del_view.empty();

                                    if (response.evidencia_type !== 'image') {
                                        createIcon(evidencia_uploaded, evidencia_del_view, response.evidencia_icon, response.evidencia_name);
                                    }

                                    switch (response.evidencia_type) {
                                        case 'image':
                                            var img = '<img src="' + response.evidencia_url + '" class="file-upload-image-saved" style="max-height: 200px; max-width: 200px; margin: auto; padding-bottom: 5px;">';
                                            evidencia_view.html(img)
                                            evidencia_del_view.html(img);
                                            break;
                                        case 'pdf':
                                            var embed = '<embed src="' + response.evidencia_url + '" frameborder="0" width="100%" height="400px">';
                                            evidencia_view.html(embed);
                                            break;
                                        case 'office':
                                            var iframe = '<iframe src="https://view.officeapps.live.com/op/embed.aspx?src=' + response.evidencia_url + '" width="100%" height="100%" frameborder="0"></iframe>';
                                            evidencia_view.html(iframe);
                                            break;
                                        case 'video':
                                            var video = '<video src="' + response.evidencia_url + '" width="100%" height="100%"></video>';
                                            var mensaje = "Lo sentimos. Este vídeo no puede reproducirse en este navegador.<br>Puedes descargar el video si deseas abrirlo localmente";
                                            video.html(mensaje);
                                            evidencia_view.html(video);
                                            break;
                                        default:
                                            evidencia_view.hide();
                                            break;
                                    }
                                } else {
                                    $('#cronograma-evidencia-modal-' + cronograma_id).hide();
                                    $('#cronograma-evidencia-download-' + cronograma_id).html(`<a href="${response.evidencia_url}" download="${response.evidencia_name}" style="padding: 0px; !important;"><img src="${response.evidencia_icon}" style="height: 18px; padding-bottom: 2px;"></a>`).show();
                                }
                                break;
                            case "presupuesto":
                                var cronograma_presupuesto = '0'
                                if (response.cronograma_presupuesto > 0) {
                                    cronograma_presupuesto = "RD$" + response.cronograma_presupuesto.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
                                }
                                $('#cronograma-presupuesto-' + cronograma_id).text(cronograma_presupuesto);
                                break;
                            case "notas":
                                break;
                        }
                    }
                    else {
                        location.reload();
                    }
                },
                error: function(xhr, status, error) {
                    showModal('Error al enviar el formulario');
                }
            });
        }
    });
});

//Actualizar cronograma
function CronogramaUpdate(cronograma_id) {
    try {
        var url = `/poa_cronograma_update/${cronograma_id}`;
        $.post(url)
            .done(function(response) {
                if (response.success) {
                    var check = document.getElementById("cronograma-check-" + cronograma_id);
                    var iconos = document.getElementById("cronograma-iconos-" + cronograma_id);
                    var icono_eliminar = document.getElementById("cronograma-iconos-eliminar-" + cronograma_id);
                    var icono_evidencia = document.getElementById("cronograma-evidencia-" + cronograma_id);
                    var defasada = document.getElementById("cronograma-defasada-" + cronograma_id);
                    var newdefasada = document.getElementById("cronograma-newdefasada-" + cronograma_id);
                    //var cronogramaRow = document.getElementById("cronograma-row-" + cronograma_id);

                    var currentMonth = new Date().getMonth() + 1;

                    if (response.cronograma_cumplimiento) {
                        $('#cronograma-card-planificada-' + cronograma_id).hide();
                        $('#cronograma-card-realizada-' + cronograma_id).show();
                        iconos.style.display = 'block';
                        if (check) {
                            check.classList.remove("fa-square");
                            check.classList.add("fa-check-square");
                        }

                        if (response.has_evidencia) {
                            icono_evidencia.style.display = 'block';
                            icono_eliminar.style.display = 'block';
                        }

                        if (response.cronograma_defasado) {
                            newdefasada.style.display = 'block';
                            //if (cronogramaRow != null) {
                                //cronogramaRow.style.backgroundColor = "#DFB7D6";
                            //}
                        //} else {
                            //cronogramaRow.style.backgroundColor = "#B5D9C8";
                        }
                    } else {
                        $('#cronograma-card-planificada-' + cronograma_id).show();
                        $('#cronograma-card-realizada-' + cronograma_id).hide();
                        iconos.style.display = 'none';
                        icono_eliminar.style.display = 'none';
                        icono_evidencia.style.display = 'none';
                        if (defasada) {
                            defasada.style.display = 'none';
                        }
                        newdefasada.style.display = 'none';
                        if (check) {
                            check.classList.remove("fa-check-square");
                            check.classList.add("fa-square");
                        }

                        //if (mes_id < currentMonth) {
                            //cronogramaRow.style.backgroundColor = "#F8D7DA";
                        //} else {
                            //cronogramaRow.style.backgroundColor = "#ADD8E6";
                        //}
                    }
                } else {
                    showModal("Error al actualizar");
                }
            })
    } catch (error) {
        showModal("Ocurrió un error, por favor refrescar la página");
    }
}

// Cargar presupuestos en modal cronogrmama actividades realizadas
function presupuestoModal(formId, cronogramaId) {
    $.ajax({
        url: '/cronograma_presupuesto',
        method: 'GET',
        data: {
            cronograma_id: cronogramaId
        },
        success: function(response) {
            const span = document.getElementById(formId + '_valor');
            if (span) {
                span.textContent = response.cronograma_presupuesto;
                if (response.es_negativo) {
                    span.classList.add('text-danger');
                }
            }
        },
        error: function(xhr, status, error) {
            console.error(error);
        }
    });
}

// Procesar los formularios desde un popover
function popoverModal(formId, poaId, notaItemid, notaItemname) {
    $.ajax({
        url: '/popover_notas',
        method: 'GET',
        data: {
            poa_id: poaId,
            nota_itemid: notaItemid,
            nota_itemname: notaItemname
        },
        success: function(notas_list) {
            if (notas_list.length > 0) {
                $('#' + notas_list[0].popover_id).empty()
                notas_list.forEach(function(notaValue) {
                    popoverAddNota(formId, notaValue);
                });
            }
        },
        error: function(xhr, status, error) {
            console.error(error);
        }
    });
}

function popoverAddNota(formId, updatedValue) {
    var updatedHtml = '<div id="' + updatedValue.popover_nota_id + '"><div clase="row"><strong>' + updatedValue.nota_user +
                        '</strong><span style="font-size: 11px;">, ' +
                        updatedValue.nota_date + '</span>';
    updatedHtml += '<a class="float-right mr-2" href="#" onclick="submitForm(&apos;' + formId + '&apos;, &apos;' + updatedValue.nota_id + '&apos;); return false;"><i class="' + updatedValue.nota_removeicon + '" title="' + updatedValue.nota_removetitle + '"></i></a>';
    updatedHtml += '</div><div>' + updatedValue.nota_description + '</div></div>';
    $('#' + updatedValue.popover_id).append(updatedHtml);
}

function poaAddNota(modalId, nota_id, nota_user, nota_date, nota_description, nota_order) {
    var containerId = 'container_' + modalId;
    var containerNotaId = containerId + '_' + nota_id;
    var contenidoHtml = `
        <div id="${containerNotaId}">
            <div>
                <strong>${nota_user}</strong>
                <span style="font-size: 11px;">, ${nota_date} <strong>${nota_order}</strong></span>
            </div>
            <div>${nota_description}</div>
        </div>
    `;
    containerId = '#' + containerId;
    $(containerId).append(contenidoHtml);
    $(containerId).scrollTop($(containerId)[0].scrollHeight);
}

function submitForm(formId, actionId) {
    var formData = $('#' + formId).serializeArray();
    formData.push({name: 'nota_id', value: actionId});
    formData = $.param(formData);
    $.ajax({
        url: $('#' + formId).attr('action'),
        type: 'POST',
        data: formData,
        success: function(data) {
            var updatedValue = data.updatedValue;
            if (updatedValue !== undefined && updatedValue !== null) {
                if (updatedValue.action === 'save') {
                    popoverAddNota(formId, updatedValue);
                    $('#' + formId).find('textarea').val('');
                    poaAddNota('modal_form_nota_poa_' + updatedValue.nota_poa, updatedValue.nota_id, updatedValue.nota_user, updatedValue.nota_date, updatedValue.nota_description, updatedValue.nota_order);
                } else {
                    $('#' + updatedValue.popover_nota_id).remove();
                    if (updatedValue.nota_remove) {
                        $('#container_modal_form_nota_poa_' + updatedValue.nota_poa + '_' + updatedValue.nota_id).remove();
                    }
                }
                $('#color_' + formId).css('background-color', updatedValue.color);
            } else {
                // Agregar notas al POA
                var modalId = 'modal_' + formId;
                poaAddNota(modalId, data.nota_id, data.nota_user, data.nota_date, data.nota_description, '');
                $('#'+formId+'_nota textarea').val('');
                $('#'+modalId).modal('hide');
            }
        },
        error: function(xhr, status, error) {
            showModal('Error al enviar el formulario');
        }
    });
}


function SendMessage(menu_estamento_id) {
    var form = $('#modal_message_' + menu_estamento_id + ' form');
    $('#modal_message_' + menu_estamento_id).modal('hide');
    $.post(form.attr('action'), form.serialize())
        .done(function(response) {
            if (response.success) {
                $('#notificacion_message_' + response.menu_estamento_id + ' textarea[name="notificacion_message"]').val('');
                console.log("Mensaje enviado");
            } else {
                showModal("Error al enviar el mensaje");
            }
        })
        .fail(function() {
            showModal("Ocurrió un error al enviar el mensaje");
        });
}


function clickShowAndHide(showId, hideId) {
    var showElement = document.getElementById(showId);
    var hideElement = document.getElementById(hideId);

    showElement.style.display = 'block';
    hideElement.style.display = 'none';
}

function filterShowAndHide() {
    // Filtrar por mes
    var filtroMes = document.getElementById('filtro_mes').value;
    if (filtroMes === "cronograma_mes_todas") {
        filterShowDivs('filtro_mes_')
    }
	else {
		var numeroMes = "";

		switch (filtroMes) {
			case "cronograma_mes_anterior":
				numeroMes = new Date().getMonth();
				break;
			case "cronograma_mes_actual":
				numeroMes = new Date().getMonth() + 1;
				break;
			case "cronograma_mes_siguiente":
				numeroMes = new Date().getMonth() + 2;
				break;
			default:
				numeroMes = filtroMes.split("_")[2];
				break;
		}

        filterShowAndHideDivs('filtro_mes_', numeroMes)
	}

    // Filtrar por estado
    var filtroEstado = document.getElementById('filtro_estado').value;
    if (filtroEstado === "cronograma_estado_todas") {
        filterShowDivs('filtro_estado_')
    }
    else {
        var estadoId = filtroEstado.split("_")[2];
        filterShowAndHideDivs('filtro_estado_', estadoId)
    }

    // Filtrar por meta
    var filtroMeta = document.getElementById('filtro_meta').value;
    if (filtroMeta === "cronograma_meta_todas") {
        filterShowDivs('filtro_meta_')
    }
    else {
        var metaId = filtroMeta.split("_")[2];
        filterShowAndHideDivs('filtro_meta_', metaId)
    }
}


function filterShowDivs(section_name) {
    // Mostrar todos los divs
    var divsShow = document.querySelectorAll("[id^='" + section_name + "']");
    divsShow.forEach(function(div) {
        div.style.display = "block";
    });
}

function filterShowAndHideDivs(section_name, section_id) {
    // Ocultar todos los divs que comienzan con section_name
    var divsHide = document.querySelectorAll("[id^='" + section_name + "']");
    divsHide.forEach(function(div) {
        div.style.display = "none";
    });

    // Mostrar todos los divs que comienzan con section_name y que contienen section_id en su valor
    var divsShow = document.querySelectorAll("[id='" + section_name + section_id + "']");
    divsShow.forEach(function(div) {
        div.style.display = "block";
    });
}


function RefreshNotifications() {
    $.ajax({
        url: '/refresh_notifications',
        type: 'GET',
        success: function(response) {
            var contadorNotificaciones = response.notifications_number;

            if (contadorNotificaciones > 0) {
                $('#notificaciones-marcar-leidas a').show();
                $('#notificaciones-number').show();
                $('#notificaciones-number .number').text(contadorNotificaciones);
            } else {
                $('#notificaciones-marcar-leidas a').hide();
                $('#notificaciones-number').hide();
            }

            var listaNotificaciones = $('#notificaciones_list ul.custom-notifications');
            listaNotificaciones.empty();

            if (contadorNotificaciones > 0) {
                response.notifications.forEach(function(notification) {
                    listaNotificaciones.show();
                    var li = '<li id="notificacion_li_' + notification.id + '" class="unread">' +
                                '<span class="d-flex">' +
                                    '<div class="w-100">' +
                                        '<div class="text-right">' +
                                            '<a href="#" id="notificacion_leer_' + notification.id + '" onclick="NotificationMark(' + notification.id + ', true)"><i class="fas fa-times" title="Marcar como leída"></i></a>' +
                                        '</div>' +
                                        '<div id="notificacion_' + notification.id + '" class="text">' +
                                            '<strong>' + notification.notificacion_username + '</strong>&nbsp;&nbsp;' + notification.notificacion_message +
                                        '</div>' +
                                    '<div>' +
                                '</span>' +
                             '</li>';
                    listaNotificaciones.append(li);
                });
            } else {
                listaNotificaciones.hide();
                $('.custom-notifications p').hide();
            }
        },
        error: function(xhr, status, error) {
            console.error('Error al actualizar las notificaciones:', error);
        }
    });
}


// marcar como leidas las notificaciones
function NotificationMark(notificationId, notificationReaded) {
    $.ajax({
            url: '/mark_notifications',
            method: 'POST',
            data: { notificacion_id: notificationId, notificacion_readed: notificationReaded },
            success: function(response) {
                if (response.success) {
                    var listaNotificaciones = $('#notificaciones_list ul.custom-notifications');
                    if (response.notification_read) {
                        if (response.notifications_number > 0) {
                            listaNotificaciones.show();
                            $('#notificaciones-marcar-leidas a').show();
                            $('#notificaciones-number').show();
                            $('#notificaciones-number .number').text(response.notifications_number);
                            var li = document.getElementById('notificacion_li_' + response.notification_id);
                            if (li) {
                                li.remove();
                            }
                            $('#notification_mark_'+response.notification_id).attr('onclick', 'NotificationMark('+response.notification_id+', '+!response.notification_read+')');
                            $('#notification_icon_'+response.notification_id).removeClass('fa-envelope').addClass('fa-envelope-open');
                        } else {
                            listaNotificaciones.hide();
                            $('#notificaciones-marcar-leidas a').hide();
                            $('#notificaciones-number').hide();
                            var lis = document.querySelectorAll('li[id^="notificacion_li_"]');
                            lis.forEach(function(li) {
                                li.remove();
                            });

                            $('[id^="notification_mark_"]').each(function() {
                                var notification_id = $(this).attr('id').split('_').pop();
                                $(this).attr('onclick', 'NotificationMark('+notification_id+', '+!response.notification_read+')');
                            });
                            $('[id^="notification_icon_"]').each(function() {
                                $(this).removeClass('fa-envelope').addClass('fa-envelope-open');
                            });
                        }
                    }
                    else {
                        if (response.notification_id > 0) {
                            $('#notification_mark_'+response.notification_id).attr('onclick', 'NotificationMark('+response.notification_id+', '+!response.notification_read+')');
                            $('#notification_icon_'+response.notification_id).removeClass('fa-envelope-open').addClass('fa-envelope');
                        } else {
                            $('[id^="notification_mark_"]').each(function() {
                                var notification_id = $(this).attr('id').split('_').pop();
                                $(this).attr('onclick', 'NotificationMark('+notification_id+', '+!response.notification_read+')');
                            });
                            $('[id^="notification_icon_"]').each(function() {
                                $(this).removeClass('fa-envelope').addClass('fa-envelope');
                            });
                        }
                        RefreshNotifications()
                    }
                } else {
                    console.error('Error al marcar la notificación como leída');
                }
            },
            error: function(xhr, status, error) {
                console.error('Error marcando como leida');
            }
        });
}


// Guardando
function Loading(formId, element) {
    $('#modal_'+formId).modal('hide');
    const overlay = document.getElementById("preload-overlay");
    if (overlay) {
        var mensaje = "";
        if (formId.endsWith('_add_form')) {
            mensaje = "Creando" + element;
        } else if (formId.endsWith('_edit_form')) {
            mensaje = "Actualizando" + element;
        } else if (formId.endsWith('_del_form')) {
            mensaje = "Eliminando" + element;
        }
        overlay.style.display = "flex";
        overlay.innerHTML = `<div id="preload"></div><p>${mensaje}</p>`;
    }
}


// cargar Preload
function Preload(showMessage) {
    const overlay = document.getElementById("preload-overlay");
    if (overlay) {
        overlay.style.display = "flex";

        if (showMessage) {
            const mensajes = ["Obteniendo información...", "Leyendo la data...", "Generando la información...", "Esta acción puede tardar...", "Extrayendo estructura...", "Codificando...", "Siguiente tarea...", "Generando la información...", "Codificando la data...", "Esta acción puede tardar...", "Generando la información...", "Sincronizando...", "Generando la información...", "Descargando multimedia...", "Generando la información...", "Obteniendo presupuestos...", "Revisando presupuestos...", "Calculando porcentajes...", "Procesando porcentajes...", "Verificando información..."];
            let index = 0;

            function cambiarMensaje() {
                overlay.innerHTML = `
                  <div id="preload"></div>
                  <p>${mensajes[index]}</p>
                `;
                index = (index + 1) % mensajes.length;
            }

            const intervaloMensajes = setInterval(cambiarMensaje, 2000);
        }
        else {
            overlay.innerHTML = `<div id="preload"></div>`;
        }
    }
}


// Actualizar los radio buttons al cargar la página
document.addEventListener("DOMContentLoaded", function () {
    // Open loader
    var url = window.location.href;
    if (url.includes("poa_card") ||
        (url.includes("poa_preview")) ||
        (url.includes("poa_progreso")) ||
        (url.includes("poa_cronograma")) ||
        (url.includes("poa_correlacion")) ||
        (url.includes("poa_ejecutoria"))) {
        Preload();
    }
    RefreshNotifications();

    const selectlevel1Elements = document.querySelectorAll('select[id^="selectlevel1"]');

    selectlevel1Elements.forEach(selectlevel1 => {
        const idSuffix = selectlevel1.id.replace('selectlevel1', '');
        const selectlevel2 = document.getElementById('selectlevel2' + idSuffix);
        const selectlevel2Opts = [...selectlevel2.children];

        // Define the function to update selectlevel2
        function updateSelectLevel2(value) {
            selectlevel2.innerHTML = selectlevel2Opts.filter(
                o => value.match("\\b" + o.value + "\\b")
            ).map(o => o.outerHTML).join('');
        }

        // Add event listener for change event
        selectlevel1.addEventListener('change', (e) => {
            updateSelectLevel2(e.target.value);
        });

        // Trigger the change event on load to initialize selectlevel2
        updateSelectLevel2(selectlevel1.value);
    });

    window.onload = function() {
        var radioButtons = document.querySelectorAll('input[type="radio"]');
        radioButtons.forEach(function(radioButton) {
            radioButton.checked = false;
        });

        var spanElements = document.querySelectorAll('span[id^="radio"][id$="_True"]');
        spanElements.forEach(function(spanElement) {
            var radioButton = spanElement.querySelector('input[type="radio"]');
            if (radioButton) {
                radioButton.checked = true;
                localStorage.setItem(radioButton.name, radioButton.id);
            }
        });
    };

    // Close loader
    window.addEventListener('load', function() {
        const overlay = document.getElementById("preload-overlay");
        if (overlay) {
            overlay.style.display = "none";
        }
    });
});
