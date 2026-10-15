const input = document.getElementById("imageInput");
const fileLabel = document.getElementById("fileLabel");
const analyzeBtn = document.getElementById("analyzeBtn");
const resultPanel = document.getElementById("resultPanel");
const resultContent = document.getElementById("resultContent");
const placeholder = resultPanel.querySelector(".placeholder");
const muted = resultPanel.querySelector(".muted");

input.addEventListener("change", () => {
  fileLabel.textContent = input.files.length ? input.files[0].name : "Click to choose an image";
});

function makeList(items) {
  return `<ul class="result-list">${items.map(item => `<li>${escapeHtml(item)}</li>`).join("")}</ul>`;
}
function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, ch => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;"
  }[ch]));
}

analyzeBtn.addEventListener("click", async () => {
  if (!input.files.length) {
    alert("Please choose an image first.");
    return;
  }
  const formData = new FormData();
  formData.append("image", input.files[0]);
  analyzeBtn.disabled = true;
  analyzeBtn.innerHTML = "Analyzing…";
  try {
    const response = await fetch("/api/analyze", { method: "POST", body: formData });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Something went wrong.");
    placeholder.hidden = true;
    muted.hidden = true;
    resultContent.hidden = false;
    resultContent.innerHTML = `
      <div class="status">ANALYSIS COMPLETE · PROTOTYPE</div>
      <h3 style="margin-top:12px">${escapeHtml(data.item)}</h3>
      <div class="result-label">ILLUSTRATIVE CO₂ IMPACT</div>
      <div class="impact-value">${escapeHtml(data.co2_saved_kg)} kg <span style="font-size:12px;color:#718076">potentially avoided*</span></div>
      <div class="result-label">REUSE IDEAS</div>${makeList(data.reuse)}
      <div class="result-label">SAFE RECYCLING</div>${makeList(data.recycle)}
      <div class="notice">${escapeHtml(data.note)}<br><br>*Impact is an illustrative estimate, not a verified lifecycle calculation. Follow local e-waste rules.</div>`;
  } catch (error) {
    alert(error.message);
  } finally {
    analyzeBtn.disabled = false;
    analyzeBtn.innerHTML = 'Analyze item <span>→</span>';
  }
});
