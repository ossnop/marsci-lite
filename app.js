/* Frontend logic (demo) */
const INDUSTRIES_URL = 'industry-list.json';
const KPI_DEFS = [
  {id:'cpm', label:'CPM'},
  {id:'vtr', label:'VTR (%)'},
  {id:'cpv', label:'CPV'},
  {id:'er', label:'ER (%)'},
  {id:'cpe', label:'CPE'},
  {id:'ctr', label:'CTR (%)'},
  {id:'cpc', label:'CPC'},
  {id:'cvr', label:'CVR (%)'},
  {id:'cpa', label:'CPA'}
];

async function loadIndustries(){
  try{
    const r = await fetch(INDUSTRIES_URL);
    const j = await r.json();
    const sel = document.getElementById('industry');
    sel.innerHTML = '';
    j.sort((a,b)=> (a.name_en||'').localeCompare(b.name_en)).forEach(it=>{
      const opt = document.createElement('option');
      opt.value = it.id;
      opt.textContent = it.name_en + ' / ' + it.name_th;
      sel.appendChild(opt);
    });
  }catch(e){
    console.warn('No industry list', e);
  }
}

function buildKPISelects(){
  const container = document.getElementById('kpi-selects');
  container.innerHTML = '';
  for(let i=0;i<3;i++){
    const sel = document.createElement('select');
    sel.className='kpi-select';
    sel.dataset.idx = i;
    const empty = document.createElement('option'); empty.value=''; empty.textContent='-- เลือก KPI --'; sel.appendChild(empty);
    KPI_DEFS.forEach(k=>{
      const o = document.createElement('option');
      o.value = k.id; o.textContent = k.label;
      sel.appendChild(o);
    });
    container.appendChild(sel);
  }
}

function parseValues(text){
  if(!text) return [];
  const parts = text.split(/[\r\n,]+/).map(s=>s.trim()).filter(Boolean);
  const nums = parts.map(s=> Number(s.replace(/%/g,''))).filter(n=> !isNaN(n));
  return nums;
}

function mean(arr){ if(!arr.length) return null; return arr.reduce((a,b)=>a+b,0)/arr.length; }
function median(arr){ if(!arr.length) return null; const s=[...arr].sort((a,b)=>a-b); const m=Math.floor(s.length/2); return s.length%2? s[m] : (s[m-1]+s[m])/2; }
function sd(arr){ if(!arr.length) return null; const m=mean(arr); const v=arr.reduce((s,x)=>s+Math.pow(x-m,2),0)/arr.length; return Math.sqrt(v); }
function sdPercent(sdVal, meanVal){ if(meanVal === 0 || meanVal === null) return sdVal*100; return Math.abs(sdVal / meanVal) * 100; }

function anomalyLevelFromSdPercent(p){
  if(p < 7) return {label:'Stable', cls:'badge-stable'};
  if(p < 13) return {label:'Slightly', cls:'badge-slight'};
  if(p < 19) return {label:'Moderate', cls:'badge-slight'};
  if(p < 25) return {label:'High', cls:'badge-high'};
  return {label:'Severe', cls:'badge-high'};
}

function formatPercent(v){
  if (v === null || v === undefined) return 'n/a';
  return v.toFixed(2);
}

function renderResultForKPI(kpiLabel, arr){
  const container = document.createElement('div');
  container.className = 'result-card';
  const n = arr.length;
  const m = mean(arr);
  const med = median(arr);
  const s = sd(arr);
  const sdP = sdPercent(s, m);

  const lower = med - s;
  const upper = med + s;

  const anomaly = anomalyLevelFromSdPercent(sdP);

  container.innerHTML = `
    <div class="result-header"><div class="kpi-name">${kpiLabel}</div><div class="small">N=${n} · sd%=${sdP.toFixed(2)}%</div></div>
    <div class="kpi-pair">
      <div class="kpi-left">
        <div class="kpi-name">ค่ากลาง (Benchmark)</div>
        <div class="range">${formatPercent(lower)} ⁓ ${formatPercent(upper)}</div>
        <div class="small">(คำนวณจาก median ± 1·sd)</div>
      </div>
      <div class="kpi-right">
        <div class="kpi-name">ค่าผิดปกติ (Anomaly)</div>
        <div class="${anomaly.cls}">${anomaly.label}</div>
        <div class="reco"><strong>คำแนะนำ:</strong> หากสถานะไม่ Stable ให้ตรวจ KPI อื่นที่เกี่ยวข้อง</div>
        <div class="small">(${sdP.toFixed(2)}% · N=${n})</div>
        <div style="margin-top:8px">
          <button class="btn" onclick="addMore()">ตรวจ KPI เพิ่ม</button>
          <button class="btn" onclick="showDetails('${kpiLabel.replace(/'/g,'')}')">ดูรายละเอียด</button>
        </div>
      </div>
    </div>
  `;
  return container;
}

function addMore(){ alert('กดเพื่อตรวจ KPI เพิ่ม — จะเปิดช่องเลือก KPI ใหม่'); }
function showDetails(kpi){ alert('รายละเอียดสำหรับ ' + kpi + '\\n(ฟีเจอร์รายละเอียดยังเป็นเวอร์ชันตัวอย่าง)'); }

document.getElementById('startBtn')?.addEventListener('click', ()=>{ document.getElementById('values')?.focus(); });

document.getElementById('run')?.addEventListener('click', ()=>{
  const selects = Array.from(document.querySelectorAll('.kpi-select')).map(s=>s.value).filter(Boolean);
  if(selects.length === 0) { alert('กรุณาเลือก KPI อย่างน้อย 1 ตัว'); return; }
  const vals = parseValues(document.getElementById('values').value);
  if(vals.length < 3) { alert('ข้อมูลน้อยเกินไป — กรุณาใส่อย่างน้อย 3 ค่าเพื่อผลที่ไม่ผันผวนมาก'); return; }
  const resultsArea = document.getElementById('result-area');
  resultsArea.innerHTML = '';
  selects.forEach(id => {
    const def = KPI_DEFS.find(k=>k.id===id) || {label:id.toUpperCase()};
    const card = renderResultForKPI(def.label, vals);
    resultsArea.appendChild(card);
  });
});

document.getElementById('clear')?.addEventListener('click', ()=>{
  document.getElementById('values').value='';
  document.getElementById('result-area').innerHTML='';
  Array.from(document.querySelectorAll('.kpi-select')).forEach(s=>s.value='');
});

loadIndustries();
buildKPISelects();
