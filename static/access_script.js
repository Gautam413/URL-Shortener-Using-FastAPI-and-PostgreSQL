document.getElementById("accessForm").addEventListener("submit", async function (event) {
    event.preventDefault();

    const emailInput = document.getElementById("user_email");
    const shortUrlInput = document.getElementById("short_url");
    const resultDiv = document.getElementById("result");

    // Clear previous message
    resultDiv.innerHTML = "";

    const email = emailInput.value.trim();
    const shortUrl = shortUrlInput.value.trim();

    if (!email) {
        resultDiv.innerHTML = `<p style="color: red;">Please enter your email.</p>`;
        return;
    }

    const requestData = { user_email: email };

    try {
        // Indicate loading state
        resultDiv.innerHTML = `<p style="color: blue;">Processing request...</p>`;

        const response = await fetch(`http://127.0.0.1:8000/${shortUrl}/request-access`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(requestData)
        });

        const data = await response.json();

        resultDiv.innerHTML = response.ok
            ? `<p style="color: green;">${data.message}</p>`
            : `<p style="color: red;">${data.detail || "Too many requests. Please try again later."}</p>`;
    } catch (error) {
        resultDiv.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
    }
});
