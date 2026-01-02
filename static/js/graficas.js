/* global Chart */

let hostsChartInstance = null;
let usersChartInstance = null;
let countriesChartInstance = null;

document.addEventListener("DOMContentLoaded", () => {
  fetch("/api/dashboard")
    .then((res) => res.json())
    .then((data) => {
      if (data.hosts) {
        crearGraficoHosts(data.hosts);
        crearGraficoPaises(data.hosts);
      }
      if (data.usuarios) {
        crearGraficoUsuarios(data.usuarios);
      }
    })
    .catch((err) => console.error("Error cargando gráficas:", err));
});

// =========================
// GRÁFICOS HOSTS
// =========================
function crearGraficoHosts(hosts) {
  const ctx = document.getElementById("hostsChart");
  if (!ctx) return;

  if (hostsChartInstance) hostsChartInstance.destroy();

  const top10 = hosts.slice(0, 10);

  hostsChartInstance = new Chart(ctx, {
    type: "bar",
    data: {
      labels: top10.map((h) => h.host),
      datasets: [
        {
          label: "Intentos",
          data: top10.map((h) => h.intentos),
          backgroundColor: "rgba(54, 162, 235, 0.6)",
        },
      ],
    },
    options: {
      responsive: true,
    },
  });
}

// =========================
// GRÁFICOS USUARIOS
// =========================
function crearGraficoUsuarios(usuarios) {
  const ctx = document.getElementById("usersChart");
  if (!ctx) return;

  if (usersChartInstance) usersChartInstance.destroy();

  const top10 = usuarios.slice(0, 10);

  usersChartInstance = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: top10.map((u) => u.usuario),
      datasets: [
        {
          data: top10.map((u) => u.intentos),
          backgroundColor: [
            "#ff6384",
            "#36a2eb",
            "#ffce56",
            "#4bc0c0",
            "#9966ff",
            "#1cc88a",
            "#e74a3b",
          ],
        },
      ],
    },
    options: {
      responsive: true,
    },
  });
}

// =========================
// GRÁFICO POR PAÍS (heurístico)
// =========================
function crearGraficoPaises(hosts) {
  const ctx = document.getElementById("countriesChart");
  if (!ctx) return;

  if (countriesChartInstance) countriesChartInstance.destroy();

  const conteo = {};

  hosts.forEach((h) => {
    const host = h.host.toLowerCase();
    let pais = "Otros";

    if (host.endsWith(".ru")) pais = "Rusia";
    else if (host.endsWith(".cn")) pais = "China";
    else if (host.endsWith(".br")) pais = "Brasil";
    else if (host.endsWith(".net") || host.endsWith(".com"))
      pais = "Internacional";
    else if (/^\d+\.\d+\.\d+\.\d+$/.test(host)) pais = "IP desconocida";

    conteo[pais] = (conteo[pais] || 0) + h.intentos;
  });

  const labels = Object.keys(conteo);
  const values = labels.map((p) => conteo[p]);

  countriesChartInstance = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels,
      datasets: [
        {
          data: values,
          backgroundColor: [
            "#e74a3b",
            "#f6c23e",
            "#36b9cc",
            "#4e73df",
            "#858796",
          ],
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: "bottom",
        },
      },
    },
  });
}
