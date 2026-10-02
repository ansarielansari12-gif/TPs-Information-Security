// ======================================
// ACTIVE BROWSER FEATURE COLLECTION
// ======================================

// 1. Browser language
const browserLanguage = navigator.language;

// 2. Time zone
const timeZone = Intl.DateTimeFormat().resolvedOptions().timeZone;

// 3. Screen resolution
const screenResolution = `${screen.width} x ${screen.height}`;

// 4. Color depth
const colorDepth = screen.colorDepth;

// 5. Logical CPU cores
const cpuCores = navigator.hardwareConcurrency;

// 6. Browser window size
const windowSize = `${window.innerWidth} x ${window.innerHeight}`;


// ======================================
// PRINT FEATURES IN BROWSER CONSOLE
// ======================================

console.log("Browser language:", browserLanguage);
console.log("Time zone:", timeZone);
console.log("Screen resolution:", screenResolution);
console.log("Color depth:", colorDepth);
console.log("Logical CPU cores:", cpuCores);
console.log("Browser window size:", windowSize);


// ======================================
// DISPLAY FEATURES ON WEBPAGE
// ======================================

const outputElement = document.getElementById("feature-output");

outputElement.innerHTML = `
    <h2>Collected Active Features</h2>

    <p><strong>Browser language:</strong> ${browserLanguage}</p>

    <p><strong>Time zone:</strong> ${timeZone}</p>

    <p><strong>Screen resolution:</strong> ${screenResolution}</p>

    <p><strong>Color depth:</strong> ${colorDepth}</p>

    <p><strong>Logical CPU cores:</strong> ${cpuCores}</p>

    <p><strong>Browser window size:</strong> ${windowSize}</p>
`;


// ======================================
// SEND FEATURES TO FLASK
// ======================================

fetch("/collect", {
    method: "POST",

    headers: {
        "Content-Type": "application/json"
    },

    body: JSON.stringify({
        browserLanguage: browserLanguage,
        timeZone: timeZone,
        screenResolution: screenResolution,
        colorDepth: colorDepth,
        cpuCores: cpuCores,
        windowSize: windowSize
    })
})
.then(response => response.json())
.then(data => {
    console.log("Server response:", data);
})
.catch(error => {
    console.error("Error sending features:", error);
});