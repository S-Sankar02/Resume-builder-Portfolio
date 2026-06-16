document.addEventListener("DOMContentLoaded", function () {

    const btn = document.getElementById("atsAnalyzeBtn");

    if (!btn) return;

    btn.addEventListener("click", async function () {

        const jobDesc = document.getElementById("jobDescription").value;
        const fileInput = document.getElementById("resumeFile");

        if (!jobDesc.trim()) {
            alert("Please enter job description");
            return;
        }

        if (fileInput.files.length === 0) {
            alert("Please upload resume file");
            return;
        }

        const formData = new FormData();
        formData.append("job_description", jobDesc);
        formData.append("resume_file", fileInput.files[0]);

        try {
            const res = await fetch("/api/ats/analyze", {
                method: "POST",
                body: formData
            });

            const data = await res.json();

            console.log("API response:", data);

            if (!data.success) {
                alert(data.message);
                return;
            }

            document.getElementById("scoreValue").innerText = data.score + "%";
            document.getElementById("scoreLabel").innerText = data.label;

            document.getElementById("scoreBar").style.width = data.score + "%";

            document.getElementById("analysisText").innerText = data.analysis;

            const skillBox = document.getElementById("missingSkills");
            skillBox.innerHTML = "";

            data.missing.forEach(skill => {
                let span = document.createElement("span");
                span.className = "badge bg-danger me-1";
                span.innerText = skill;
                skillBox.appendChild(span);
            });

        } catch (err) {
            console.error(err);
            alert("ATS failed");
        }
    });
});