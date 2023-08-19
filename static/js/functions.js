function message_error(obj) {
    var html = '<ul style= "text-align:left;">';
    $.each(obj, function(key, value) {
        html += '<li>' + value + '</li>';
    });
    html += '</ul>';
    Swal.fire({
        title: 'Error!',
        html: html,
        icon: 'error',
        allowOutsideClick: false,
		clickOutsideToClose: false,
        confirmButtonText: 'Ok'
    });
}