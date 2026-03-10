// =====================================
// SentinelVote AI - Behavioral Tracking
// =====================================

// ===============================
// Global Behavioral Storage
// ===============================
window.holdTimes = [];
window.keyIntervals = [];
window.mouseSpeeds = [];

let keyDownTimes = {};
let lastKeyTime = null;

let lastMouseTime = null;
let lastMouseX = null;
let lastMouseY = null;

let behaviorTrackingEnabled = true; // control flag


// ===============================
// Utility: Limit Array Size
// Prevent memory overflow
// ===============================
function limitArraySize(arr, max = 200) {
    if (arr.length > max) {
        arr.splice(0, arr.length - max);
    }
}


// ===============================
// Key Hold Time + Key Interval
// ===============================
document.addEventListener("keydown", function (e) {

    if (!behaviorTrackingEnabled) return;

    const now = Date.now();
    keyDownTimes[e.code] = now;

    if (lastKeyTime !== null) {
        window.keyIntervals.push(now - lastKeyTime);
        limitArraySize(window.keyIntervals);
    }

    lastKeyTime = now;
});


document.addEventListener("keyup", function (e) {

    if (!behaviorTrackingEnabled) return;

    const now = Date.now();

    if (keyDownTimes[e.code]) {
        const holdTime = now - keyDownTimes[e.code];
        window.holdTimes.push(holdTime);
        limitArraySize(window.holdTimes);

        delete keyDownTimes[e.code];
    }
});


// ===============================
// Mouse Movement Speed
// ===============================
document.addEventListener("mousemove", function (e) {

    if (!behaviorTrackingEnabled) return;

    const now = Date.now();

    if (lastMouseTime !== null) {

        const dx = e.clientX - lastMouseX;
        const dy = e.clientY - lastMouseY;
        const dt = now - lastMouseTime;

        if (dt > 0) {
            const speed = Math.sqrt(dx * dx + dy * dy) / dt;
            window.mouseSpeeds.push(speed);
            limitArraySize(window.mouseSpeeds);
        }
    }

    lastMouseTime = now;
    lastMouseX = e.clientX;
    lastMouseY = e.clientY;
});


// ===============================
// Reset Behavioral Data
// ===============================
function resetBehaviorData() {
    window.holdTimes = [];
    window.keyIntervals = [];
    window.mouseSpeeds = [];
}


// ===============================
// Send Behavioral Data to Server
// ===============================
async function sendBehaviorData(email) {

    if (!email) return;

    try {
        const response = await fetch("/behavior-data", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email: email,
                holdTimes: window.holdTimes,
                keyIntervals: window.keyIntervals,
                mouseSpeeds: window.mouseSpeeds
            })
        });

        if (!response.ok) {
            console.warn("Behavior data submission failed");
        }

    } catch (error) {
        console.error("Behavior tracking error:", error);
    }
}


// ===============================
// Logout
// ===============================
// ===============================
// Logout
// ===============================
function handleLogout() {

    behaviorTrackingEnabled = false;
    resetBehaviorData();
    localStorage.clear();

    // Redirect to logout route (GET)
    window.location.href = "/logout";
}
