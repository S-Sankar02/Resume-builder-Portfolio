document.addEventListener("DOMContentLoaded", function () {
  const btn = document.getElementById("atsAnalyzeBtn");
  if (!btn) return;
  btn.addEventListener("click", async function () {
    const jobDesc = document.getElementById("jobDescription").value;
    const fileInput = document.getElementById("resumeFile");
    if (!jobDesc.trim()) {
      showToast("Please enter job description");
      return;
    }
    if (fileInput.files.length === 0) {
      showToast("Please upload resume file", "danger");
      return;
    }
    const formData = new FormData();
    formData.append("job_description", jobDesc);
    formData.append("resume_file", fileInput.files[0]);
    try {
      const res = await fetch("/api/ats/analyze", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      console.log("API response:", data);
      if (!data.success) {
        showToast(data.message || "Analysis failed", "danger");
        return;
      }
      document.getElementById("scoreValue").innerText = data.score + "%";
      document.getElementById("scoreLabel").innerText = data.label;
      document.getElementById("scoreBar").style.width = data.score + "%";
      document.getElementById("analysisText").innerText = data.analysis;
      const skillBox = document.getElementById("missingSkills");
      skillBox.innerHTML = "";
      if (data.missing.length > 0) {
        data.missing.forEach((skill) => {
          let span = document.createElement("span");
          span.className = "badge bg-danger me-1";
          span.innerText = skill;
          skillBox.appendChild(span);
        });
      } else {
        skillBox.innerHTML = `<span class="badge bg-success">
                    No missing skills 🎉
                 </span>`;
      }
      showToast("ATS analysis completed successfully", "success");
    } catch (err) {
      console.error(err);
      showToast("ATS analysis failed", "danger");
    }
  });
});
function showToast(message, type = "primary") {
  const toast = document.getElementById("atsToast");
  const text = document.getElementById("toastMessage");
  if (!toast || !text) {
    console.log(message);
    return;
  }
  text.innerText = message;
  toast.className =
    "toast align-items-center text-white bg-" + type + " border-0";
  const bsToast = new bootstrap.Toast(toast);
  bsToast.show();
}
function showToast(message, type = "primary") {
  let toast = document.getElementById("atsToast");

  let text = document.getElementById("toastMessage");

  text.innerHTML = message;

  toast.className =
    "toast align-items-center text-white bg-" + type + " border-0";

  let bsToast = new bootstrap.Toast(toast);

  bsToast.show();
}
