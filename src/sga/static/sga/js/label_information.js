/*
@organization: Solvo
@license: GNU General Public License v3.0
@date: Created on 26 sept. 2018
@author: Guillermo Castro Sánchez
@email: guillermoestebancs@gmail.com
*/

// Control label information validation
var errorsValidation = $('.wizard-card form');

$(document).ready(function () {
    //Search sustance with autocomplete
    $("#substance").autocomplete({
        source: "search_autocomplete_sustance",
        //Start predicting at character #1
        minLength: 1,
        //Show important substance information and save id
        select: function (event, ui) {
            $('#substance_id').val(ui.item.value); // save selected id to hidden input
            $('#substance_id').data("name", ui.item.label); // save the selected text to hidden input
            $('#substance').val(ui.item.label); // display the selected text
            return false;
        }
    })

    // Valid substance entered
    $.validator.addMethod("validSubstance", function () {
        if ($('#substance_id').data("name") != $('#substance').val() || $('#substance_id').data("name") == 'No results') {
            return false;
        } else {
            return true;
        }
    }, "Por favor, ingrese una sustancia válida.");
    // Code for the Validator
    errorsValidation.validate({
        rules: {
            substance: {
                required: true,
                validSubstance: true,
                maxlength: 250
            },
            company_name: {
                required: true,
                maxlength: 150
            },
            company_address: {
                required: true,
                maxlength: 100
            },
            company_phone: {
                required: true,
                maxlength: 15
            },
            comercial_information: {
                maxlength: 250
            },
        }
    });
    // Save label information in JSON
    $("#Next").click(function () {
        var label_JSON = {};
        //if (hasClass(label_information, 'active')) {
            errorsValidation.validate();
            if (errorsValidation.valid() == false) {
                /*
                swal({
                    type: 'error',
                    title: 'Información incompleta',
                    text: 'Por favor, compruebe los datos solicitados.'
                })
                */
            } else {
                //Label properties
                // #1: Substance
                var substance = $('#substance').val();
                label_JSON.substance_commercial_name = substance.split(' : ')[0];
                label_JSON.substance_id =  $('#substance_id').val();
                // #2: Supplier Identification
                label_JSON.company_name = $('#company_name').val();
                var company_address = $('#company_address').val();
                label_JSON.company_address = company_address;
                label_JSON.company_phone =  $('#company_phone').val();
                // #3: Product Identification
                label_JSON.commercial_information =  $('#commercial_information').val();

                // Save label information in local storage
                var label_JSON_String = JSON.stringify(label_JSON);
                localStorage.setItem('information', label_JSON_String);
                $('#loadingMessage').modal("show");
            }
        //}
    });
});

function changePlaceHolder(sel) {
    sel.style.cssText = 'color: #000 !important';
}