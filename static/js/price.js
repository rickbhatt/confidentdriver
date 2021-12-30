const checkbox = document.getElementById("checkbox");
const thirty = document.getElementById("thirty");
const fourteen = document.getElementById("fourteen");
const seven = document.getElementById("seven"); 


checkbox.addEventListener("click", () =>{

    seven.textContent =seven.textContent === "999" ? "1799" : "999";
    
    thirty.textContent =thirty.textContent === "2699" ? "4999" : "2699";

    fourteen.textContent =fourteen.textContent === "1899" ? "3599" : "1899";

});