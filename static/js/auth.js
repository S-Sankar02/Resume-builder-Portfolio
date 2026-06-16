/* ==========================================
   AI RESUME BUILDER - FULL APP JS
========================================== */

/* ==========================================
   AUTH FEATURES
========================================== */

/* PASSWORD TOGGLE */
function togglePassword() {
    const field = document.getElementById("password");
    if (!field) return;
    field.type = field.type === "password" ? "text" : "password";
}

/* CONFIRM PASSWORD TOGGLE */
function toggleConfirmPassword() {
    const field = document.getElementById("confirmPassword");
    if (!field) return;
    field.type = field.type === "password" ? "text" : "password";
}

/* PASSWORD STRENGTH */
function passwordStrength() {

    const password = document.getElementById("password");
    const bar = document.getElementById("strengthBar");
    const text = document.getElementById("strengthText");

    if (!password || !bar || !text) return;

    let value = password.value;
    let score = 0;

    if (value.length >= 8) score++;
    if (/[A-Z]/.test(value)) score++;
    if (/[a-z]/.test(value)) score++;
    if (/[0-9]/.test(value)) score++;
    if (/[!@#$%^&*()_+\-=[\]{};':"\\|,.<>/?]/.test(value)) score++;

    if (score <= 2) {
        bar.style.width = "30%";
        bar.className = "progress-bar bg-danger";
        text.innerText = "Weak Password";
    }
    else if (score <= 4) {
        bar.style.width = "70%";
        bar.className = "progress-bar bg-warning";
        text.innerText = "Medium Password";
    }
    else {
        bar.style.width = "100%";
        bar.className = "progress-bar bg-success";
        text.innerText = "Strong Password";
    }
}

/* EMAIL VALIDATION */
function validateEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

/* LOGIN VALIDATION */
function validateLoginForm() {

    const email = document.querySelector("input[name='email']");
    const password = document.querySelector("input[name='password']");

    if (!email || !password) return true;

    if (!validateEmail(email.value)) {
        alert("Enter valid email");
        return false;
    }

    if (password.value.length < 6) {
        alert("Password too short");
        return false;
    }

    return true;
}

/* REGISTER VALIDATION */
function validateRegisterForm() {

    const email = document.querySelector("input[name='email']");
    const password = document.getElementById("password");
    const confirm = document.getElementById("confirmPassword");

    if (!email || !password || !confirm) return true;

    if (!validateEmail(email.value)) {
        alert("Invalid email");
        return false;
    }

    if (password.value.length < 8) {
        alert("Min 8 characters required");
        return false;
    }

    if (password.value !== confirm.value) {
        alert("Passwords do not match");
        return false;
    }

    return true;
}

/* DARK MODE */
function toggleTheme() {
    document.body.classList.toggle("dark-mode");
    localStorage.setItem(
        "theme",
        document.body.classList.contains("dark-mode") ? "dark" : "light"
    );
}

/* LOAD THEME */
window.addEventListener("load", () => {
    if (localStorage.getItem("theme") === "dark") {
        document.body.classList.add("dark-mode");
    }
});

/* AUTO REMOVE ALERTS */
window.addEventListener("load", () => {
    document.querySelectorAll(".alert").forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = "0";
            setTimeout(() => alert.remove(), 500);
        }, 4000);
    });
});

/* LOADING BUTTON */
function loadingButton(btn) {
    if (!btn) return;
    btn.disabled = true;
    btn.innerText = "Please wait...";
}

/* FORM AUTO SUBMIT PREVENT */
document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("form").forEach(form => {
        form.addEventListener("submit", () => {
            const btn = form.querySelector("button[type='submit']");
            if (btn) loadingButton(btn);
        });
    });
});

/* ==========================================
   RESUME BUILDER
========================================== */

let currentResumeId = null;
let autosaveTimer = null;

/* CREATE RESUME */
async function createResume() {

    const res = await fetch("/resume/create", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            title: "Untitled Resume",
            template_id: "basic"
        })
    });

    const data = await res.json();
    currentResumeId = data.id;

    loadResumes();
}

/* LOAD RESUMES */
async function loadResumes() {

    const res = await fetch("/resume/");
    const data = await res.json();

    const list = document.getElementById("resumeList");
    if (!list) return;

    list.innerHTML = "";

    data.forEach(r => {
        const div = document.createElement("div");
        div.className = "resume-item";
        div.innerText = r.title;
        div.onclick = () => loadResume(r.id);
        list.appendChild(div);
    });
}

/* LOAD SINGLE RESUME */
async function loadResume(id) {

    const res = await fetch(`/resume/${id}`);
    const data = await res.json();

    currentResumeId = data.id;

    document.getElementById("title").value = data.title || "";
    document.getElementById("summary").value = data.summary || "";
}

/* AUTOSAVE */
function autosave() {

    if (!currentResumeId) return;

    clearTimeout(autosaveTimer);

    autosaveTimer = setTimeout(async () => {

        await fetch(`/resume/${currentResumeId}/autosave`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                title: document.getElementById("title").value,
                summary: document.getElementById("summary").value
            })
        });

        console.log("Autosaved");

    }, 800);
}

/* DELETE RESUME */
async function deleteResume() {

    if (!currentResumeId) return;

    await fetch(`/resume/${currentResumeId}`, {
        method: "DELETE"
    });

    currentResumeId = null;

    document.getElementById("title").value = "";
    document.getElementById("summary").value = "";

    loadResumes();
}

/* ==========================================
   ATS CHECKER
========================================== */

async function checkATS() {

    const file = document.getElementById("resumeFile");
    const job = document.getElementById("jobDesc");

    if (!file || !file.files[0]) {
        alert("Upload resume first");
        return;
    }

    const formData = new FormData();
    formData.append("resume", file.files[0]);
    formData.append("job_description", job.value);

    const res = await fetch("/ats/check", {
        method: "POST",
        body: formData
    });

    const data = await res.json();

    const score = data.score || 0;

    if (document.getElementById("score"))
        document.getElementById("score").innerText = score + "%";

    if (document.getElementById("bar"))
        document.getElementById("bar").style.width = score + "%";

    if (document.getElementById("feedback"))
        document.getElementById("feedback").innerText = data.feedback || "Done";
}

/* ==========================================
   PORTFOLIO BUILDER
========================================== */

let projects = [];

/* ADD PROJECT */
function addProject() {

    const title = document.getElementById("title");
    const desc = document.getElementById("desc");
    const link = document.getElementById("link");

    if (!title || !title.value) {
        alert("Enter project title");
        return;
    }

    projects.push({
        title: title.value,
        desc: desc.value,
        link: link.value
    });

    title.value = "";
    desc.value = "";
    link.value = "";

    renderProjects();
}

/* RENDER PROJECTS */
function renderProjects() {

    const grid = document.getElementById("portfolioGrid");
    if (!grid) return;

    grid.innerHTML = "";

    projects.forEach(p => {

        const card = document.createElement("div");
        card.className = "portfolio-card";

        card.innerHTML = `
            <div class="portfolio-header">${p.title}</div>
            <div class="portfolio-body">${p.desc}</div>
            <a href="${p.link}" target="_blank">View Project</a>
        `;

        grid.appendChild(card);
    });
}

/* ==========================================
   AUTO INIT
========================================== */

window.addEventListener("load", () => {

    if (document.getElementById("resumeList")) {
        loadResumes();
    }

    if (document.getElementById("portfolioGrid")) {
        renderProjects();
    }
});

console.log("AI Resume Builder FULL JS Loaded");