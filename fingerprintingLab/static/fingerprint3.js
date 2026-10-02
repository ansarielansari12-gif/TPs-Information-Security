// ======================================
// PART 4 — SHA-256 FINGERPRINT
// ======================================


// ======================================
// GET HTML ELEMENT
// ======================================

const fingerprintOutput =
    document.getElementById("fingerprint-output");


// ======================================
// COMBINE FEATURES IN A FIXED ORDER
// ======================================

// We exclude typing behaviour here.
// The goal is to test whether the fingerprint
// remains stable when the browser features
// stay the same.

const fingerprintData = [
    browserLanguage,
    screenResolution,
    timeZone,
    colorDepth,
    cpuCores,
    windowSize
].join("|");


// Show the combined data in the console
// so we can understand what is being hashed.

console.log("Fingerprint input:", fingerprintData);


// ======================================
// GENERATE SHA-256 HASH
// ======================================

async function generateFingerprint() {

    // Convert the fingerprint data into bytes
    const encoder = new TextEncoder();

    const data = encoder.encode(fingerprintData);


    // Generate SHA-256 hash
    const hashBuffer =
        await crypto.subtle.digest(
            "SHA-256",
            data
        );


    // Convert the hash into an array of bytes
    const hashArray =
        Array.from(new Uint8Array(hashBuffer));


    // Convert each byte to hexadecimal
    const hashHex =
        hashArray
            .map(
                byte =>
                    byte
                        .toString(16)
                        .padStart(2, "0")
            )
            .join("");


    // ======================================
    // DISPLAY FINGERPRINT ON WEBPAGE
    // ======================================

    fingerprintOutput.innerHTML = `
        <h2>Browser Fingerprint</h2>

        <p>
            <strong>SHA-256 fingerprint:</strong>
            ${hashHex}
        </p>
    `;


    // ======================================
    // PRINT FINGERPRINT IN CONSOLE
    // ======================================

    console.log(
        "SHA-256 fingerprint:",
        hashHex
    );


    // ======================================
    // SEND ONLY THE HASH TO FLASK
    // ======================================

    fetch("/collect", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({

            fingerprint: hashHex

        })

    })

    .then(response => response.json())

    .then(data => {

        console.log(
            "Fingerprint server response:",
            data
        );

    })

    .catch(error => {

        console.error(
            "Error sending fingerprint:",
            error
        );

    });
}


// ======================================
// START FINGERPRINT GENERATION
// ======================================

generateFingerprint();