console.log("AI Resume Builder FULL JS Loaded");

document
  .getElementById("atsAnalyzeBtn")
  .addEventListener("click", async function () {
    const jobDescription = document
      .getElementById("jobDescription")
      .value.trim();

    const resumeFile = document.getElementById("resumeFile").files[0];

    if (!jobDescription || !resumeFile) {
      alert("Provide job description and resume");

      return;
    }

    const formData = new FormData();

    formData.append("job_description", jobDescription);

    formData.append("resume_file", resumeFile);

    try {
      const response = await fetch("/ai/api/ats/analyze", {
        method: "POST",

        body: formData,
      });

      const data = await response.json();

      console.log("ATS RESPONSE:", data);

      if (!data.success) {
        alert(data.message);

        return;
      }

      const result = data.result;

      /*
        SCORE
        */

      const scoreValue = document.getElementById("scoreValue");

      if (scoreValue) {
        scoreValue.innerText = result.score + "%";
      }

      const scoreBar = document.getElementById("scoreBar");

      if (scoreBar) {
        scoreBar.style.width = result.score + "%";
      }

      const scoreLabel = document.getElementById("scoreLabel");

      if (scoreLabel) {
        scoreLabel.innerText = "AI Analysis Complete";
      }

      /*
        ANALYSIS
        */

      const analysisText = document.getElementById("analysisText");

      if (analysisText) {
        analysisText.innerText = result.analysis || "Analysis completed";
      }

      /*
        MATCHED SKILLS
        */

      let matchedHTML = "";

      (result.matched_keywords || []).forEach((skill) => {
        matchedHTML += `

            <span class="badge bg-success m-1">

                ${skill}

            </span>

            `;
      });

      const matchedBox = document.getElementById("matchedSkills");

      if (matchedBox) {
        matchedBox.innerHTML = matchedHTML;
      }

      /*
        MISSING SKILLS
        */

      let missingHTML = "";

      (result.missing_keywords || []).forEach((skill) => {
        missingHTML += `

            <span class="badge bg-danger m-1">

                ${skill}

            </span>

            `;
      });

      const missingBox = document.getElementById("missingSkills");

      if (missingBox) {
        missingBox.innerHTML = missingHTML;
      }

      /*
        SUGGESTIONS
        */

      let suggestionHTML = "";

      (result.suggestions || []).forEach((item) => {
        suggestionHTML += `

            <li>
                ${item}
            </li>

            `;
      });

      const suggestionBox = document.getElementById("suggestions");

      if (suggestionBox) {
        suggestionBox.innerHTML = suggestionHTML;
      }
    } catch (error) {
      console.error("ATS JS ERROR:", error);

      alert("Something went wrong");
    }
  });
