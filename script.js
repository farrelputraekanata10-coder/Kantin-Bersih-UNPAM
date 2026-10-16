(() => {
  const KEY = "kantinBersihUnpamDemoReports";
  const form = document.getElementById("reportForm");
  const message = document.getElementById("formMessage");
  const section = document.getElementById("savedSection");
  const list = document.getElementById("reportList");
  function getReports() {
    try { return JSON.parse(localStorage.getItem(KEY) || "[]"); } catch (_) { return []; }
  }
  function render() {
    const reports = getReports();
    section.hidden = reports.length === 0;
    list.replaceChildren();
    reports.slice().reverse().forEach((r) => {
      const item = document.createElement("article");
      item.className = "report-item";
      const title = document.createElement("strong");
      title.textContent = r.category + " — " + r.location;
      const desc = document.createElement("p");
      desc.textContent = r.description;
      const date = document.createElement("small");
      date.textContent = new Date(r.createdAt).toLocaleString("id-ID");
      item.append(title, desc, date);
      list.append(item);
    });
  }
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const reports = getReports();
    reports.push({
      category: document.getElementById("category").value,
      location: document.getElementById("location").value.trim(),
      description: document.getElementById("description").value.trim(),
      createdAt: new Date().toISOString()
    });
    try {
      localStorage.setItem(KEY, JSON.stringify(reports));
      form.reset();
      message.textContent = "Laporan demo tersimpan di browser perangkat ini saja.";
      render();
    } catch (_) {
      message.textContent = "Browser tidak dapat menyimpan laporan. Coba hapus sebagian data browser.";
    }
  });
  document.getElementById("clearReports").addEventListener("click", () => {
    if (confirm("Hapus semua laporan demo yang tersimpan di browser ini?")) {
      localStorage.removeItem(KEY);
      message.textContent = "Laporan demo di perangkat ini sudah dihapus.";
      render();
    }
  });
  render();
})();