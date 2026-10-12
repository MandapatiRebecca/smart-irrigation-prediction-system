const $ = (id) => document.getElementById(id);

function setReadings(m, t, h) {
  $("mMoisture").textContent = `${m}%`;
  $("mTemp").textContent = `${t}°C`;
  $("mHumidity").textContent = `${h}%`;
}

async function runPrediction(event) {
  if (event) event.preventDefault();
  const payload = {
    moisture: Number($("moisture").value),
    temperature: Number($("temperature").value),
    humidity: Number($("humidity").value),
    rain_expected: $("rain").checked
  };
  $("formMessage").textContent = "Sending readings to the backend…";
  try {
    const response = await fetch("/api/predict", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(payload)
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Prediction failed.");
    setReadings(payload.moisture, payload.temperature, payload.humidity);
    $("mWater").textContent = `${data.estimated_water_litres} L`;
    $("resultTitle").textContent = data.recommendation;
    $("resultReason").textContent = data.reason;
    $("resultWater").textContent = `${data.estimated_water_litres} L`;
    $("resultScore").textContent = data.score;
    $("resultIcon").textContent = data.irrigation_needed ? "💧" : "🌿";
    $("formMessage").textContent = "Prediction completed and saved to history.";
    await loadHistory();
  } catch (error) {
    $("formMessage").textContent = error.message + " Is the Flask server running?";
  }
}

async function loadHistory() {
  try {
    const response = await fetch("/api/history");
    const rows = await response.json();
    const body = $("historyBody");
    if (!rows.length) {
      body.innerHTML = '<tr><td colspan="3" class="muted">No predictions yet. Submit sensor readings to start.</td></tr>';
      return;
    }
    body.innerHTML = rows.map(row => `
      <tr>
        <td>${escapeHtml(row.time.split(" ")[1] || row.time)}</td>
        <td>${row.moisture}%</td>
        <td><span class="tag ${row.irrigation_needed ? "yes" : "no"}">${row.irrigation_needed ? "WATER" : "NO WATER"}</span></td>
      </tr>`).join("");
  } catch {
    $("historyBody").innerHTML = '<tr><td colspan="3" class="muted">Could not load history.</td></tr>';
  }
}

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, ch => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"}[ch]));
}

async function togglePump() {
  const enabled = $("pumpSwitch").checked;
  try {
    const response = await fetch("/api/pump", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({enabled})
    });
    const data = await response.json();
    $("pumpChip").textContent = enabled ? "ON (DEMO)" : "OFF";
    $("pumpMessage").textContent = data.message;
  } catch {
    $("pumpMessage").textContent = "Could not reach backend.";
    $("pumpSwitch").checked = false;
  }
}

$("predictForm").addEventListener("submit", runPrediction);
$("refreshHistory").addEventListener("click", loadHistory);
$("pumpSwitch").addEventListener("change", togglePump);
setReadings(24, 31, 48);
loadHistory();
