document.addEventListener("DOMContentLoaded", () => {
  const projectsContainer = document.getElementById("projects-list");

  async function fetchProjects(order = "latest") {
    try {
      const response = await fetch(`/projects/api/?order=${order}`);
      if (!response.ok) {
        throw new Error("Failed to fetch projects");
      }

      const projects = await response.json();

      projectsContainer.innerHTML = "";

      if (projects.length === 0) {
        projectsContainer.innerHTML = "<p>No projects available.</p>";
        return;
      }

      projects.forEach(project => {
        const projectCard = document.createElement("div");
        projectCard.className = "project-card";

        projectCard.innerHTML = `
          ${project.cover_image_url ? `<img class="project-cover" src="${project.cover_image_url}" alt="${project.title}">` : ""}
          <h3>${project.title}</h3>
          <p><strong>Publisher:</strong> ${project.owner}</p>
          <p><strong>Target:</strong> ${project.target} EGP</p>
          <p><strong>Raised:</strong> ${project.current_amount} EGP</p>
          <div class="progress"><div class="bar" style="width:${project.progress_percent || 0}%"></div></div>
          <p><strong>Duration:</strong> ${project.start_date} → ${project.end_date}</p>
          <button class="btn-view" data-id="${project.id}">View</button>
        `;

        projectsContainer.appendChild(projectCard);
      });
    } catch (error) {
      console.error(error);
      projectsContainer.innerHTML = "<p>Failed to load projects.</p>";
    }
  }
  projectsContainer.addEventListener("click", async (e) => {
  if (e.target.classList.contains("btn-view")) {
    const projectId = e.target.dataset.id;
    try {
      const response = await fetch(`/projects/api/${projectId}/`);
      if (!response.ok) throw new Error("Failed to fetch details");

      const project = await response.json();

      projectsContainer.innerHTML = `
        <div class="project-detail">
          ${project.cover_image_url ? `<img class="project-cover" src="${project.cover_image_url}" alt="${project.title}">` : ""}
          <h2>${project.title}</h2>
          <p><strong>Publisher:</strong> ${project.owner}</p>
          <p><strong>Target:</strong> ${project.target} EGP</p>
          <p><strong>Raised:</strong> ${project.current_amount} EGP</p>
          <div class="progress"><div class="bar" style="width:${project.progress_percent || 0}%"></div></div>
          <p><strong>Support:</strong> ${project.payment_info || ""}</p>
          <p><strong>Details:</strong> ${project.details}</p>
          <p><strong>Duration:</strong> ${project.start_date} → ${project.end_date}</p>
          ${project.can_donate ? `
            <div class=\"donate-box\">
              <input type=\"number\" id=\"donate-amount\" placeholder=\"Amount (EGP)\" min=\"1\">
              <button id=\"donate-btn\" data-id=\"${project.id}\">Donate</button>
            </div>
          ` : `<p class=\"donate-disabled\" style=\"color: red;\">${project.is_fully_funded ? 'This project is fully funded.' : 'You cannot donate to this project.'}</p>`}
          <div id="contrib-list"></div>
          <button id="back-btn">Back</button>
        </div>
      `;

      document.getElementById("back-btn").addEventListener("click", fetchProjects);

      try {
        const clRes = await fetch(`/projects/api/${projectId}/contributions/`);
        if (clRes.ok) {
          const items = await clRes.json();
          const list = document.getElementById("contrib-list");
          list.innerHTML = `<h3>Recent Contributions</h3>` + (items.length ? items.map(c => `<p>+${c.amount} by ${c.donor_name}</p>`).join("") : "<p>No contributions yet.</p>");
        }
      } catch {}

      const donateBtn = document.getElementById("donate-btn");
      if (donateBtn) donateBtn.addEventListener("click", async (ev) => {
        const amt = document.getElementById("donate-amount").value;
        const res = await fetch(`/projects/api/${projectId}/contributions/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(),
          },
          body: JSON.stringify({ amount: amt })
        });
        if (res.ok) {
          alert("Thank you for your contribution!");
          const back = document.getElementById("back-btn");
          back.click();
          setTimeout(() => {
            document.querySelector(`.btn-view[data-id='${projectId}']`).click();
          }, 100);
        } else if (res.status === 403) {
          alert("You must be logged in to donate.");
          window.location.href = "/accounts/login/";
        } else {
          try {
            const err = await res.json();
            alert(Object.values(err).flat().join("\n"));
          } catch {
            alert("Failed to donate.");
          }
        }
      });
    } catch (error) {
      console.error(error);
    }
  }
});
  fetchProjects();

  const orderSelect = document.getElementById("order");
  if (orderSelect) {
    orderSelect.addEventListener("change", () => fetchProjects(orderSelect.value));
  }

  function getCSRFToken() {
    const input = document.querySelector("#csrf-form input[name=csrfmiddlewaretoken]") || document.querySelector("[name=csrfmiddlewaretoken]");
    return input ? input.value : "";
  }
});
