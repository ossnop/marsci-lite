/* ===== Language hook: safe attach (waits for DOM + marSciSetLang) ===== */
(function(){
  function attachLangHook(){
    if(window.marSciSetLang && !window.__marsci_lang_hooked){
      const originalSetLang = window.marSciSetLang;
      window.marSciSetLang = function(mode){
        try { originalSetLang(mode); } catch(e){ console.warn('marSciSetLang original threw', e); }
        if (typeof window.marSciRepopulateIndustries === 'function') {
          try { window.marSciRepopulateIndustries(); } catch(e){ console.error('repopulate failed', e); }
        }
      };
      window.__marsci_lang_hooked = true;
      // Also call once to sync UI on attach (in case language already set)
      try { if (typeof window.marSciRepopulateIndustries === 'function') window.marSciRepopulateIndustries(); } catch(e){}
    }
  }

  document.addEventListener('DOMContentLoaded', attachLangHook);
  // In case marSciSetLang defined after DOMContentLoaded, try again a short while later
  setTimeout(attachLangHook, 500);
  setTimeout(attachLangHook, 1500);
})();

/* ===== MarSci Lite — FRONTEND CONTROLLER (CLEAN VERSION) =====
   รองรับการวางค่าจาก Excel / Sheets ทุกแบบ
   Note: all DOM selectors and event wiring executed after DOMContentLoaded for safety.
=================================================================*/
document.addEventListener('DOMContentLoaded', function(){

  /* normalizeKPIInput: รองรับ comma, tab, newline, space, NBSP */
  function normalizeKPIInput(rawText) {
    try {
      if (!rawText || typeof rawText !== "string") return [];

      var txt = rawText.replace(/\r\n/g, "\n").replace(/\u00A0/g, " ");
      txt = txt.replace(/\t+/g, ",")
               .replace(/\n+/g, ",")
               .replace(/ +/g, ",")
               .replace(/,+/g, ",")
               .trim();

      if (txt === "") return [];

      var parts = txt.split(",").map(function(s){ return s.trim(); }).filter(function(s){ return s.length > 0; });

      var nums = parts.map(function(p){
        var cleaned = p.replace(/[^\d\.\-eE,]/g, "");
        if (cleaned.indexOf('.') === -1 && (cleaned.match(/,/g) || []).length === 1) {
          cleaned = cleaned.replace(',', '.');
        }
        var n = parseFloat(cleaned);
        return isNaN(n) ? null : n;
      }).filter(function(v){ return v !== null; });

      return nums;

    } catch (e) {
      console.error("normalizeKPIInput ERROR:", e);
      return [];
    }
  }

  /* UI selectors (safe after DOM ready) */
  const industryEl = document.querySelector('#industry');
  const startDate = document.querySelector('#start-date');
  const endDate = document.querySelector('#end-date');
  const analyzeBtn = document.querySelector('#analyze');
  const resultBox = document.querySelector('#result-box');

  /* Build payload */
  function getPayload() {
    const sd = startDate ? startDate.value : null;
    const ed = endDate ? endDate.value : null;
    let days = 0;
    if (sd && ed) {
      const s = new Date(sd), e = new Date(ed);
      days = Math.floor((e - s) / (1000*60*60*24)) + 1;
    }
    const kpiButtons = document.querySelectorAll(".kpi-btn.active");
    const selectedKPIs = Array.from(kpiButtons).map(b => b.dataset.kpi);
    const dailyAreas = document.querySelectorAll(".kpi-values");
    let kpis = [];
    dailyAreas.forEach((area, idx) => {
      const raw = area.value || "";
      const cleaned = normalizeKPIInput(raw);
      kpis.push({ name: selectedKPIs[idx] || ("KPI_" + (idx+1)), daily_values: cleaned });
    });
    return {
      industry: (industryEl && industryEl.value) ? industryEl.value : null,
      start_date: sd || null,
      end_date: ed || null,
      days: days,
      kpis: kpis
    };
  }

  /* Send and render */
  async function sendAnalyze(payload) {
    try {
      const res = await fetch("http://localhost:8000/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      if (!res.ok) {
        resultBox.innerHTML = `<div class='error'>Error: ${data.detail || JSON.stringify(data)}</div>`;
        return;
      }
      const displayed = data.results && data.results.length ? data.results[0] : data;
      resultBox.innerHTML = `<div class="card"><h3>${displayed.kpi||'Result'}</h3>
        <p>Severity: <strong>${displayed.severity||'N/A'}</strong></p>
        <p>Benchmark: ${displayed.benchmark_min||'-'} – ${displayed.benchmark_max||'-'}</p>
        <p>${displayed.summary||''}</p>
        <p class="small">${displayed.timestamp||data.timestamp||''}</p></div>`;
    } catch (e) {
      console.error(e);
      resultBox.innerHTML = `<div class='error'>Connection failed</div>`;
    }
  }

  /* Hook analyze button */
  if (analyzeBtn) {
    analyzeBtn.addEventListener("click", async () => {
      const payload = getPayload();
      console.log("PAYLOAD:", payload);
      await sendAnalyze(payload);
    });
  } else {
    console.warn("analyze button not found (#analyze).");
  }

}); // end DOMContentLoaded
