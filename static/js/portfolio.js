document.addEventListener("DOMContentLoaded", function () {

    const portfolioIdEl = document.getElementById("portfolioId");

    if (!portfolioIdEl || !portfolioIdEl.value) {
        console.warn("Portfolio ID missing - skipping JS init");
        return;
    }

    const pid = portfolioIdEl.value;

    const saveBtn = document.getElementById("savePortfolioBtn");
    const exportBtn = document.getElementById("exportPortfolioBtn");

    // ======================
    // SAVE
    // ======================
    saveBtn?.addEventListener("click", async function () {

        const state = {
            hero: {
                name: document.getElementById("fullName")?.value || "",
                title: document.getElementById("title")?.value || "",
                bio: document.getElementById("about")?.value || ""
            },
            skills: (document.getElementById("skills")?.value || "")
                .split(",")
                .map(s => s.trim())
                .filter(Boolean),
            contact: {
                email: document.getElementById("email")?.value || "",
                github: document.getElementById("githubInput")?.value || "",
                linkedin: document.getElementById("linkedinInput")?.value || ""
            }
        };

        await fetch(`/portfolio/update/${pid}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(state)
        });

        alert("Saved ✅");
    });

    // ======================
    // EXPORT (FIXED)
    // ======================
    exportBtn?.addEventListener("click", function () {

        // 🔥 DIRECT DOWNLOAD (NO JSON, NO FETCH)
        window.open(`/portfolio/export/${pid}`, "_blank");
    });

});
