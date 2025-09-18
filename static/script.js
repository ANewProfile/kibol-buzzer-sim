// connect to the server
const socket = io("http://localhost:5001", {
    transports: ["websocket", "polling"]
});


let playerName;

document.addEventListener("DOMContentLoaded", () => {
    playerName = prompt("Enter your player name:");
    if (!playerName) playerName = "Anonymous";
});

// ----- Elements -----
const buzzButton = document.getElementById("buzz-button");
const statusText = document.getElementById("status-text");

// ----- Buzzing -----
buzzButton.addEventListener("click", () => {
    socket.emit("buzz", { player: playerName });
    buzzButton.disabled = True
});

// ----- Incoming Events -----
socket.on("buzzed", (data) => {
    statusText.innerText = `${data.player} buzzed first!`;
    buzzButton.disabled = True;
});

socket.on("reset", () => {
    statusText.innerText = "Ready...";
    buzzButton.disabled = False;
});

socket.on("connect_error", (err) => {
    console.error("Connection failed: " + err);
});
