let mediaStream = null;
let currentSelectedFile = null;
let predictionHistoryCache = [];

let farmerData = {
    name: "",
    phone: ""
};

const LANG_MAP = {
    'en': 'English', 'te': 'తెలుగు', 'kn': 'ಕನ್ನಡ',
    'ta': 'தமிழ்', 'ml': 'മലയാളം', 'hi': 'हिन्दी'
};

window.addEventListener('DOMContentLoaded', () => {
    let progress = 0;
    const preloaderFill = document.getElementById('preloader-fill');
    const preloaderText = document.getElementById('preloader-text');
    const preloader = document.getElementById('site-preloader');

    const interval = setInterval(() => {
        progress += Math.floor(Math.random() * 12) + 4;
        if (progress >= 100) {
            progress = 100;
            clearInterval(interval);
            if (preloaderFill) preloaderFill.style.width = '100%';
            if (preloaderText) preloaderText.innerText = 'FALCON-AI READY! 100%';

            setTimeout(() => {
                if (preloader) {
                    preloader.style.opacity = '0';
                    preloader.style.visibility = 'hidden';
                }
                showLoginModal();
            }, 300);
        } else {
            if (preloaderFill) preloaderFill.style.width = progress + '%';
            if (preloaderText) preloaderText.innerText = `INITIALIZING FALCON-AI... ${progress}%`;
        }
    }, 400);

    const nameInput = document.getElementById('farmer-name');
    const phoneInput = document.getElementById('farmer-phone');

    if (nameInput) {
        nameInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                phoneInput?.focus();
            }
        });
    }

    if (phoneInput) {
        phoneInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                submitFarmerRegistration(e);
            }
        });
    }

    const dropZone = document.getElementById('image-drop-zone');
    if (dropZone) {
        ['dragenter', 'dragover'].forEach(eventName => dropZone.addEventListener(eventName, event => {
            event.preventDefault();
            dropZone.classList.add('is-dragging');
        }));
        ['dragleave', 'drop'].forEach(eventName => dropZone.addEventListener(eventName, event => {
            event.preventDefault();
            dropZone.classList.remove('is-dragging');
        }));
        dropZone.addEventListener('drop', event => {
            const file = event.dataTransfer.files[0];
            if (file) handleSelectedImage(file);
        });
        dropZone.addEventListener('keydown', event => {
            if (event.key === 'Enter' || event.key === ' ') triggerGallery();
        });
    }
});

function applySensorPreset(preset) {
    const values = {
        normal: ['48', '30', '58'],
        dry: ['18', '34', '38'],
        clear: ['', '', '']
    }[preset];
    if (!values) return;
    ['soil-moisture', 'temperature', 'humidity'].forEach((id, index) => {
        const input = document.getElementById(id);
        if (input) input.value = values[index];
    });
    showToast(preset === 'clear' ? 'Sensor inputs cleared' : `${preset === 'dry' ? 'Dry soil' : 'Normal field'} preset loaded`);
}

// THE FIX IS HERE: STRICT SESSION VALIDATION
function checkLoginSession() {
    const savedName = localStorage.getItem('falcon_farmer_name');
    const savedPhone = localStorage.getItem('falcon_farmer_phone');
    const loginModal = document.getElementById('login-modal');

    // Make sure they have a name AND a valid 10-digit number saved
    const phoneRegex = /^[0-9]{10}$/;

    if (savedName && savedPhone && phoneRegex.test(savedPhone)) {
        if (loginModal) {
            loginModal.classList.remove('show-modal');
            loginModal.style.display = 'none';
        }
    } else {
        // If data is corrupt or missing, clear it and force the modal
        localStorage.removeItem('falcon_farmer_name');
        localStorage.removeItem('falcon_farmer_phone');

        if (loginModal) {
            loginModal.classList.add('show-modal');
            loginModal.style.display = 'flex';
        }
    }
}

