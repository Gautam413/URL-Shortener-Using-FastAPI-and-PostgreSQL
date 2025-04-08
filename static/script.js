document.getElementById("shortenForm").addEventListener("submit", async function(event) {
    event.preventDefault(); // Prevent form refresh

    const original_url = document.getElementById("original_url").value;
    const creator_email = document.getElementById("creator_email").value;
    const authorized_emails = document.getElementById("authorized_emails").value.split(",").map(email => email.trim()).filter(email => email !== "");

    console.log("User entered URL:", original_url);
    console.log("Is valid:", isValidURL(original_url));
    if (!isValidURL(original_url)) {
        document.getElementById("result").innerHTML = `<p style="color: red;">Invalid URL! Please enter a valid HTTP or HTTPS URL.</p>`;
        return;
    }
    if (authorized_emails.includes(creator_email)) {
        document.getElementById("result").innerHTML = `<p style="color: red;">Creator email cannot be in the authorized emails list.</p>`;
        return;
    }
    if (authorized_emails.length === 0) {
        document.getElementById("result").innerHTML = `<p style="color: red;">Please enter at least one authorized email.</p>`;
        return;
    }

    const invalidEmails = authorized_emails.filter(email => !isValidEmail(email));

if (invalidEmails.length > 0) {
    document.getElementById("result").innerHTML = `<p style="color: red;">Invalid emails found: ${invalidEmails.join(", ")}</p>`;
    return;
}

if (authorized_emails.length === 0 || (authorized_emails.length === 1 && authorized_emails[0] === "")) {
    document.getElementById("result").innerHTML = `<p style="color: red;">Please enter at least one valid authorized email.</p>`;
    return;
}

    const requestData = {
        original_url: original_url,
        creator_email: creator_email,
        authorized_emails: authorized_emails
    };

    try {
        const response = await fetch("http://127.0.0.1:8000/shorten", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(requestData)
        });

        if (!response.ok) {
            // Log the detailed error response
            const errorData = await response.json();
            console.error("Server Error:", errorData);
    
            document.getElementById("result").innerHTML = `<p style="color: red;">Error: ${errorData.detail || "Invalid input!"}</p>`;
            return;
        }


        const data = await response.json();

        document.getElementById("result").innerHTML = data.short_url
            ? `<h3>Your Shortened URL:</h3> <a href="${data.short_url}" target="_blank">${data.short_url}</a>.<br><br> This link will expire in <b>60 days.`
            : `<p style="color: red;">${data.detail}</p>`;
    } catch (error) {
        document.getElementById("result").innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
    }
});

function isValidURL(url) {
    try {
        const parsedUrl = new URL(url); // Checks for basic structure

        // Ensures correct protocol
        if (!(parsedUrl.protocol === "http:" || parsedUrl.protocol === "https:")) {
            return false;
        }

        const domainPattern = /^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        const hostname = parsedUrl.hostname;

        return domainPattern.test(hostname);
    } catch (e) {
        return false;
    }
}

// Email validation function
function isValidEmail(email) {
    const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return emailPattern.test(email);
}