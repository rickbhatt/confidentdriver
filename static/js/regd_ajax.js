function ReSendOTP(email, mess_id){
    mess = document.getElementById(mess_id);
    mess.innerText = "Sending...";
    $.ajax({
        type: 'GET',
        url: 'resendOTP',
        data: {usr:email},
        success: function(data){
            mess.innerText = data;
        }
    })
}