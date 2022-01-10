
let csrftoken = getCookie('csrftoken');

$(function() {
    $('#confirm-backup-btn').click(function(e) {
        $.ajax({
        type: "POST",
        url: backup_to_s3_url,
        headers:{'X-CSRFToken':csrftoken},
        success: function (response) {
            console.log(response);
            if(response.success){
                $('#spinnerModal').hide();
                $('.modal-backdrop').remove();
            }
            if(response.error) {
                $('#spinnerModal').hide();
                $('.modal-backdrop').remove();
                setTimeout(() => alert(response.error), 2000)
            }
        }
        });
    });

    $('#confirm-restore-btn').click(function(e) {
        $.ajax({
        type: "POST",
        url: restore_from_s3_url,
        headers:{'X-CSRFToken':csrftoken},
        success: function (response) {
            if(response.success){
                $('#spinnerRestoreModal').hide();
                window.location.reload();
            }
            if(response.error) {
                $('#spinnerRestoreModal').hide();
                $('.modal-backdrop').remove();
                alert(response.error)
            }

        }

        });
    });

});