function applySettings() {
    const bgColor = localStorage.getItem("bgColor") || "#f4f4f9";
    const font = localStorage.getItem("fontFamily") || "Arial";
    const fontSize = localStorage.getItem("fontSize") || "16px";
    const buttonStyle = localStorage.getItem("buttonStyle") || "rounded";

    document.body.style.backgroundColor = bgColor;
    document.body.style.fontFamily = font;
    document.body.style.fontSize = fontSize;

    document.querySelectorAll(".action-button, .nav-button").forEach(btn => {
        if (buttonStyle === "flat") {
            btn.style.borderRadius = "0px";
            btn.style.boxShadow = "none";
        } else {
            btn.style.borderRadius = "4px";
            btn.style.boxShadow = "";
        }
    });
}

document.addEventListener("DOMContentLoaded", () => {
    applySettings();

    if (location.pathname === "/settings") {
        document.getElementById("bgColor").value = localStorage.getItem("bgColor") || "#f4f4f9";
        document.getElementById("fontFamily").value = localStorage.getItem("fontFamily") || "Arial";
        document.getElementById("fontSize").value = parseInt(localStorage.getItem("fontSize") || "16");
        document.getElementById("fontSizeDisplay").textContent = document.getElementById("fontSize").value + "px";
        document.getElementById("buttonStyle").value = localStorage.getItem("buttonStyle") || "rounded";

        document.getElementById("fontSize").addEventListener("input", e => {
            document.getElementById("fontSizeDisplay").textContent = e.target.value + "px";
        });
    }
});

function saveSettings() {
    localStorage.setItem("bgColor", document.getElementById("bgColor").value);
    localStorage.setItem("fontFamily", document.getElementById("fontFamily").value);
    localStorage.setItem("fontSize", document.getElementById("fontSize").value + "px");
    localStorage.setItem("buttonStyle", document.getElementById("buttonStyle").value);
    applySettings();
}