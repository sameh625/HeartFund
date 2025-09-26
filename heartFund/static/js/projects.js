document.addEventListener("DOMContentLoaded", () => {
  const projectsContainer = document.getElementById("projects-list");

  async function fetchProjects() {
    try {
      const response = await fetch("/projects/api/");
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
          <h3>${project.title}</h3>
          <p><strong>Publisher:</strong> ${project.owner}</p>
          <p><strong>Target:</strong> ${project.target} EGP</p>
          <p><strong>Support:</strong> ${project.payment_info}</p>
          <p><strong>Duration:</strong> ${project.start_date} → ${project.end_date}</p>
          <button class="btn-view" data-id="${project.id}">View</button>
        `;

        projectsContainer.appendChild(projectCard);
      });
    } catch (error) {
      console.error(error);
      projectsContainer.innerHTML = "<p>Failed to load projects. you have to be loged in</p>";
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
          <h2>${project.title}</h2>
          <p><strong>Publisher:</strong> ${project.owner}</p>
          <p><strong>Target:</strong> ${project.target} EGP</p>
          <p><strong>Support:</strong> ${project.payment_info}</p>
          <p><strong>Details:</strong> ${project.details}</p>
          <p><strong>Duration:</strong> ${project.start_date} → ${project.end_date}</p>
          <button id="back-btn">Back</button>
        </div>
      `;

      document.getElementById("back-btn").addEventListener("click", fetchProjects);
    } catch (error) {
      console.error(error);
    }
  }
});
  fetchProjects();
});
