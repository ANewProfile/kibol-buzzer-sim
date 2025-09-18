const socket = io("http://localhost:5001");

// ----- Elements -----
const resetButton = document.getElementById("reset-button");
const nextQButton = document.getElementById("next-question-button");
const questionBox = document.getElementById("question-box");
const buzzStatus = document.getElementById("buzz-status")

// ----- Socket Events -----
socket.on("buzzed", (data) => {
    buzzStatus.innerText = `${data.player} buzzed first!`;
});

socket.on("reset", () => {
    buzzStatus.innerText = "Waiting for buzz...";
});

// ----- Buttons -----
resetButton.addEventListener("click", () => {
    socket.emit("reset");
    buzzStatus.innerText = "Resetting...";
});

nextQButton.addEventListener("click", async () => {
    const response = await fetch("/next_question")
    const data = await response.json()

    questionBox.innerText = data.text
});
