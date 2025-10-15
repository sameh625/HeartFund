document.addEventListener("DOMContentLoaded", () => {
  const container = document.getElementById("my-projects-list");

  async function fetchMyProjects() {
    try {
      const response = await fetch("/projects/api/mine/");
      if (!response.ok) throw new Error("Failed to fetch projects");

      const projects = await response.json();
      container.innerHTML = "";

      if (projects.length === 0) {
        container.innerHTML = "<p>You have no campaigns yet.</p>";
        return;
      }

      projects.forEach((p) => {
        const card = document.createElement("div");
        card.className = "project-card";

        card.innerHTML = `
        <h3>${p.title}</h3>
        <p><strong>Target:</strong> ${p.target} EGP</p>
        <p><strong>Raised:</strong> ${p.current_amount} EGP</p>
        <p><strong>Duration:</strong> ${p.start_date} → ${p.end_date}</p>
        <button class="edit-btn" onclick="openEditForm(${p.id}, '${p.title}', '${p.details}', ${p.target}, '${p.start_date}', '${p.end_date}')">Edit</button>
        <button class="delete-btn" onclick="deleteProject(${p.id})">Delete</button>
        `;
        container.appendChild(card);
      });
    } catch (err) {
      console.error(err);
      container.innerHTML = "<p>Error loading projects.</p>";
    }
  }

  fetchMyProjects();

  window.deleteProject = async function (id) {
    if (!confirm("Are you sure you want to delete this campaign?")) return;

    const response = await fetch(`/projects/api/${id}/`, {
      method: "DELETE",
      headers: {
        "X-CSRFToken": getCSRFToken(),
      },
    });

    if (response.ok) {
      alert("Campaign deleted!");
      fetchMyProjects();
    } else {
      const error = await response.text();
      console.error(error);
      alert("Failed to delete campaign: " + error);
    }
  };

  window.openEditForm = function (
    id,
    title,
    details,
    target,
    start_date,
    end_date
  ) {
    container.innerHTML = `
      <div class="add-project-container">
        <h2>Edit Campaign</h2>
        <form id="edit-form">
          <label>Title</label>
          <input type="text" id="edit-title" value="${title}" required>

          <label>Details</label>
          <textarea id="edit-details" required>${details}</textarea>

          <label>Target</label>
          <input type="number" id="edit-target" value="${target}" required>

          <label>Start Date</label>
          <input type="date" id="edit-start" value="${start_date}" required>

          <label>End Date</label>
          <input type="date" id="edit-end" value="${end_date}" required>

          <button class="save" type="submit">Save Changes</button>
          <button class="cancel" type="button" onclick="window.location.href='/projects/mine/'">Cancel</button>
        </form>
      </div>
    `;

    document
      .getElementById("edit-form")
      .addEventListener("submit", async (e) => {
        e.preventDefault();

        const updated = {
          title: document.getElementById("edit-title").value,
          details: document.getElementById("edit-details").value,
          target: document.getElementById("edit-target").value,
          start_date: document.getElementById("edit-start").value,
          end_date: document.getElementById("edit-end").value,
        };

        const response = await fetch(`/projects/api/${id}/`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(),
          },
          body: JSON.stringify(updated),
        });

        if (response.ok) {
          alert("Project updated!");
          fetchMyProjects();
        } else {
          alert("Failed to update project.");
        }
      });
  };

  function getCSRFToken() {
    return document.querySelector("#csrf-form input[name=csrfmiddlewaretoken]").value;
  }
});
