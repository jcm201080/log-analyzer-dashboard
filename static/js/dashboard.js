/* global Chart */

document.addEventListener("DOMContentLoaded", () => {
  console.log("🚀 dashboard.js ejecutándose");

  fetch("/api/dashboard")
    .then((res) => {
      if (!res.ok) {
        throw new Error("Error al cargar datos del dashboard");
      }
      return res.json();
    })
    .then((data) => {
      console.log("Datos recibidos:", data);

      // =========================
      // RESUMEN GENERAL
      // =========================
      const totalEl = document.getElementById("total");
      if (totalEl && data.total_intentos !== undefined) {
        totalEl.textContent = `Total de intentos detectados: ${data.total_intentos}`;
      }

      // =========================
      // HOSTS MÁS AGRESIVOS
      // =========================
      const rhosts = document.getElementById("rhosts");
      if (rhosts && Array.isArray(data.hosts)) {
        rhosts.innerHTML = "";

        data.hosts
          .sort((a, b) => b.intentos - a.intentos)
          .forEach((h) => {
            const li = document.createElement("li");

            let icono = "🟢";
            if (h.gravedad === "alta") icono = "🔴";
            else if (h.gravedad === "media") icono = "🟠";

            li.textContent = `${icono} ${h.host} → ${h.intentos} intentos`;
            rhosts.appendChild(li);
          });

        crearGraficoHosts(data.hosts);
      }

      // =========================
      // USUARIOS MÁS ATACADOS
      // =========================
      const users = document.getElementById("users");
      if (users && Array.isArray(data.usuarios)) {
        users.innerHTML = "";

        data.usuarios
          .sort((a, b) => b.intentos - a.intentos)
          .forEach((u) => {
            const li = document.createElement("li");
            li.textContent = `${u.usuario} → ${u.intentos} intentos`;
            users.appendChild(li);
          });

        crearGraficoUsuarios(data.usuarios);
      }
    })
    .catch((err) => {
      console.error("❌ Error en dashboard.js:", err);
    });
});

// =========================
// GRÁFICOS
// =========================
function crearGraficoHosts(hosts) {
  const ctx = document.getElementById("hostsChart");
  if (!ctx) return;

  const top5 = hosts.slice(0, 5);

  new Chart(ctx, {
    type: "bar",
    data: {
      labels: top5.map((h) => h.host),
      datasets: [
        {
          label: "Intentos",
          data: top5.map((h) => h.intentos),
          backgroundColor: "rgba(54, 162, 235, 0.6)",
        },
      ],
    },
    options: {
      responsive: true,
    },
  });
}

function crearGraficoUsuarios(usuarios) {
  const ctx = document.getElementById("usersChart");
  if (!ctx) return;

  new Chart(ctx, {
    type: "pie",
    data: {
      labels: usuarios.map((u) => u.usuario),
      datasets: [
        {
          data: usuarios.map((u) => u.intentos),
          backgroundColor: [
            "#ff6384",
            "#36a2eb",
            "#ffce56",
            "#4bc0c0",
            "#9966ff",
          ],
        },
      ],
    },
    options: {
      responsive: true,
    },
  });
}
