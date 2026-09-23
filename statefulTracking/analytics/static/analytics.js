function getCookie(name) {
    const cookies = document.cookie.split("; ");

    for (const cookie of cookies) {
        const parts = cookie.split("=");

        if (parts[0] === name) {
            return parts[1];
        }
    }

    return null;
}


// Generate a random identifier
function generateId() {
    return Math.random().toString(36).substring(2) +
           Date.now().toString(36);
}


// 1. Check whether the analytics cookie exists
let analyticsId = getCookie("analytics_id");


// 2. Generate an identifier if it does not exist
if (!analyticsId) {
    analyticsId = generateId();

    // 3. Store the identifier
    document.cookie =
        "analytics_id=" + analyticsId +
        "; Max-Age=31536000; Path=/";
}


// 4. Collect browsing activity
const publisher = window.location.hostname;
const page = window.location.pathname;


// Send the activity to the analytics server
fetch(
    "http://analytics.test:9100/collect" +
    "?id=" + encodeURIComponent(analyticsId) +
    "&publisher=" + encodeURIComponent(publisher) +
    "&page=" + encodeURIComponent(page)
);