document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("add-project-form");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const title = document.getElementById("title").value.trim();
    const details = document.getElementById("details").value.trim();
    const target = document.getElementById("target").value;
    const startDate = document.getElementById("start_date").value;
    const endDate = document.getElementById("end_date").value;


    const today = new Date().toISOString().split("T")[0];
    if (startDate < today) {
      alert("Start date must be today or later.");
      return;
    }
    if (endDate <= startDate) {
      alert("End date must be after the start date.");
      return;
    }

    const formData = {
      title,
      details,
      target,
      start_date: startDate,
      end_date: endDate,
    };

    try {
      const response = await fetch("/projects/api/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        alert("Project created successfully!");
        window.location.href = "/";
      } else if (response.status === 403) {
        alert("You must be logged in to create a project.");
        window.location.href = "/accounts/login/";
      } else {
        const error = await response.json();
        alert("Error: " + JSON.stringify(error));
      }
    } catch (err) {
      console.error("Error creating project:", err);
      alert("Something went wrong. Please try again.");
    }
  });
});
