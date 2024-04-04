const moon = "bi-moon-stars-fill";
const sun = "bi-sun-fill";

function SetUserThemeCookie(value){
    Cookies.set("user-theme", value, { expires: 14 })
}

function GetUserTheme(){
    let userTheme = "light"
    if (Cookies.get("user-theme")){
        userTheme = Cookies.get("user-theme")
    }

    if(userTheme != "light" && userTheme != "dark"){
        //Get Browser Default
        userTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? "dark" : "light"
    }

    return userTheme
}

function setTheme(targetTheme){
    //Get the current theme

    //Update the user-theme cookie with the new data
    SetUserThemeCookie(targetTheme)
    //Swap the icon on the button
    toggleButton = document.getElementById("themeToggler")
    if(toggleButton){
        if(toggleButton.classList.contains(moon)){
            toggleButton.classList.replace(moon, sun)
        }
        else if (toggleButton.classList.contains(sun)){
            toggleButton.classList.replace(sun, moon)
        }
    }
    document.documentElement.setAttribute("data-bs-theme", targetTheme)
}

function toggleTheme(){
    let theme = GetUserTheme()
    if(theme == "light"){
        setTheme("dark")
    }
    else{
        setTheme("light")
    }
}
