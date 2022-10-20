var contentString = 
`

`;


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


$("table").prepend(contentString);
$('.dropOneColumn').confirm({
    title: 'Confirm',
    content: 'Delete column!',
    buttons: {
        delete: {
            text: 'Delete',
            btnClass: 'btn-red',
            keys: ['enter', 'shift'],
            action: function(){
                var process = this.$target.val();
                var column = this.$target.attr('val1');
                $.ajax({
                    type:"POST",
                    data: {process:process, value1:column,value2:null},
                    url: window.location.pathname,
                    cache: false,
                    dataType: "html",
                    success: function(){
                        window.location.reload();
                    },
                    error: function(){
                        alert("false");
                    }
                });
            }
        },
        cancel: function () {
        },
    }
});
$('.dropNullRowsInColumn').confirm({
    title: 'Confirm',
    content: 'Delete Null row in this column!',
    buttons: {
        delete: {
            text: 'Delete',
            btnClass: 'btn-red',
            keys: ['enter', 'shift'],
            action: function(){
                var process = this.$target.val();
                var column = this.$target.attr('val1');
                var axis = this.$target.attr('val2');
                $.ajax({
                    type:"POST",
                    data: {process:process, value1:column,value2:axis},
                    url: window.location.pathname,
                    cache: false,
                    dataType: "html",
                    success: function(){
                        window.location.reload();
                    },
                    error: function(){
                        alert("false");
                    }
                });
            }
        },
        cancel: function () {
        },
    }
});
$('.dropAllNullRows').confirm({
    title: 'Confirm',
    content: 'Delete all rows contain null values!',
    buttons: {
        delete: {
            text: 'Delete',
            btnClass: 'btn-red',
            keys: ['enter', 'shift'],
            action: function(){
                var process = this.$target.val();
                var axis = this.$target.attr('val1');

                $.ajax({
                    type:"POST",
                    data: {process:process, value1:axis, value2:null},
                    url: window.location.pathname,
                    cache: false,
                    dataType: "html",
                    success: function(){
                        window.location.reload();
                    },
                    error: function(){
                        alert("false");
                    }
                });
            }
        },
        cancel: function () {
        },
    }
});

$('.dropAllNullColumns').confirm({
    title: 'Confirm',
    content: 'Delete all columns contain null values!',
    buttons: {
        delete: {
            text: 'Delete',
            btnClass: 'btn-red',
            keys: ['enter', 'shift'],
            action: function(){
                var process = this.$target.val();
                var axis = this.$target.attr('val1');
                $.ajax({
                    type:"POST",
                    data: {process:process, value1:axis, value2:null},
                    url: window.location.pathname,
                    cache: false,
                    dataType: "html",
                    success: function(){
                        window.location.reload();
                    },
                    error: function(){
                        alert("false");
                    }
                });
            }
        },
        cancel: function () {
        },
    }
});


$('.replaceAllNulls').confirm({
    title: 'split null values!',
    content: '' +
    '<form action="" class="formName">' +
    '<div class="form-group">' +
    '<label>Enter the value to split here</label>' +
    '<input type="text" placeholder="split with" class="name form-control" required />' +
    '</div>' +
    '</form>',
    buttons: {
        formSubmit: {
            text: 'Submit',
            btnClass: 'btn-blue',
            action: function () {
                var name = this.$content.find('.name').val();
                if(!name){
                    $.alert('provide a valid name');
                    return false;
                }
                var process = this.$target.val();
                $.ajax({
                    type:"POST",
                    data: {process:process, value1:name, value2:null},
                    url: window.location.pathname,
                    cache: false,
                    dataType: "html",
                    success: function(){
                        window.location.reload();
                    },
                    error: function(){
                        alert("false");
                    }
                });

                // $.alert('Your name is ' + name);
            }
        },
        cancel: function () {
            //close
        },
    },
    onContentReady: function () {
        // bind to events
        var jc = this;
        this.$content.find('form').on('submit', function (e) {
            // if the user submits the form by pressing enter in the field.
            e.preventDefault();
            jc.$$formSubmit.trigger('click'); // reference the button and click it
        });
    }
});


$('.replaceColNulls').confirm({
    title: 'split null values!',
    content: '' +
    '<form action="" class="formName">' +
    '<div class="form-group">' +
    '<label>Enter the value to split here</label>' +
    '<input type="text" placeholder="split with" class="name form-control" required />' +
    '</div>' +
    '</form>',
    buttons: {
        formSubmit: {
            text: 'Submit',
            btnClass: 'btn-blue',
            action: function () {
                var name = this.$content.find('.name').val();
                var column = this.$target.attr('val1');
                console.log(column);
                if(!name){
                    $.alert('provide a valid value');
                    return false;
                }
                var process = this.$target.val();
                $.ajax({
                    type:"POST",
                    data: {process:process, value1:column, value2:name},
                    url: window.location.pathname,
                    cache: false,
                    dataType: "html",
                    success: function(){
                        window.location.reload();
                    },
                    error: function(){
                        alert("false");
                    }
                });
                // $.alert('Your name is ' + name);
            }
        },
        cancel: function () {
            //close
        },
    },
    onContentReady: function () {
        // bind to events
        var jc = this;
        this.$content.find('form').on('submit', function (e) {
            // if the user submits the form by pressing enter in the field.
            e.preventDefault();
            jc.$$formSubmit.trigger('click'); // reference the button and click it
        });
    }
});