function submitFarmerRegistration(event) {
    if (event) event.preventDefault();

    const nameInput = document.getElementById('farmer-name');
    const phoneInput = document.getElementById('farmer-phone');

    if (!nameInput || !phoneInput) return false;

    const name = nameInput.value.trim();
    const phone = phoneInput.value.trim();
    const phoneRegex = /^[0-9]{10}$/;

    if (!name) {
        showToast("⚠️ Please enter your Name.");
        nameInput.focus();
        return false;
    }

    if (!phoneRegex.test(phone)) {
        showToast("⚠️ Please enter a valid 10-digit Mobile Number.");
        phoneInput.focus();
        return false;
    }

    farmerData.name = name;
    farmerData.phone = phone;

    localStorage.setItem('falcon_farmer_name', name);
    localStorage.setItem('falcon_farmer_phone', phone);
    renderPredictionHistory();

    const loginModal = document.getElementById('login-modal');
    if (loginModal) {
        loginModal.classList.remove('show-modal');
        setTimeout(() => {
            loginModal.style.display = 'none';
        }, 300);
    }

    setTimeout(() => {
        showToast(`Welcome ${name}! FALCON-AI Portal Ready 🌿`);
    }, 400);

    return false;
}

function openLangModal() {
    const langModal = document.getElementById('lang-picker-modal');
    if (langModal) langModal.classList.add('show-modal');
}

function closeLangModal() {
    const langModal = document.getElementById('lang-picker-modal');
    if (langModal) langModal.classList.remove('show-modal');
}

function switchLanguageViaApi(langCode) {
    const translateCombo = document.querySelector('.goog-te-combo');
    if (translateCombo) {
        translateCombo.value = langCode;
        translateCombo.dispatchEvent(new Event('change'));
    }

    const langTextElement = document.getElementById('lang-text');
    if (langTextElement && LANG_MAP[langCode]) {
        langTextElement.innerText = LANG_MAP[langCode];
    }

    closeLangModal();
    showToast(`Language switched to ${LANG_MAP[langCode] || langCode}`);
}

function toggleTheme() {
    const body = document.body;
    const themeIcon = document.getElementById('theme-icon');

    if (body.classList.contains('dark-theme')) {
        body.classList.remove('dark-theme');
        body.classList.add('light-theme');
        if (themeIcon) themeIcon.className = "fa-solid fa-moon";
    } else {
        body.classList.remove('light-theme');
        body.classList.add('dark-theme');
        if (themeIcon) themeIcon.className = "fa-solid fa-sun";
    }
}

function openDpModal(imageSrc, name) {
    const modal = document.getElementById('dp-modal');
    const modalImg = document.getElementById('dp-modal-img');
    const modalName = document.getElementById('dp-modal-name');

    if (modalImg) modalImg.src = imageSrc;
    if (modalName) modalName.innerText = name;
    if (modal) modal.classList.add('show');
}

function closeDpModal() {
    const modal = document.getElementById('dp-modal');
    if (modal) modal.classList.remove('show');
}

function showToast(message) {
    const toast = document.getElementById('toast-notification');
    if (!toast) return;

    toast.innerText = message;
    toast.classList.add('show');
    setTimeout(() => toast.classList.remove('show'), 3000);
}

function copyToClipboard(text, message) {
    navigator.clipboard.writeText(text).then(() => {
        showToast(message || 'Copied to clipboard!');
    }).catch(err => console.error('Copy failed:', err));
}

function triggerSmartCamera() {
    const isMobile = /Android|iPhone|iPad|iPod/i.test(navigator.userAgent);
    if (isMobile) {
        const camInput = document.getElementById('file-input-camera');
        if (camInput) camInput.click();
    } else {
        openCameraModal();
    }
}

function triggerGallery() {
    const galleryInput = document.getElementById('file-input-gallery');
    if (galleryInput) galleryInput.click();
}

async function openCameraModal() {
    const modal = document.getElementById('camera-modal');
    const video = document.getElementById('webcam-stream');

    try {
        mediaStream = await navigator.mediaDevices.getUserMedia({
            video: { width: { ideal: 1280 }, height: { ideal: 720 }, facingMode: "environment" },
            audio: false
        });
        if (video) video.srcObject = mediaStream;
        if (modal) modal.style.display = 'flex';
    } catch (err) {
        alert("Camera Access Denied or Webcam Not Detected.");
    }
}

function closeCameraModal() {
    if (mediaStream) {
        mediaStream.getTracks().forEach(track => track.stop());
    }
    const modal = document.getElementById('camera-modal');
    if (modal) modal.style.display = 'none';
}

function captureWebcamFrame() {
    const video = document.getElementById('webcam-stream');
    const canvas = document.getElementById('photo-canvas');
    const previewImg = document.getElementById('image-preview');
    const previewContainer = document.getElementById('preview-container');

    if (!video || !canvas) return;

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob((blob) => {
        currentSelectedFile = new File([blob], "camera_capture.jpg", { type: "image/jpeg" });
        if (previewImg) previewImg.src = URL.createObjectURL(blob);
        if (previewContainer) previewContainer.style.display = 'block';

        closeCameraModal();
        startScanAndPredict(currentSelectedFile);
    }, 'image/jpeg');
}

