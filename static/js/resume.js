document.addEventListener("DOMContentLoaded", function () {
  const btn = document.getElementById("analyzeBtn");

  if (!btn) {
    console.error("Analyze button not found!");
    return;
  }

  btn.addEventListener("click", async function () {
    console.log("Button clicked ✅");

    const jobDesc = document.querySelector("textarea").value;
    const fileInput = document.querySelector("input[type='file']");
    const file = fileInput.files[0];

    if (!jobDesc) {
      alert("Please enter job description");
      return;
    }

    let resumeText = "";

    if (file) {
      resumeText = await file.text();
    }

    const response = await fetch("/api/ats/analyze", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        job_description: jobDesc,
        resume_text: resumeText,
      }),
    });

    const data = await response.json();

    console.log("API response:", data);

    if (!data.success) {
      alert(data.message);
      return;
    }

    document.querySelector(".text-center div").innerText = data.score + "%";
    document.querySelector(".progress-bar").style.width = data.score + "%";
    document.querySelector(".text-muted + p").innerText = data.analysis;
  });
});
