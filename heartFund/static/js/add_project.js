document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("add-project-form");

  function getCSRFToken() {
    const input = document.querySelector("#csrf-form input[name=csrfmiddlewaretoken]") || document.querySelector("[name=csrfmiddlewaretoken]");
    return input ? input.value : "";
  }

  function validateDates(startDate, endDate) {
    const today = new Date().toISOString().split("T")[0];
    if (startDate < today) {
      alert("Start date must be today or later.");
      return false;
    }
    if (endDate <= startDate) {
      alert("End date must be after the start date.");
      return false;
    }
    return true;
  }

  function buildFormData() {
    const title = document.getElementById("title").value.trim();
    const details = document.getElementById("details").value.trim();
    const target = document.getElementById("target").value;
    const startDate = document.getElementById("start_date").value;
    const endDate = document.getElementById("end_date").value;

    if (!validateDates(startDate, endDate)) return null;
    if (!title || !details || !target) {
      alert("Please complete all required fields.");
      return null;
    }

    const formData = new FormData();
    formData.append("title", title);
    formData.append("details", details);
    formData.append("target", target);
    formData.append("start_date", startDate);
    formData.append("end_date", endDate);

    const fileInput = document.getElementById("cover_image");
    if (fileInput && fileInput.files && fileInput.files[0]) {
      formData.append("cover_image", fileInput.files[0]);
    }
    return formData;
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const formData = buildFormData();
    if (!formData) return;

    try {
      const response = await fetch("/projects/api/", {
        method: "POST",
        headers: { "X-CSRFToken": getCSRFToken() },
        body: formData,
      });

      if (response.ok) {
        alert("Project created successfully!");
        window.location.href = "/";
        return;
      }
      if (response.status === 403) {
        alert("You must be logged in to create a project.");
        window.location.href = "/accounts/login/";
        return;
      }
      const error = await response.json();
      alert("Error: " + JSON.stringify(error));
    } catch (err) {
      console.error("Error creating project:", err);
      alert("Something went wrong. Please try again.");
    }
  });
});