function handleImageUpload(event) {
    const file = event.target.files[0];
    if (file) handleSelectedImage(file);
}

function handleSelectedImage(file) {
    if (!file.type.startsWith('image/')) {
        showToast('Please choose an image file');
        return;
    }
    if (file.size > 15 * 1024 * 1024) {
        showToast('Image must be smaller than 15 MB');
        return;
    }

    currentSelectedFile = file;
    const reader = new FileReader();
    reader.onload = function(e) {
        const previewImg = document.getElementById('image-preview');
        const previewContainer = document.getElementById('preview-container');
        if (previewImg) previewImg.src = e.target.result;
        if (previewContainer) previewContainer.style.display = 'block';

        startScanAndPredict(currentSelectedFile);
    };
    reader.readAsDataURL(file);
}

function startScanAndPredict(file) {
    const progressContainer = document.getElementById('analysis-progress');
    const resultCard = document.getElementById('result-card');
    const scanFill = document.getElementById('scan-bar-fill');
    const statusText = document.getElementById('scan-status-text');
    const percentageText = document.getElementById('scan-percentage');

    if (resultCard) resultCard.style.display = 'none';
    if (progressContainer) progressContainer.style.display = 'block';
    if (scanFill) scanFill.style.width = '0%';
    if (percentageText) percentageText.innerText = '0%';

    const formData = new FormData();
    formData.append("file", file);
    formData.append("farmer_name", farmerData.name);
    formData.append("farmer_phone", farmerData.phone);
    const sensorFields = ["soil-moisture", "temperature", "humidity"];
    const sensorKeys = ["soil_moisture", "temperature", "humidity"];
    sensorFields.forEach((fieldId, index) => {
        const value = document.getElementById(fieldId)?.value.trim();
        if (value) formData.append(sensorKeys[index], value);
    });

    let currentStage = 0;
    const stages = [
        { pct: 30, status: "EXTRACTING COLOR MASKS..." },
        { pct: 60, status: "CHECKING EDGE DENSITY..." },
        { pct: 85, status: "RUNNING DUAL-MODEL INFERENCE..." }
    ];

    const scanInterval = setInterval(() => {
        if (currentStage < stages.length) {
            if (scanFill) scanFill.style.width = stages[currentStage].pct + '%';
            if (percentageText) percentageText.innerText = stages[currentStage].pct + '%';
            if (statusText) statusText.innerText = stages[currentStage].status;
            currentStage++;
        } else {
            clearInterval(scanInterval);

            fetch("/predict", { method: "POST", body: formData })
            .then(res => {
                if (!res.ok) throw new Error(`Prediction request failed (${res.status})`);
                return res.json();
            })
            .then(data => {
                if (scanFill) scanFill.style.width = '100%';
                if (percentageText) percentageText.innerText = '100%';
                if (statusText) statusText.innerText = "DIAGNOSIS COMPLETE!";

                setTimeout(() => {
                    if (progressContainer) progressContainer.style.display = 'none';
                    displayResults(data);
                }, 800);
            })
            .catch(err => {
                if (statusText) statusText.innerText = "❌ FAILED";
                if (progressContainer) progressContainer.style.display = 'none';
                displayResults({
                    status: "Unavailable",
                    disease_name: "Analysis unavailable",
                    confidence: 0,
                    message: "The server could not complete the analysis. Please try again.",
                    is_valid_crop: false,
                    recommendation: {
                        action: "Retake the image and try again",
                        dosage: "No treatment recommendation available",
                        sensor_status: "Connection failed",
                        reason: err.message
                    }
                });
            });
        }
    }, 400);
}

