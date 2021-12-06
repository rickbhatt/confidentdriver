const checkbox = document.getElementById('checkagree')
const agreeBtn = document.getElementById('iagree')


checkbox.addEventListener("click", () =>{

    if(checkbox.checked){
        agreeBtn.disabled = false;
    }else{
            agreeBtn.disabled = true;
    }
});

