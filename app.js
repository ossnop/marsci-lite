// Minimal frontend analyzer (no backend)
// Thresholds for sd% to level mapping (as agreed): Slightly: 7-12%, Mid: 13-18%, High: 19-24%, VeryHigh: >=25%
// We'll compute sd% = (stddev / mean) * 100
(function(){
  const industryList = [
    {"id":"spa","name_th":"สปา / นวดเพื่อสุขภาพ","name_en":"Spa & Wellness"},
    {"id":"retail","name_th":"ค้าปลีก","name_en":"Retail"},
    {"id":"ecom","name_th":"อีคอมเมิร์ซ","name_en":"E-commerce"},
    {"id":"hotel","name_th":"โรงแรม/ที่พัก","name_en":"Hotel / Accommodation"}
    // expand in industry-list.json if needed
  ];

  const kpis = ["CPM","VTR","CPV","ER","CPE","CTR","CPC","CVR","CPA"];

  function qsel(s){return document.querySelector(s)}
  function qall(s){return Array.from(document.querySelectorAll(s))}

  // populate selects
  const industry = qsel("#industry");
  industryList.forEach(i=>{
    const opt = document.createElement('option');
    opt.value = i.id; opt.textContent = i.name_th + " / " + i.name_en;
    industry.appendChild(opt);
  });

  qall(".kpi-select").forEach(s=>{
    kpis.forEach(k=>{
      const o = document.createElement('option'); o.value = k; o.textContent = k; s.appendChild(o);
    });
  });

  function parseValues(text){
    if(!text) return [];
    // accept comma or newline separated
    const items = text.split(/\r?\n|,/).map(t=>t.trim()).filter(Boolean);
    const nums = items.map(x=>{ const n = parseFloat(x.replace(/,/g,'')); return isNaN(n)?null:n });
    return nums.filter(n=>n!==null);
  }

  function mean(arr){ return arr.reduce((a,b)=>a+b,0)/arr.length }
  function stddev(arr,m){
    const mm = typeof m === 'number' ? m : mean(arr);
    const v = arr.reduce((s,x)=>s+Math.pow(x-mm,2),0) / arr.length;
    return Math.sqrt(v);
  }

  function determineAnomaly(sdPercent){
    // thresholds based on agreed bands
    // Slightly: 7–12% ; Mid: 13–18% ; High: 19–24% ; VeryHigh: >=25%
    if(sdPercent < 7) return {label:"Stable", color:"green"};
    if(sdPercent <= 12) return {label:"Slightly Volatile", color:"#e6a600"};
    if(sdPercent <= 18) return {label:"Moderate Anomaly", color:"#ff7a00"};
    if(sdPercent <= 24) return {label:"High Anomaly", color:"#ff3b30"};
    return {label:"Very High Anomaly", color:"#b00020"};
  }

  qsel("#runBtn").addEventListener('click', ()=>{
    // pick first non-empty KPI
    const k = qall(".kpi-select").map(s=>s.value).filter(Boolean)[0];
    if(!k){ alert("เลือก KPI 1 ตัวอย่างน้อย"); return; }
    const vals = parseValues(qsel("#dailyValues").value);
    if(vals.length < 5){ alert("ข้อมูลน้อยเกินไปสำหรับการคำนวณ (แนะนำ >=5 วัน)"); return; }
    // compute
    const m = mean(vals); const sd = stddev(vals,m);
    const sdPercent = m===0?0: Math.abs(sd/m)*100;
    // baseline (benchmark) simple: lower = mean - sd, upper = mean + sd (but constrained)
    const lower = Math.max(0, m - sd);
    const upper = m + sd;
    const anomaly = determineAnomaly(sdPercent);

    // render result
    document.querySelector("#result").classList.remove('hide');
    qsel("#rKpi").textContent = k;
    qsel("#benchRange").textContent = (lower.toFixed(4)) + "  ⁓  " + (upper.toFixed(4));
    qsel("#benchMeta").textContent = "(mean: " + m.toFixed(4) + " · sd: " + sd.toFixed(4) + " · N=" + vals.length + ")";
    qsel("#benchRec").textContent = "แนะนำ: ใช้ช่วงนี้เป็นกรอบอ้างอิงสำหรับการตรวจสอบต่อไป";

    qsel("#anomStatus").textContent = anomaly.label;
    qsel("#anomStatus").style.color = anomaly.color;
    qsel("#anomMeta").textContent = "sd%: " + sdPercent.toFixed(1) + " · N=" + vals.length;
    qsel("#anomRec").textContent = anomaly.label === 'Stable' ? "ค่าคงที่ดี ยังไม่พบสัญญาณผิดปกติ" : "แนะนำตรวจ KPI อื่นๆ เพิ่มเติมเพื่อยืนยันสัญญาณ";
    window.scrollTo({top: document.querySelector("#result").offsetTop - 20, behavior:'smooth'});
  });

  qsel("#clearBtn").addEventListener('click', ()=>{
    qsel("#dailyValues").value=''; qall(".kpi-select").forEach(s=>s.selectedIndex=0);
    qsel("#result").classList.add('hide');
  });

  qsel("#checkMore").addEventListener('click', ()=>{
    window.scrollTo({top: document.querySelector("#analyzeForm").offsetTop - 20, behavior:'smooth'});
  });

})();