function displayResults(data) {
    const resultCard = document.getElementById('result-card');
    const title = document.getElementById('result-title');
    const disease = document.getElementById('result-disease');
    const confidence = document.getElementById('result-confidence');
    const message = document.getElementById('result-message');
    const leafArea = document.getElementById('result-leaf-area');
    const damage = document.getElementById('result-damage');
    const markers = document.getElementById('result-markers');
    const overlay = document.getElementById('result-overlay');
    const recommendation = data.recommendation || {};

    if (!resultCard) return;

    let themeClass = "";
    let emoji = "";
    let engagingMessage = "";

    if (data.is_valid_crop === false) {
        themeClass = "theme-invalid";
        emoji = "⚠️";
        engagingMessage = `Hold on! ${data.message}`;
    } else if (data.status === "Healthy") {
        themeClass = "theme-healthy";
        emoji = "🌿✨";
        engagingMessage = `Great news! ${data.message}`;
    } else if (data.status === "Uncertain") {
        themeClass = "theme-invalid";
        emoji = "⚠️";
        engagingMessage = `Review required. ${data.message}`;
    } else {
        themeClass = "theme-disease";
        emoji = "🚨";
        engagingMessage = `Attention! ${data.message}`;
    }

    resultCard.classList.remove("theme-disease", "theme-healthy", "theme-invalid");
    resultCard.classList.add(themeClass);

    if (title) title.innerText = `${emoji} Status: ${data.status}`;
    if (disease) disease.innerText = data.disease_name;
    if (confidence) confidence.innerText = `Confidence: ${data.confidence}%`;
    if (message) message.innerText = engagingMessage;
    if (leafArea) leafArea.innerText = `${data.leaf_area_percent ?? 0}%`;
    if (damage) damage.innerText = `${data.damage_percent ?? 0}%`;
    if (markers) markers.innerText = data.markers?.length ?? 0;
    if (overlay) {
        overlay.src = data.overlay || '';
        overlay.style.display = data.overlay ? 'block' : 'none';
    }
    const action = document.getElementById('result-action');
    const dosage = document.getElementById('result-dosage');
    const sensorStatus = document.getElementById('result-sensor-status');
    const reason = document.getElementById('result-reason');
    if (action) action.innerText = recommendation.action || 'No recommendation available';
    if (dosage) dosage.innerText = recommendation.dosage || '';
    if (sensorStatus) sensorStatus.innerText = recommendation.sensor_status || '';
    if (reason) reason.innerText = recommendation.reason || '';

    resultCard.style.display = 'block';
    renderPredictionHistory();
}

async function renderPredictionHistory() {
    const container = document.getElementById('prediction-history');
    if (!container) return;
    if (!farmerData.phone) {
        predictionHistoryCache = [];
        container.innerHTML = '<p class="empty-history">Your completed analyses will appear here.</p>';
        return;
    }
    try {
        const response = await fetch(`/history?phone=${encodeURIComponent(farmerData.phone)}`);
        if (!response.ok) throw new Error('History request failed');
        const payload = await response.json();
        predictionHistoryCache = payload.items || [];
    } catch (error) {
        predictionHistoryCache = [];
        container.innerHTML = '<p class="empty-history">History is temporarily unavailable.</p>';
        return;
    }
    if (!predictionHistoryCache.length) {
        container.innerHTML = '<p class="empty-history">No diagnoses recorded for this farmer.</p>';
        return;
    }
    container.innerHTML = predictionHistoryCache.map(item => `
        <article class="history-row">
            <div><strong>${escapeHtml(item.disease_name)}</strong><small>${escapeHtml(item.created_at)}</small></div>
            <span>${escapeHtml(item.status)} · ${item.confidence}% confidence</span>
            <span>${item.damage_percent}% visible damage</span>
        </article>`).join('');
}

function exportPredictionHistory() {
    if (!predictionHistoryCache.length) {
        showToast('Complete an analysis before exporting');
        return;
    }
    const headers = ['Time', 'Disease', 'Status', 'Confidence', 'Visible damage', 'Recommended action'];
    const rows = predictionHistoryCache.map(item => [item.created_at, item.disease_name, item.status, item.confidence, item.damage_percent, item.action]);
    const csv = [headers, ...rows].map(row => row.map(value => `"${String(value).replaceAll('"', '""')}"`).join(',')).join('\n');
    const link = document.createElement('a');
    link.href = URL.createObjectURL(new Blob([csv], { type: 'text/csv' }));
    link.download = 'falcon-ai-diagnosis-report.csv';
    link.click();
    URL.revokeObjectURL(link.href);
}

function escapeHtml(value) {
    return String(value).replace(/[&<>'"]/g, character => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[character]));
}

function showLoginModal() {
    const loginModal = document.getElementById('login-modal');
    if (!loginModal) return;
    loginModal.classList.add('show-modal');
    loginModal.style.display = 'flex';
    document.getElementById('farmer-name')?.focus();
}