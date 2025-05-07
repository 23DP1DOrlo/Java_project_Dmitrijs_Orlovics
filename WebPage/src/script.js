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

     
    
    const totalTimeInSeconds = +(elapsed / 1000).toFixed(2);
    console.log("Total time (rounded):", totalTimeInSeconds);

    if (totalTimeInSeconds > 3.05) {
        document.getElementById('simple-timer').style.color = 'green';
    } else {
    document.getElementById('simple-timer').style.color = 'red';
    }
    if (totalTimeInSeconds < 7) {
        messageElement.textContent = "Did you even turn the cube, or was that just magic?";
    } 
    else if (totalTimeInSeconds < 10) {
        messageElement.textContent = "Sub-10? Must be using some next-level algorithm.";
    }
    else if (totalTimeInSeconds < 15) {
        messageElement.textContent = "15 seconds? Are you secretly a CFOP master?";
    } 
    else if (totalTimeInSeconds < 23) {
        messageElement.textContent = "Under 23? You’re probably out here solving OLL cases blindfolded.";
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

        if (!isRunning && heldTime >= 500) {
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
  "WebPage/src/images/svg/cube.svg"
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
    }, 600);
  }
});


function animateNumber(id, start, end, duration) {
    const el = document.getElementById(id);
    let startTime = null;
  
    const step = timestamp => {
      if (!startTime) startTime = timestamp;
      const progress = Math.min((timestamp - startTime) / duration, 1);
      const value = Math.floor(progress * (end - start) + start);
      el.textContent = value;
      if (progress < 1) requestAnimationFrame(step);
    };
  
    requestAnimationFrame(step);
  }
  
  let sessions = 500 + Math.floor(Math.random() * 200);
  let users = 50 + Math.floor(Math.random() * 30);
  let countries = 20 + Math.floor(Math.random() * 10);
  
  animateNumber("sessions", 0, sessions, 1000);
  animateNumber("users", 0, users, 1000);
  animateNumber("countries", 0, countries, 1000);
  
  setInterval(() => {
    sessions += Math.floor(Math.random() * 10);
    users += Math.floor(Math.random() * 3 - 1);
    countries += Math.floor(Math.random() * 2 - 1);
  
    animateNumber("sessions", parseInt(document.getElementById("sessions").textContent), sessions, 800);
    animateNumber("users", parseInt(document.getElementById("users").textContent), users, 800);
    animateNumber("countries", parseInt(document.getElementById("countries").textContent), countries, 800);
  }, 5000);


