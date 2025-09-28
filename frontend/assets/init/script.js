const usernameInput = document.getElementById("username_input")

usernameInput.addEventListener("keydown", function (event){
    if (event.key === "Enter"){

        event.preventDefault();

        const nick = usernameInput.value.trim();

        if (nick.length >=  15){
            alert("O nick pode ter no maxímo 15 caracteres");
            return;
        }
        
        sessionStorage.setItem("username", nick);
        window.location.href = "../pages/main.html";

        usernameInput.value = "";
    
    }
});