const checkbox = document.getElementById("checkbox");
const twentyone = document.getElementById("twentyone");
const fourteen = document.getElementById("fourteen");
const seven = document.getElementById("seven"); 


checkbox.addEventListener("click", () =>{

    seven.textContent =seven.textContent === "2000" ? "Not Available" : "2000";
    
    twentyone.textContent =twentyone.textContent === "5000" ? "Not Available" : "5000";

    fourteen.textContent =fourteen.textContent === "3500" ? "Not Available" : "3500";

});