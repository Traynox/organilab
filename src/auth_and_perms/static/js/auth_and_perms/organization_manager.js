const Toast = Swal.mixin({
                toast: true,
                position: 'top-end',
                showConfirmButton: false,
                timer: 3000,
                timerProgressBar: true,
                didOpen: (toast) => {
                    toast.addEventListener('mouseenter', Swal.stopTimer)
                    toast.addEventListener('mouseleave', Swal.resumeTimer)
                }
             })

function organization_rol(element){
    const obj=  {
    'is_manager': element.getAttributeNames().find(e => e=="data-addbtn") != undefined,
    'element': element,
    'instance': $(element),
    'init': function(){

        if(this.is_manager){
            this.initialize_buttons();
        }else{
            this.display_rols();
        }

    },
    'display_rols': function(){
        console.log('load roles');
    },
    'initialize_buttons': function(){
         this.instance.find('.rolbtnadd').on('click', this.call_add_btn_click(this));
    },

    'get_add_form_title': function(){
        return this.element.title || "Creating Rol"
    },
    'get_add_form_html': function(){
        return document.getElementById("addrolform").innerHTML;
    },
    'get_add_form_confirmbtntext': function(){
        return this.element.getAttribute('confirmbtntext');
    },
    'add_btn_click': function(){
        const fatherobj=this;
        Swal.fire({
          title: this.get_add_form_title(),
          html: this.get_add_form_html(),
          confirmButtonText: this.get_add_form_confirmbtntext(),
          focusConfirm: false,
          preConfirm: () => {
            const rolname = Swal.getPopup().querySelector('#rolname').value

            if (!rolname) {
              Swal.showValidationMessage(  document.getElementById("addrolform").title )
            }

            return { rolname: rolname }
          }
        }).then((result) => {

          const data = {
            'name': result.value.rolname,
            'rol': fatherobj.element.getAttribute('rol')
          }

          return fetch(document.getElementById("addrolform").getAttribute('url'), {
              method: 'POST', // or 'PUT'
              headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
              },
              body: JSON.stringify(data),
            })
            }).then(results => {
              return results.json();
            })
            .then(json => {
                 windows.location.ref.reload();
            })
            .catch(err => {
              if (err) {
                swal("Oh noes!", "The AJAX request failed!", "error");
              } else {
                swal.stopLoading();
                swal.close();
              }
            });
    },
    // CALLS
    'call_add_btn_click': function(instance){
        return () => { instance.add_btn_click() };
    }
}
    obj.init();
    return obj;
}


document.addEventListener("DOMContentLoaded", function(){
    const collection = document.getElementsByClassName("rolcontainer");
    for (let i = 0; i < collection.length; i++) {
     organization_rol(collection[i]);
    }
});

$(document).ready(function(){
    $("input.checkrol").parent().addClass("checked");
});



$("input[type='checkbox']").on('ifChanged', function(){
    var parent = $(this).parent();
    $.ajax({
        url: $(this).data('url'),
        type:'POST',
        headers: {'X-CSRFToken': getCookie('csrftoken') },
        success: function (message) {
            if(message.result == 'ok'){
                Toast.fire({
                    icon: 'success',
                    title: 'Element saved successfully.'
                });
                if(message.removecheck){
                    parent.removeClass("checked");
                }else{
                    parent.addClass("checked");
                }
            }else{
                 Toast.fire({
                    icon: 'error',
                    title: 'Something went wrong while saving this permission rol.'
                });
            }
        }
    });
});


$(".userbtnadd").on('click', function(){
    var id = $(this).data('id');
    var user_list = $("#permissionTable"+id+" tbody tr");
    var url = $(this).data('url');

    if(user_list){
        Array.from(user_list).forEach((item)=>{
            var user_id = $(item).data('id');
            var newOption = new Option($(item).data('name'), user_id, true, false);
            $("#id_users").append(newOption);
            $("#id_users option[value='" + user_id + "']").prop("selected", true);
        });
    }
    $("#id_users").trigger('change');
    $("#adduserform").attr('action', url);
    $("#addusermodal").modal('show');
});