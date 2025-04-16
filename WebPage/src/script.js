let timerElement = document.getElementById("simple-timer");
let messageElement = document.getElementById("message");

let isRunning = false;
let startTime = null;
let elapsed = 0;
let animationFrame = null;

let spacePressedAt = null;

function formatTime(ms) {
    const totalSeconds = Math.floor(ms / 1000);
    const minutes = Math.floor(totalSeconds / 60);
    const seconds = totalSeconds % 60;
    const centiseconds = Math.floor((ms % 1000) / 10);
    return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}:${String(centiseconds).padStart(2, '0')}`;
}

function updateTimer() {
    const currentTime = performance.now();
    const currentElapsed = currentTime - startTime + elapsed;
    timerElement.textContent = formatTime(currentElapsed);
    animationFrame = requestAnimationFrame(updateTimer);
}

function startTimer() {
    startTime = performance.now();
    animationFrame = requestAnimationFrame(updateTimer);
    isRunning = true;
}

function stopTimer() {
    cancelAnimationFrame(animationFrame);
    const currentTime = performance.now();
    elapsed += currentTime - startTime;
    isRunning = false;
    
    const totalTimeInSeconds = Math.floor(elapsed / 1000);
    if (totalTimeInSeconds < 7) {
        messageElement.textContent = "Did you even turn the cube, or was that just magic?";
    } 
    else if (totalTimeInSeconds < 10) {
        messageElement.textContent = "Sub-10? Must be using some next-level algorithm.";
    }
    else if (totalTimeInSeconds < 15) {
        messageElement.textContent = "15 seconds? Are you secretly a CFOP master?";
    } 
    else if (totalTimeInSeconds < 20) {
        messageElement.textContent = "Under 20? You’re probably out here solving OLL cases blindfolded.";
    } else {
        messageElement.textContent = "30 seconds or less? Guess you’re on your way to becoming the next speedcubing legend, just learn OLLs and PLLs.";
    }
}

document.addEventListener("keydown", (e) => {
    if (e.code === "Space" && !spacePressedAt) {
        e.preventDefault();
        spacePressedAt = performance.now();
    }
});

document.addEventListener("keyup", (e) => {
    if (e.code === "Space") {
        e.preventDefault();
        const heldTime = performance.now() - spacePressedAt;
        spacePressedAt = null;

        if (!isRunning && heldTime >= 1000) {
            elapsed = 0;
            timerElement.textContent = "00:00:00";
            startTimer();
        } else if (isRunning) {
            stopTimer();
        }
    }
});
document.addEventListener("keydown", (e) => {
    if (e.code === "Space" && !spacePressedAt) {
        e.preventDefault();
        spacePressedAt = performance.now();
    }
});

// space dont scroll
window.addEventListener("keydown", function (e) {
    if (e.code === "Space" && e.target === document.body) {
        e.preventDefault();
    }
});

// CUBES
const fallingContainer = document.querySelector(".falling-objects");
const imageSources = [
  "/JAVA_Project_Timer/WebPage/src/images/svg/cube.svg"
];

function spawnFallingImage() {
  const img = document.createElement("img");
  img.src = imageSources[Math.floor(Math.random() * imageSources.length)];
  img.classList.add("falling");
  img.style.left = `${Math.random() * window.innerWidth}px`;
  fallingContainer.appendChild(img);

  setTimeout(() => {
    img.remove();
  }, 3000);
}

let scrollTimeout;
window.addEventListener("scroll", () => {
  if (!scrollTimeout) {
    spawnFallingImage();
    scrollTimeout = setTimeout(() => {
      scrollTimeout = null;
    }, 400);
  }
});