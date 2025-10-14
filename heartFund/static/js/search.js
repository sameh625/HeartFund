document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("search-form");
  const projectsContainer = document.getElementById("projects-list");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const start = document.getElementById("start-date").value;
    const end = document.getElementById("end-date").value;

    try {
      const order = document.getElementById("order") ? document.getElementById("order").value : "latest";
      const response = await fetch(`/projects/api/search/?start=${start}&end=${end}&order=${order}`);
      if (!response.ok) throw new Error("Search failed");

      const projects = await response.json();

      projectsContainer.innerHTML = "";

      if (projects.length === 0) {
        projectsContainer.innerHTML = "<p>No projects found in this range.</p>";
        return;
      }

      projects.forEach(p => {
        const card = document.createElement("div");
        card.className = "project-card";
        card.innerHTML = `
          ${p.cover_image_url ? `<img class="project-cover" src="${p.cover_image_url}" alt="${p.title}">` : ""}
          <h3>${p.title}</h3>
          <p><strong>Publisher:</strong> ${p.owner}</p>
          <p><strong>Target:</strong> ${p.target} EGP</p>
          <p><strong>Raised:</strong> ${p.current_amount} EGP</p>
          <div class="progress"><div class="bar" style="width:${p.progress_percent || 0}%"></div></div>
          <p><strong>Duration:</strong> ${p.start_date} → ${p.end_date}</p>
          <button class="btn-view" data-id="${p.id}">View</button>
        `;
        projectsContainer.appendChild(card);
      });

    } catch (err) {
      console.error(err);
      projectsContainer.innerHTML = "<p>Error performing search.</p>";
    }
  });
});
