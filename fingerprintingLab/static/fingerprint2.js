// ======================================
// TASK 4 — ALICE'S TYPING RHYTHM
// ======================================


// ======================================
// GET HTML ELEMENTS
// ======================================

const targetSentence = document.getElementById("target-sentence");

const typingInput = document.getElementById("typing-input");

const restartButton = document.getElementById("restart-button");

const typingResults = document.getElementById("typing-results");


// ======================================
// GET TARGET SENTENCE
// ======================================

// Get the exact sentence Alice must reproduce
const targetText = targetSentence.textContent.trim();

console.log("Target sentence:", targetText);


// ======================================
// EXPERIMENT VARIABLES
// ======================================

// Timer variables
let startTime = null;
let endTime = null;

// Number of Backspace corrections
let corrections = 0;

// Indicates whether the experiment is finished
let experimentFinished = false;


// ======================================
// OBSERVE ALICE'S TYPING
// ======================================

typingInput.addEventListener("input", function () {

    // ----------------------------------
    // START TIMER
    // ----------------------------------

    // Start the timer when Alice types
    // her first character
    if (startTime === null && typingInput.value.length > 0) {

        startTime = performance.now();

        console.log("Typing experiment started.");
    }


    // ----------------------------------
    // CHECK IF SENTENCE IS EXACTLY CORRECT
    // ----------------------------------

    if (
        !experimentFinished &&
        typingInput.value === targetText
    ) {

        // Stop the timer
        endTime = performance.now();

        experimentFinished = true;


        // ----------------------------------
        // CALCULATE TYPING TIME
        // ----------------------------------

        const typingTime =
            (endTime - startTime) / 1000;


        // ----------------------------------
        // CALCULATE TYPING SPEED
        // ----------------------------------

        // Formula:
        // typing speed =
        // number of characters / time in seconds

        const typingSpeed =
            targetText.length / typingTime;


        // ----------------------------------
        // DISPLAY RESULTS
        // ----------------------------------

        typingResults.innerHTML = `

            <h2>Results</h2>

            <p>
                <strong>Total typing time:</strong>
                ${typingTime.toFixed(2)} seconds
            </p>

            <p>
                <strong>Typing speed:</strong>
                ${typingSpeed.toFixed(2)}
                characters/second
            </p>

            <p>
                <strong>Corrections:</strong>
                ${corrections}
            </p>

        `;


        // ----------------------------------
        // PRINT RESULTS IN BROWSER CONSOLE
        // ----------------------------------

        console.log("Typing experiment finished.");

        console.log(
            "Typing time:",
            typingTime.toFixed(2),
            "seconds"
        );

        console.log(
            "Typing speed:",
            typingSpeed.toFixed(2),
            "characters/second"
        );

        console.log(
            "Corrections:",
            corrections
        );


        // ----------------------------------
        // SEND RESULTS TO FLASK
        // ----------------------------------

        fetch("/collect", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                typingTime:
                    Number(typingTime.toFixed(2)),

                typingSpeed:
                    Number(typingSpeed.toFixed(2)),

                corrections:
                    corrections

            })

        })

        .then(response => response.json())

        .then(data => {

            console.log(
                "Server response:",
                data
            );

        })

        .catch(error => {

            console.error(
                "Error sending typing data:",
                error
            );

        });


        // Disable input after the experiment finishes
        typingInput.disabled = true;
    }

});


// ======================================
// COUNT BACKSPACE CORRECTIONS
// ======================================

typingInput.addEventListener("keydown", function (event) {

    // Every Backspace press is counted
    // as one correction
    if (event.key === "Backspace") {

        corrections++;

        console.log(
            "Backspace detected."
        );

        console.log(
            "Corrections:",
            corrections
        );
    }

});


// ======================================
// RESTART EXPERIMENT
// ======================================

restartButton.addEventListener("click", function () {

    // Clear input
    typingInput.value = "";


    // Reset timer
    startTime = null;
    endTime = null;


    // Reset corrections
    corrections = 0;


    // Reset experiment state
    experimentFinished = false;


    // Clear results
    typingResults.innerHTML = "";


    // Enable input again
    typingInput.disabled = false;


    // Put cursor back in input
    typingInput.focus();


    console.log(
        "Typing experiment restarted."
    );

});