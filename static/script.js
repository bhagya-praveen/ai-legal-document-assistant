const loginButton = document.getElementById("loginButton");
const registerButton = document.getElementById("registerButton");

const emailInput = document.getElementById("email");
const passwordInput = document.getElementById("password");

const authStatus = document.getElementById("authStatus");

const logoutButton = document.getElementById("logoutButton");

const documentSection = document.getElementById("documentSection");
const questionSection = document.getElementById("questionSection");


function updateAuthUI() {

    const token = localStorage.getItem("token");

    console.log("Token exists:", !!token);

    if (token) {

        logoutButton.style.display = "inline-block";

        documentSection.hidden = false;
        questionSection.hidden = false;

    } else {

        logoutButton.style.display = "none";

        documentSection.hidden = true;
        questionSection.hidden = true;

    }
}




registerButton.addEventListener("click", async () => {

    const email = emailInput.value;
    const password = passwordInput.value;

    const username = email.split("@")[0];

    try {

        const response = await fetch("/api/auth/register", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                username: username,
                email: email,
                password: password
            })

        });

        const data = await response.json();

        if (response.ok) {

            authStatus.textContent =
                "Registration successful. You can now login.";


                emailInput.value = "";
                passwordInput.value = "";

        } else {

            authStatus.textContent =
                data.message || "Registration failed.";

        }

    } catch (error) {

        authStatus.textContent =
            "Could not connect to the server.";

        console.error(error);
    }

});


loginButton.addEventListener("click", async () => {

    const email = emailInput.value;
    const password = passwordInput.value;

    try {

        const response = await fetch("/api/auth/login", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                email: email,
                password: password
            })

        });

        const data = await response.json();

        if (response.ok) {

            localStorage.setItem(
                "token",
                data.access_token
            );

            authStatus.textContent =
                "Login successful!";

            passwordInput.value = "";

                updateAuthUI();


        } else {

            authStatus.textContent =
                data.message || "Invalid email or password.";

        }

    } catch (error) {

        authStatus.textContent =
            "Could not connect to the server.";

        console.error(error);
    }

});

const uploadButton = document.getElementById("uploadButton");
const documentFile = document.getElementById("documentFile");
const uploadStatus = document.getElementById("uploadStatus");


uploadButton.addEventListener("click", async () => {

    const file = documentFile.files[0];

    if (!file) {
        uploadStatus.textContent = "Please select a PDF file.";
        return;
    }

    const token = localStorage.getItem("token");

    if (!token) {
        uploadStatus.textContent = "Please login first.";
        return;
    }

    const formData = new FormData();

    formData.append("file", file);

    try {

        uploadStatus.textContent = "Uploading...";

        const response = await fetch("/api/documents/upload", {

            method: "POST",

            headers: {
                "Authorization": `Bearer ${token}`
            },

            body: formData

        });

        const data = await response.json();

        if (response.ok) {

                    uploadStatus.innerHTML = `
                <strong>Document uploaded successfully!</strong><br>
                File: ${data.document.filename}<br>
                <small>You can now ask questions about this document.</small>
            `;

            localStorage.setItem(
                "documentId",
                data.document.id
            );

        } else {

            uploadStatus.textContent =
                data.message || data.msg || "Upload failed.";

        }

    } catch (error) {

        uploadStatus.textContent =
            "Could not connect to the server.";

        console.error(error);
    }

});


const askButton = document.getElementById("askButton");
const questionInput = document.getElementById("question");
const answerBox = document.getElementById("answer");


askButton.addEventListener("click", async () => {

    const question = questionInput.value.trim();

    if (!question) {
        answerBox.textContent = "Please enter a question.";
        return;
    }

    const token = localStorage.getItem("token");
    const documentId = localStorage.getItem("documentId");

    if (!token) {
        answerBox.textContent = "Please login first.";
        return;
    }

    if (!documentId) {
        answerBox.textContent = "Please upload a document first.";
        return;
    }

    try {

            askButton.disabled = true;
        askButton.textContent = "Analyzing...";

        answerBox.textContent =
            "⏳ Analyzing the document and generating an answer...";


        const response = await fetch(
            `/api/documents/${documentId}/ask`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },

                body: JSON.stringify({
                    question: question
                })
            }
        );

        const data = await response.json();

        if (response.ok) {

            answerBox.textContent = data.answer;

        } else {

            answerBox.textContent =
                answerBox.textContent =
            data.error || data.message || data.msg || "Could not generate answer.";

        }

        

    }  catch (error) {

    answerBox.textContent =
        "Could not connect to the server. Check the Flask terminal for the actual error.";

    console.error("Request error:", error);
    }

    finally {

    askButton.disabled = false;
    askButton.textContent = "Ask Question";
}



});






logoutButton.addEventListener("click", () => {

    localStorage.removeItem("token");
    localStorage.removeItem("documentId");

     emailInput.value = "";
    passwordInput.value = "";

    authStatus.textContent = "Logged out successfully.";

    uploadStatus.textContent = "";

    answerBox.textContent =
        "Your answer will appear here.";

    updateAuthUI();

});


updateAuthUI();