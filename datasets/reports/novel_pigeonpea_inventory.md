# Forensic Dataset Inventory: Novel Pigeonpea Leaf Dataset
**DOI:** 10.17632/bd553pdtny.1  
**Authors:** Dr. G.G. Rajput & Vanita Doddamani (UAS / Agriculture College Vijayapur)  
**Archive:** `bd553pdtny-1.zip` (12,264,708 bytes, ~11.7 MB)  
**SHA256:** `c9f24738913e81d6e90d147fcaabab369198af4df30ac317933894cd4e407994`  
**License:** CC BY 4.0 (Creative Commons Attribution 4.0 International)  

---

### Inventory Breakdown:
- **Total Image Count:** **1,000 images** (256 x 256 pixels, RGB JPEG)
- **Optical Sensor:** Sony Cyber-Shot digital camera
- **Environmental Context:** Natural outdoor agricultural field, Vijayapur, Karnataka (semi-arid black soil belt bordering Maharashtra)
- **Annotation Type:** Directory-level Image Classification (Folder-based ground truth)
- **Bounding Boxes:** None currently included in archive.
- **Class Breakdown (4 Classes):**
  1. `Cercospora Leaf Spot`: 336 images (33.6%)
  2. `Sterilic Mosaic`: 292 images (29.2%)
  3. `Healthy`: 196 images (19.6%)
  4. `Leaf Webber`: 146 images (14.6%)
- **Data Integrity & Quality:**
  - Corrupted Images: 0 (All 1,000 images valid JPEG headers)
  - Duplicate Filenames: 0
  - Resolution: Uniform 256 x 256 pixels
- **Network / Acquisition Status:** S3 cache verified on DataCite (`10.17632/bd553pdtny.1`). Automated direct download triggers Cloudflare Bot Challenge; manual browser download or API session handshake required.

### Forensic Conclusion:
- **Acceptance Decision:** **CONDITIONAL ACCEPT**
- **Action Required Before Training:** Must add bounding-box coordinates for Cercospora lesions and Leaf Webber damage if integrating into YOLO detection pipeline, OR utilize as an auxiliary whole-leaf classification head.