$('.splitCol').confirm({
    title: 'split column!',
    content: '' +
    '<form action="" class="formName">' +
    '<div class="form-group">' +
    '<label>Separator</label>' +
    '<input type="text" placeholder="Separator" class="separator form-control" required />' +
    '</div>' +
    '</form>',
    buttons: {
        formSubmit: {
            text: 'Submit',
            btnClass: 'btn-blue',
            action: function () {
                var separator = this.$content.find('.separator').val();
                var column = this.$target.attr('val1');
                if(!separator){
                    $.alert('provide a valid value');
                    return false;
                }
                var process = this.$target.val();
                $.ajax({
                    type:"POST",
                    data: {process:process, value1:column, value2:separator},
                    url: window.location.pathname,
                    cache: false,
                    dataType: "html",
                    success: function(){
                        window.location.reload();
                    },
                    error: function(){
                        alert("false");
                    }
                });
            }
        },
        cancel: function () {
            //close
        },
    },
    onContentReady: function () {
        // bind to events
        var jc = this;
        this.$content.find('form').on('submit', function (e) {
            // if the user submits the form by pressing enter in the field.
            e.preventDefault();
            jc.$$formSubmit.trigger('click'); // reference the button and click it
        });
    }
});


$('.rename_col').confirm({
    title: 'rename column!',
    content: '' +
    '<form action="" class="formName">' +
    '<div class="form-group">' +
    '<label>New Name</label>' +
    '<input type="text" placeholder="name" class="name form-control" required />' +
    '</div>' +
    '</form>',
    buttons: {
        formSubmit: {
            text: 'Submit',
            btnClass: 'btn-blue',
            action: function () {
                var name = this.$content.find('.name').val();
                var column = this.$target.attr('val1');
                console.log(column);
                if(!name){
                    $.alert('provide a valid value');
                    return false;
                }
                var process = this.$target.val();
                $.ajax({
                    type:"POST",
                    data: {process:process, value1:column, value2:name},
                    url: window.location.pathname,
                    cache: false,
                    dataType: "html",
                    success: function(){
                        window.location.reload();
                    },
                    error: function(){
                        alert("false");
                    }
                });
                // $.alert('Your name is ' + name);
            }
        },
        cancel: function () {
            //close
        },
    },
    onContentReady: function () {
        // bind to events
        var jc = this;
        this.$content.find('form').on('submit', function (e) {
            // if the user submits the form by pressing enter in the field.
            e.preventDefault();
            jc.$$formSubmit.trigger('click'); // reference the button and click it
        });
    }
});



$('.undo').confirm({
    title: 'Confirm',
    content: 'Are you shore you want to undo changes!',
    buttons: {
        delete: {
            text: 'UnDo',
            btnClass: 'btn-red',
            keys: ['enter', 'shift'],
            action: function(){
                var process = this.$target.val();
                console.log('process', process);
                $.ajax({
                    type:"POST",
                    data: {process:process, value1:null, value2:null},
                    url: window.location.pathname,
                    cache: false,
                    dataType: "html",
                    success: function(){
                        window.location.reload();
                    },
                    error: function(){
                        alert("false");
                    }
                });
            }
        },
        cancel: function () {
        },
    }
});





var CheckBoxHtml = function (){
    var column = $(this).val();
    console.log({"columntestcvgfbhn":column});
    var columns = [];
    var types = [];
    let checkboxHtml = "";
    $(".col_button").each(function(){
        columns.push($(this).val());
        console.log({"$(this).val()":$(this).val()});
        types.push($(this).attr('col-type'));
        console.log({"types":types});
    });
    for (let x in columns) {
        if (column != columns[x]) {
            
        checkboxHtml += `<br>
        <label class="container_checkbox">
        <input type="checkbox" class="col_name" name="col_name value="${columns[x]}"">
        <span class="checkmark"></span>
        ${columns[x]}</label>`;}
    };
    return checkboxHtml ;
};



$('.joinStrCol').confirm({
    columnClass: 'col-md-6',
    title: 'join columns!',
    content: function () {
        var column = this.$target.attr('val1');
        console.log({"columntestcvgfbhn":column});
        var types = [];
        let checkboxHtml = "";
        $(".col_button").each(function(){
            var col = $(this).val();
            var type = $(this).attr('col-type');
            console.log({"type":type});
            if (col != column & type == 'object') {
            checkboxHtml += `<br>
            <label class="container_checkbox">
            <input type="checkbox" class="col_name" name="col_name" value="${col}">
            <span class="checkmark"></span>
            ${col}</label>`;}
        });

        return(
        '' +
        '<form action="" class="formName">' +
        '<div class="form-group">' +
        `<label>select the column to join with  (<strong style="color:#0CAFFF; font-weight:bold"> ${column} </strong>) column</label>` +
        checkboxHtml +
        '</div>' +
        '</form>')
    },
    buttons: {
        formSubmit: {
            text: 'Submit',
            btnClass: 'btn-blue',
            action: function () {
                var columns = [];
                $('.col_name:checked').each(function () {
                    columns.push(this.value);
                });       
                var column = this.$target.attr('val1');
                console.log({"columns": columns});
                if(!columns){
                    $.alert('provide a valid value');
                    return false;
                }
                var process = this.$target.val();
                $.ajax({
                    type:"POST",
                    data: {process:process, value1:column, valueslist:columns},
                    url: window.location.pathname,
                    cache: false,
                    dataType: "html",
                    success: function(){
                        window.location.reload();
                    },
                    error: function(){
                        alert("false");
                    }
                });
                // $.alert('Your name is ' + name);
            }
        },
        cancel: function () {
            //close
        },
    },
    onContentReady: function () {
        // bind to events
        var jc = this;
        this.$content.find('form').on('submit', function (e) {
            // if the user submits the form by pressing enter in the field.
            e.preventDefault();
            jc.$$formSubmit.trigger('click'); // reference the button and click it
        });
    }
});