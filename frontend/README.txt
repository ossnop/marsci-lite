MarSci Lite — Ready Release (Frontend bundle)
(C) 2025 Annop Sripuna

ไฟล์ในแพ็ก:
 - frontend/index.html        (หน้า UI ภาษาไทย - mobile + desktop responsive)
 - frontend/styles.css        (สไตล์หลัก)
 - frontend/app.js           (เชื่อม frontend -> backend, export CSV)
 - logo.png                  (โลโก้สำหรับแสดงใน header)
 - manifest.txt              (รายการไฟล์ในแพ็ก)

คำสั่งรันอย่างย่อ (Local test)
1) เปิด terminal ไปที่โฟลเดอร์ frontend:
   cd <path-to-extracted>/frontend

2) เรียก http server (Python ต้องติดตั้ง):
   python -m http.server 8001

3) Backend (ต้องรันแยกหน้าต่าง Powershell / terminal):
   cd <path-to-backend>
   .\.venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --app-dir "phase2"

4) เปิดเบราว์เซอร์:
   http://localhost:8001/index.html

การทดสอบ:
 - กรอก start date / end date / industry / เลือก KPI (สูงสุด 5)
 - กรอก daily values (คั่นด้วย comma หรือ new line)
 - กด "ประเมิน (Analyze)" เพื่อเรียก POST /analyze
 - เมื่อได้ผล สามารถดาวน์โหลด CSV ของผลได้จากปุ่มดาวน์โหลด

Privacy / Data:
 - ระบบนี้เก็บข้อมูลที่ผู้ใช้กรอก (start_date, end_date, industry, kpis) ไว้สำหรับ export และวิเคราะห์
 - หากต้องเผยแพร่หรือเก็บข้อมูลระยะยาว ให้เพิ่มหน้า Terms & Privacy และขอความยินยอมของผู้ใช้

Support:
 - หากต้องการไฟล์ backend ที่ผมแก้ไข หรือ zip แบบรวม backend+frontend แจ้งชื่อไฟล์และผมจะรวมให้
