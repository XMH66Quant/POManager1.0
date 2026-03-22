// ✅ Restore API key + file list
window.onload = function () {
  const savedKey = localStorage.getItem("api_key");
  if (savedKey) {
    document.getElementById("api_key").value = savedKey;
  }

  const savedFiles = JSON.parse(localStorage.getItem("file_names") || "[]");
  if (savedFiles.length > 0) {
    document.getElementById("fileName").innerText =
      "Last selected files: " + savedFiles.join(", ");
  }
};


// ✅ Validate form + store values
function validateForm() {
  const apiKey = document.getElementById("api_key").value.trim();
  const fileInput = document.getElementById("fileInput");
  const error = document.getElementById("apiError");

  if (!apiKey) {
    error.style.display = "block";
    return false;
  }

  if (!fileInput.files.length) {
    alert("Please select at least one PDF");
    return false;
  }

  localStorage.setItem("api_key", apiKey);

  const names = Array.from(fileInput.files).map(f => f.name);
  localStorage.setItem("file_names", JSON.stringify(names));

  error.style.display = "none";
  return true;
}


// ✅ Show selected files instantly
document.addEventListener("DOMContentLoaded", function () {
  const fileInput = document.getElementById("fileInput");
  const fileName = document.getElementById("fileName");

  fileInput.addEventListener("change", function () {
    if (fileInput.files.length > 0) {
      const names = Array.from(fileInput.files).map(f => f.name);
      fileName.innerText = "Selected: " + names.join(", ");
    }
  });
});


// ✅ Download JSON
function downloadJSON() {
  const data = document.getElementById("jsonData").innerText;
  const blob = new Blob([data], { type: "application/json" });
  const url = URL.createObjectURL(blob);

  const a = document.createElement("a");
  a.href = url;
  a.download = "output.json";
  a.click();
}


// ✅ Download CSV
function downloadCSV() {
  let table = document.querySelector("table");
  let rows = table.querySelectorAll("tr");

  let csv = [];
  rows.forEach(row => {
    let cols = row.querySelectorAll("td, th");
    let line = Array.from(cols).map(c => `"${c.innerText}"`).join(",");
    csv.push(line);
  });

  const blob = new Blob([csv.join("\n")], { type: "text/csv" });
  const url = URL.createObjectURL(blob);

  const a = document.createElement("a");
  a.href = url;
  a.download = "output.csv";
  a.click();
}