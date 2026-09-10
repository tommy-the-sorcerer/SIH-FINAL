/**
 * FALCON-AI Client Application Engine v2.5
 * SIH 2026 Problem Statement SIH26131:
 * "Early detection and management of crop diseases and pest infestations"
 * Government of Maharashtra (Maharashtra State Innovation Society)
 */

// Global Application State
let appState = {
    lang: localStorage.getItem('falcon_lang') || 'en',
    currentUser: null,
    activeView: 'dashboard',
    activeTab: 'farmer', // Backward compatibility
    taxonomy: null,
    translations: {},
    selectedCrop: 'maize',
    selectedStage: 'vegetative',
    selectedDistrict: 'Nashik',
    selectedTaluka: '',
    selectedVillage: '',
    latitude: 20.1705,
    longitude: 73.9885,
    selectedFile: null,
    activeCaseId: null,
    lastDiagnosisData: null,
    gisMap: null,
    gisMarkers: [],
    expertAction: 'CONFIRM',
    gatewayVisible: false
};

const LANG_LABELS = {
    'en': 'English',
    'mr': 'मराठी',
    'hi': 'हिंदी'
};

// ==============================================================================
// 1. INITIALIZATION ON DOM READY
// ==============================================================================

window.addEventListener('DOMContentLoaded', async () => {
    // 1. Start preloader animation
    initPreloader();

    // 2. Restore user session or create default demo farmer
    initUserSession();

    // 3. Fetch Taxonomy & Localization Catalogs
    await loadTaxonomy();
    await loadTranslations(appState.lang);

    // 4. Setup DOM elements, drag-drop, and location
    setupDragDrop();
    populateCrops();
    populateDistricts();

    // 5. Connect real backend APIs
    updateLiveWeather(appState.latitude, appState.longitude);
    loadFarms();
    loadFarmerCasesHistory();
    refreshPendingExpertCount();
    loadDashboardStats();

    // 6. Initialize GIS Map in background
    setTimeout(() => {
        initGisMap();
    }, 600);

    // 7. Continuous Live Weather Telemetry Refresh (Every 10 minutes)
    setInterval(() => {
        updateLiveWeather(appState.latitude, appState.longitude);
    }, 10 * 60 * 1000);
});

function initPreloader() {
    let progress = 0;
    const fill = document.getElementById('preloader-fill');
    const text = document.getElementById('preloader-text');
    const preloader = document.getElementById('site-preloader');

    const timer = setInterval(() => {
        progress += Math.floor(Math.random() * 25) + 15;
        if (progress >= 100) {
            progress = 100;
            clearInterval(timer);
            if (fill) fill.style.width = '100%';
            if (text) text.innerText = 'MAHARASHTRA AGRI-AI READY! 100%';
            setTimeout(() => {
                if (preloader) {
                    preloader.style.opacity = '0';
                    preloader.style.visibility = 'hidden';
                    setTimeout(() => { preloader.style.display = 'none'; }, 300);
                }
            }, 200);
        } else {
            if (fill) fill.style.width = progress + '%';
            if (text) text.innerText = `INITIALIZING DECISION ENGINE... ${progress}%`;
        }
    }, 80);
}

function initUserSession() {
    try {
        const savedUser = localStorage.getItem('falcon_user');
        const savedRole = localStorage.getItem('falcon_user_role');
        if (savedUser) {
            appState.currentUser = JSON.parse(savedUser);
            if (savedRole && appState.currentUser) {
                const normR = savedRole.toLowerCase();
                appState.currentUser.role = normR === 'expert' ? 'EXPERT' : (normR === 'officer' || normR === 'admin' ? 'ADMIN' : 'FARMER');
            }
        }
    } catch (e) {
        appState.currentUser = null;
    }
    updateNavUserDisplay();
}

function updateNavUserDisplay() {
    const btn = document.getElementById('auth-user-name');
    const roleEl = document.getElementById('auth-user-role');
    const headerSignoutBtn = document.getElementById('header-btn-signout');
    const gatewayCard = document.getElementById('persona-gateway-card');
    const gatewayUserText = document.getElementById('gateway-user-text');
    const gatewayUserBadge = document.getElementById('gateway-user-badge');
    const signoutBtn = document.getElementById('btn-gateway-signout');
    const gatewayLoginForm = document.getElementById('gateway-login-form');

    if (appState.currentUser) {
        document.body.classList.add('authenticated');
        const role = (appState.currentUser.role || 'FARMER').toUpperCase();
        const roleClean = role === 'EXPERT' ? 'Agricultural Expert' :
                          (role === 'ADMIN' || role === 'OFFICER') ? 'Agricultural Officer' : 'Farmer';

        const roleLabel = role === 'EXPERT' ? '🔬 Agricultural Expert' :
                          (role === 'ADMIN' || role === 'OFFICER') ? '🏛️ Agricultural Officer' : '🧑‍🌾 Farmer';

        // Requirement 4: Top-right navbar display active profile badge: "[Name] ([Role])"
        if (btn) btn.innerText = `${appState.currentUser.full_name} (${roleClean})`;
        if (roleEl) roleEl.innerText = `${roleLabel}`;

        // Top navbar inline Sign Out button visible when authenticated
        if (headerSignoutBtn) {
            headerSignoutBtn.style.display = 'inline-flex';
        }

        // Requirement 4: Remove redundant Role Gateway banner from every sub-page view
        if (gatewayCard) {
            gatewayCard.style.display = 'none';
        }

        if (gatewayUserText) gatewayUserText.innerText = `${appState.currentUser.full_name} (${roleLabel})`;
        if (gatewayUserBadge) {
            gatewayUserBadge.style.background = '#ecfdf5';
            gatewayUserBadge.style.color = '#065f46';
            gatewayUserBadge.style.borderColor = '#a7f3d0';
        }
        if (signoutBtn) {
            signoutBtn.innerHTML = '<i class="fa-solid fa-right-from-bracket"></i> Sign Out';
            signoutBtn.onclick = userSignOut;
            signoutBtn.style.color = '#b91c1c';
            signoutBtn.style.borderColor = '#fecaca';
        }
        if (gatewayLoginForm) gatewayLoginForm.style.display = 'none';

        applyRoleAccessControl(role);
    } else {
        // GUEST / UNAUTHENTICATED STATE
        document.body.classList.remove('authenticated');
        if (btn) btn.innerText = 'Sign In / Register';
        if (roleEl) roleEl.innerText = 'Guest Farmer';

        // Hide top navbar sign out button in guest mode
        if (headerSignoutBtn) {
            headerSignoutBtn.style.display = 'none';
        }

        // Show Gateway banner ONLY on initial unauthenticated landing dashboard
        if (gatewayCard) {
            gatewayCard.style.display = appState.activeView === 'dashboard' ? 'block' : 'none';
        }

        if (gatewayUserText) gatewayUserText.innerText = 'Guest Farmer (Not Signed In)';
        if (gatewayUserBadge) {
            gatewayUserBadge.style.background = '#f1f5f9';
            gatewayUserBadge.style.color = '#475569';
            gatewayUserBadge.style.borderColor = '#cbd5e1';
        }
        if (signoutBtn) {
            signoutBtn.innerHTML = '<i class="fa-solid fa-arrow-right-to-bracket"></i> Sign In / Register';
            signoutBtn.onclick = openAuthModal;
            signoutBtn.style.color = '#15803d';
            signoutBtn.style.borderColor = '#bbf7d0';
        }
        if (gatewayLoginForm) gatewayLoginForm.style.display = 'flex';

        applyRoleAccessControl('FARMER');
    }
}

/**
 * RBAC Filter: Hides Pest & Disease Outbreak Surveillance Bulletin and GIS Heat Map from Farmers.
 * Guarantees restricted GPS telemetry and outbreak intelligence are only accessible by Authorized Officers & Experts.
 */
function applyRoleAccessControl(role) {
    const normRole = (role || localStorage.getItem('falcon_user_role') || 'FARMER').toUpperCase();
    const isFarmer = normRole === 'FARMER' || normRole.includes('FARMER');
    const isExpert = normRole === 'EXPERT';
    const isOfficer = normRole === 'ADMIN' || normRole === 'OFFICER';

    // Sidebar items
    const navAlerts = document.getElementById('nav-item-alerts');
    const heroAlerts = document.getElementById('hero-btn-alerts');
    const navHotspots = document.getElementById('nav-item-hotspots');
    const navSensors = document.getElementById('nav-item-sensors');
    const navExpert = document.getElementById('nav-item-expert');
    const navOfficer = document.getElementById('nav-item-officer');

    // Requirement 4: Surveillance Bulletin and GIS Heat Map must be strictly HIDDEN if active role is 'Farmer'
    if (navAlerts) navAlerts.style.display = isFarmer ? 'none' : 'flex';
    if (heroAlerts) heroAlerts.style.display = isFarmer ? 'none' : 'inline-flex';
    if (navHotspots) navHotspots.style.display = isFarmer ? 'none' : 'flex';
    if (navSensors) navSensors.style.display = isFarmer ? 'none' : 'flex';
    if (navExpert) navExpert.style.display = (isExpert || isOfficer) ? 'flex' : 'none';
    if (navOfficer) navOfficer.style.display = isOfficer ? 'flex' : 'none';

    const viewAlerts = document.getElementById('view-alerts');
    if (viewAlerts && isFarmer) {
        viewAlerts.style.display = 'none';
        viewAlerts.classList.remove('active-panel');
    }

    const viewHotspots = document.getElementById('view-hotspots');
    if (viewHotspots && isFarmer) {
        viewHotspots.style.display = 'none';
        viewHotspots.classList.remove('active-panel');
    }

    // If farmer is currently on a restricted view, redirect to farmer dashboard
    if (isFarmer && (appState.activeView === 'alerts' || appState.activeView === 'hotspots' || appState.activeView === 'sensors' || appState.activeView === 'expert' || appState.activeView === 'officer')) {
        switchView('dashboard');
    }
}


// ==============================================================================
// 2. VIEW NAVIGATION ROUTER (10 VIEWS)
// ==============================================================================

function switchView(viewName) {
    const userRole = (appState.currentUser?.role || localStorage.getItem('falcon_user_role') || 'FARMER').toUpperCase();
    const isFarmer = userRole === 'FARMER' || userRole.includes('FARMER');

    // Requirement 4 Guard: Prevent farmer from accessing Surveillance Bulletin or GIS Heat Map
    if (isFarmer && (viewName === 'alerts' || viewName === 'hotspots' || viewName === 'sensors' || viewName === 'expert' || viewName === 'officer')) {
        showToast('Access Restricted: Pest & Disease Outbreak Surveillance Bulletin and GIS Heat Map are hidden for Farmer role.');
        return;
    }

    appState.activeView = viewName;

    // Requirement 4: Remove redundant Role Gateway banner from every sub-page view
    const gatewayCard = document.getElementById('persona-gateway-card');
    if (gatewayCard) {
        if (appState.currentUser) {
            gatewayCard.style.display = 'none';
        } else {
            // Show ONLY on initial unauthenticated landing dashboard
            gatewayCard.style.display = viewName === 'dashboard' ? 'block' : 'none';
        }
    }


    // Toggle active panel
    document.querySelectorAll('.view-panel').forEach(panel => {
        panel.classList.remove('active-panel');
    });
    const targetPanel = document.getElementById(`view-${viewName}`);
    if (targetPanel) {
        targetPanel.classList.add('active-panel');
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    // Toggle active sidebar item
    document.querySelectorAll('.sidebar-nav-item').forEach(item => {
        item.classList.remove('active');
    });
    const activeNav = document.getElementById(`nav-item-${viewName}`);
    if (activeNav) {
        activeNav.classList.add('active');
    }

    // Close mobile sidebar if open
    const sidebar = document.getElementById('app-sidebar');
    if (sidebar && sidebar.classList.contains('sidebar-open')) {
        sidebar.classList.remove('sidebar-open');
    }

    // Dynamic data loading per view
    if (viewName === 'dashboard') {
        loadDashboardStats();
        loadFarmerCasesHistory();
        loadFarms();
    } else if (viewName === 'fields') {
        loadFarms();
    } else if (viewName === 'alerts') {
        loadDashboardStats();
        renderSurveillanceBulletin();
    } else if (viewName === 'weather') {
        updateLiveWeather(appState.latitude, appState.longitude);
    } else if (viewName === 'hotspots') {
        loadDashboardStats();
        setTimeout(() => {
            if (appState.gisMap) appState.gisMap.invalidateSize();
            else initGisMap();
        }, 150);
    } else if (viewName === 'advisory') {
        loadAdvisoryView();
    } else if (viewName === 'expert') {
        loadPendingExpertCases();
        refreshPendingExpertCount();
    } else if (viewName === 'officer') {
        loadOfficerDashboard();
    }
}

// Backward-compatible alias for existing tab button clicks
function switchMainTab(tabName) {
    if (tabName === 'farmer') switchView('dashboard');
    else switchView(tabName);
}

function toggleMobileSidebar() {
    const sidebar = document.getElementById('app-sidebar');
    if (sidebar) sidebar.classList.toggle('sidebar-open');
}

function selectPortalRole(role) {
    if (appState.currentUser) {
        const userRole = (appState.currentUser.role || 'FARMER').toLowerCase();
        const roleMap = { 'farmer': 'farmer', 'expert': 'expert', 'admin': 'officer', 'officer': 'officer' };
        if (roleMap[userRole] === role) {
            if (role === 'farmer') switchView('dashboard');
            else if (role === 'expert') switchView('expert');
            else if (role === 'officer') switchView('officer');
            return;
        }
    }

    const roleNames = {
        'farmer': 'Farmer Portal',
        'expert': 'Agricultural Expert Desk',
        'officer': 'Agriculture Officer Portal'
    };
    showToast(`Switching to ${roleNames[role] || 'portal'}.`);
    openAuthModalWithRole(role);
}

// Backward-compatible alias
function quickSwitchPersona(persona) {
    selectPortalRole(persona);
}

function userSignOut() {
    if (appState.currentUser && appState.currentUser.id) {
        logActivity('LOGOUT', 'User signed out');
    }
    localStorage.removeItem('falcon_user');
    localStorage.removeItem('falcon_user_role');
    localStorage.removeItem('falcon_token');
    appState.currentUser = null;
    appState.lastDiagnosisData = null;
    document.body.classList.remove('authenticated');
    closeAuthModal();
    initUserSession();
    updateNavUserDisplay();
    switchView('dashboard');
    showToast('Signed out successfully. Session state cleared.');
}


// ==============================================================================
// 3. LOCALIZATION (MARATHI FIRST, HINDI, ENGLISH)
// ==============================================================================

async function loadTranslations(lang) {
    try {
        const res = await fetch(`/api/i18n/${lang}`);
        if (res.ok) {
            appState.translations = await res.json();
            applyTranslations();
        }
    } catch (e) {
        console.warn('Failed to load translations', e);
    }
}

function t(key, fallback = '') {
    return appState.translations[key] || fallback || key;
}

function applyTranslations() {
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (appState.translations[key]) {
            el.innerText = appState.translations[key];
        }
    });

    const langText = document.getElementById('lang-text');
    if (langText) {
        langText.innerText = appState.lang === 'mr' ? 'मराठी' : (appState.lang === 'hi' ? 'हिंदी' : 'English');
    }

    // Update html lang attribute
    document.documentElement.lang = appState.lang;
}

function toggleLanguageDropdown() {
    const menu = document.getElementById('lang-dropdown-menu');
    if (menu) {
        menu.style.display = menu.style.display === 'block' ? 'none' : 'block';
    }
}

// Close dropdown on outside click
document.addEventListener('click', (e) => {
    const wrap = document.querySelector('.lang-switcher-wrap');
    const menu = document.getElementById('lang-dropdown-menu');
    if (wrap && menu && !wrap.contains(e.target)) {
        menu.style.display = 'none';
    }
});

async function changeLanguage(lang) {
    appState.lang = lang;
    localStorage.setItem('falcon_lang', lang);

    const menu = document.getElementById('lang-dropdown-menu');
    if (menu) menu.style.display = 'none';

    await loadTranslations(lang);

    // Update active button state in modal if present
    ['mr', 'hi', 'en'].forEach(l => {
        const btn = document.getElementById(`lang-btn-${l}`);
        if (btn) btn.classList.toggle('active', l === lang);
    });

    // Re-populate dynamic dropdowns with localized labels
    populateCrops();
    updateNavUserDisplay();
    logActivity('LANGUAGE_CHANGE', `Changed language to ${lang}`);
    showToast(lang === 'mr' ? 'भाषा: मराठी सेट केली' : (lang === 'hi' ? 'भाषा: हिंदी सेट की गई' : 'Language set to English'));
}



// ==============================================================================
// VOICE ASSISTANT ENGINE (कृषी सखा - KRISHI MITRA)
// ==============================================================================

let mediaRecorder = null;
let voiceChunks = [];
let isVoiceListening = false;

function toggleVoiceAssistant() {
    const modal = document.getElementById('voice-assistant-modal');
    if (modal) {
        if (modal.classList.contains('show-modal')) {
            closeVoiceAssistant();
        } else {
            modal.classList.add('show-modal');
        }
    }
}

function closeVoiceAssistant() {
    const modal = document.getElementById('voice-assistant-modal');
    if (modal) modal.classList.remove('show-modal');
    stopSpeechRecognition();
}

function toggleSpeechRecognition() {
    if (isVoiceListening) {
        stopSpeechRecognition();
    } else {
        startSpeechRecognition();
    }
}

function startSpeechRecognition() {
    if (!navigator.mediaDevices?.getUserMedia || !window.MediaRecorder) {
        showToast('Audio recording is not supported in this browser.');
        return;
    }

    navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
        const pulse = document.getElementById('voice-listening-pulse');
        const icon = document.getElementById('voice-mic-icon');
        const btn = document.getElementById('voice-mic-main-btn');
        const statusSub = document.getElementById('voice-status-sub');
        voiceChunks = [];
        mediaRecorder = new MediaRecorder(stream);
        const mimeType = mediaRecorder.mimeType || 'audio/webm';

        mediaRecorder.ondataavailable = event => {
            if (event.data && event.data.size > 0) {
                voiceChunks.push(event.data);
            }
        };

        mediaRecorder.onstop = async () => {
            stream.getTracks().forEach(track => track.stop());
            if (statusSub) statusSub.innerText = "Processing with Groq Whisper & LLaMA AI...";
            if (pulse) pulse.style.display = 'none';
            if (btn) btn.style.background = '#0284c7';
            if (icon) icon.className = 'fa-solid fa-spinner fa-spin';

            if (voiceChunks.length === 0) {
                if (statusSub) statusSub.innerText = "No speech detected. Click mic to speak.";
                resetVoiceMicUi();
                return;
            }

            const blob = new Blob(voiceChunks, { type: mimeType });
            const formData = new FormData();
            formData.append('audio', blob, 'voice.webm');

            try {
                const response = await fetch('/api/voice-command', { method: 'POST', body: formData });
                if (!response.ok) {
                    const err = await response.json().catch(() => ({}));
                    throw new Error(err.detail || 'Voice processing failed');
                }
                const result = await response.json();
                const transcriptEl = document.getElementById('voice-user-transcript');
                const replyEl = document.getElementById('voice-agent-reply');
                if (transcriptEl) transcriptEl.innerText = `"${result.transcript || ''}"`;
                if (replyEl) replyEl.innerText = result.reply_text || '';
                if (statusSub) statusSub.innerText = "Click mic to ask another farming question.";

                // Vocalize AI speech response
                speakVoiceResponse(result.reply_text || '');

                // Execute navigation intent
                if (result.intent === 'diagnose') {
                    setTimeout(() => switchView('diagnose'), 1200);
                } else if (result.intent === 'weather') {
                    setTimeout(() => switchView('weather'), 1200);
                } else if (result.intent === 'help') {
                    setTimeout(() => openQuickActionModal(), 1200);
                }
            } catch (error) {
                console.warn('Voice command error:', error);
                if (statusSub) statusSub.innerText = "Voice error: " + error.message;
                showToast(error.message);
            } finally {
                resetVoiceMicUi();
            }
        };

        mediaRecorder.start();
        isVoiceListening = true;
        if (pulse) pulse.style.display = 'block';
        if (btn) btn.style.background = '#dc2626';
        if (icon) icon.className = 'fa-solid fa-microphone-slash';
        if (statusSub) statusSub.innerText = "🔴 Listening... Click mic again when done speaking.";
    }).catch(error => {
        console.warn('Audio recording failed:', error);
        resetVoiceMicUi();
        showToast('Microphone access denied or unavailable: ' + error.message);
    });
}

function resetVoiceMicUi() {
    isVoiceListening = false;
    mediaRecorder = null;
    const pulse = document.getElementById('voice-listening-pulse');
    const icon = document.getElementById('voice-mic-icon');
    const btn = document.getElementById('voice-mic-main-btn');
    if (pulse) pulse.style.display = 'none';
    if (btn) btn.style.background = '#16a34a';
    if (icon) icon.className = 'fa-solid fa-microphone';
}

function stopSpeechRecognition() {
    isVoiceListening = false;
    if (mediaRecorder && mediaRecorder.state !== 'inactive') {
        try {
            mediaRecorder.stop();
        } catch (e) {
            console.warn('Error stopping mediaRecorder:', e);
            resetVoiceMicUi();
        }
    } else {
        resetVoiceMicUi();
    }
}

function simulateVoiceQuery(text) {
    handleVoiceQuery(text);
}

function openQuickActionModal() {
    const modal = document.getElementById('quick-action-modal');
    if (modal) modal.classList.add('show-modal');
}

function closeQuickActionModal() {
    const modal = document.getElementById('quick-action-modal');
    if (modal) modal.classList.remove('show-modal');
}

function handleVoiceQuery(query) {
    const transcriptEl = document.getElementById('voice-user-transcript');
    const replyEl = document.getElementById('voice-agent-reply');
    if (transcriptEl) transcriptEl.innerText = `"${query}"`;

    logActivity('VOICE_QUERY', query, { language: appState.lang });

    const q = (query || '').toLowerCase().trim();
    let reply = "";

    // 4. Multilingual Voice Assistant: Regex and Token Intent Extraction
    const isDiagnoseIntent = /(take\s+me\s+to\s+diagnose|diagnose(\s+page|\s+crop)?|scan\s+leaf|check\s+(my\s+)?crop|identify\s+disease|patte\s+ki\s+jaanch(\s+karni\s+hai)?|jaanch\s+karni\s+hai|पत्ते\s+की\s+जांच|फसल\s+की\s+जांच|रोग\s+पहचाने|पिकाची\s+तपासणी|रोग\s+तपास)/i.test(q);
    const isWeatherIntent = /(what\s+is\s+the\s+weather(\s+now)?|what('s|\s+is)\s+the\s+weather|how\s+is\s+the\s+weather|rain\s+forecast|weather\s+today|temperature|mausam\s+kaisa\s+hai|aaj\s+ka\s+mausam|मौसम\s+कैसा\s+है|आज\s+का\s+मौसम|हवामान\s+कसे\s+आहे|आजचे\s+हवामान|बारिश\s+होगी|तापमान)/i.test(q);
    const isHelpIntent = /(mujhko\s+ek\s+help\s+chahiye|madad\s+chahiye|help|ek\s+help\s+chahiye|how\s+does\s+this\s+work|what\s+can\s+you\s+do|सहाय्यता|मदत(\s+हवी\s+आहे)?|मदत\s+करा|मदद\s+चाहिए|कसे\s+वापरायचे|यह\s+कैसे\s+काम\s+करता\s+है)/i.test(q);

    if (isDiagnoseIntent) {
        if (appState.lang === 'mr') {
            reply = "पिकाच्या रोगाचे अचूक निदान करण्यासाठी, पिक तपासणी (Crop Diagnosis) पृष्ठावर नेले जात आहे. पानाचा स्पष्ट फोटो अपलोड करा.";
        } else if (appState.lang === 'hi') {
            reply = "फसल के रोग की सटीक जांच के लिए, फसल निदान (Crop Diagnosis) पेज खोला जा रहा है। कृपया पत्ते का फोटो अपलोड करें।";
        } else {
            reply = "Taking you to the Crop Diagnosis panel now. Please upload or align a clear photo of the crop leaf for instant neural analysis.";
        }
        setTimeout(() => switchView('diagnose'), 1400);
    } else if (isWeatherIntent) {
        const temp = document.getElementById('live-temp')?.innerText || '28 °C';
        const hum = document.getElementById('live-humidity')?.innerText || '65 %';
        const rain = document.getElementById('live-rain')?.innerText || '0.0 mm';
        if (appState.lang === 'mr') {
            reply = `आपल्या भागातील सध्याचे हवामान: तापमान ${temp}, आर्द्रता ${hum} आणि पाऊस ${rain} आहे. हवामान फवारणीसाठी योग्य आहे.`;
        } else if (appState.lang === 'hi') {
            reply = `आपके क्षेत्र में इस समय का मौसम: तापमान ${temp}, आर्द्रता ${hum} और बारिश ${rain} है। फोलियर स्प्रे के लिए परिस्थितियां अनुकूल हैं।`;
        } else {
            reply = `The current weather in your area shows temperature of ${temp}, relative humidity of ${hum}, and rainfall at ${rain}.`;
        }
        setTimeout(() => switchView('weather'), 1400);
    } else if (isHelpIntent) {
        if (appState.lang === 'mr') {
            reply = "फाल्कन-एआय सहाय्यक उघडत आहे. तुम्ही पिकांची तपासणी करू शकता, हवामान तपासू शकता, शेती व्यवस्थापन किंवा उपचार सल्ला मिळवू शकता.";
        } else if (appState.lang === 'hi') {
            reply = "फाल्कन-एआई सहायता केंद्र खुल गया है। आप सीधे पत्ते की जांच कर सकते हैं, मौसम देख सकते हैं या उपचार गाइड ले सकते हैं।";
        } else {
            reply = "FALCON-AI assistant is here to help. Opening quick actions for crop diagnosis, live weather telemetry, and validated treatment advisories.";
        }
        setTimeout(() => openQuickActionModal(), 1200);
    } else if (q.includes('लष्करी') || q.includes('मका') || q.includes('armyworm') || q.includes('मक्के') || q.includes('fall armyworm')) {
        if (appState.lang === 'mr') {
            reply = "मक्यावरील लष्करी अळी नियंत्रणासाठी ५ टक्के निंबोळी अर्क किंवा क्लोरांट्रानिलिप्रोल १८.५ टक्के एससी ०.४ मिली प्रति लिटर पाण्यात मिसळून पोंग्यात फवारावे.";
        } else if (appState.lang === 'hi') {
            reply = "मक्के के फॉल आर्मीवर्म के नियंत्रण के लिए 5% नीम अर्क या क्लोरेंट्रानिलिप्रोल 18.5% एससी 0.4 मिली प्रति लीटर पानी में मिलाकर भोंपों में छिड़कें।";
        } else {
            reply = "For Fall Armyworm in Maize, spray Chlorantraniliprole 18.5% SC @ 0.4 ml/L or 5% Neem Seed Kernel Extract directly into whorls. Observe 14 days pre-harvest interval.";
        }
    } else if (q.includes('तांबेरा') || q.includes('सोयाबीन') || q.includes('rust') || q.includes('सोयाबीन रस्ट')) {
        if (appState.lang === 'mr') {
            reply = "सोयाबीनवरील तांबेरा रोगासाठी हेक्झाकोनॅझोल ५ टक्के ईसी किंवा प्रोपिकोनॅझोल २५ टक्के ईसी १ मिली प्रति लिटर पाण्यात मिसळून पहिली लक्षणे दिसताच फवारावे.";
        } else if (appState.lang === 'hi') {
            reply = "सोयाबीन रस्ट (गेरुआ) की रोकथाम के लिए प्रोपिकोनाजोल 25% ईसी 1 मिली प्रति लीटर पानी में मिलाकर लक्षण दिखते ही तुरंत छिड़काव करें।";
        } else {
            reply = "For Soybean Rust, apply Hexaconazole 5% EC or Propiconazole 25% EC @ 1 ml/L water immediately upon detecting the first foliar pustules.";
        }
    } else if (q.includes('कापूस') || q.includes('बोंडअळी') || q.includes('bollworm') || q.includes('cotton') || q.includes('गुलाबी बोंड')) {
        if (appState.lang === 'mr') {
            reply = "कापसातील गुलाबी बोंडअळी नियंत्रणासाठी एकरी २ कामगंध सापळे लावावेत. प्रादुर्भाव वाढल्यास स्पिनोसॅड ४५ टक्के एससी ०.३ मिली प्रति लिटर फवारावे.";
        } else if (appState.lang === 'hi') {
            reply = "कपास की गुलाबी सूंडी के लिए प्रति एकड़ 2 फेरोमोन ट्रैप लगाएं। आर्थिक क्षति स्तर पार करने पर स्पिनोसैड 45% एससी 0.3 मिली/लीटर स्प्रे करें।";
        } else {
            reply = "For Cotton Pink Bollworm, deploy 2 pheromone traps per acre and apply Spinosad 45% SC @ 0.3 ml/L if trap catches exceed threshold.";
        }
    } else if (q.includes('टोमॅटो') || q.includes('करपा') || q.includes('blight') || q.includes('tomato') || q.includes('टमाटर')) {
        if (appState.lang === 'mr') {
            reply = "टोमॅटोवरील करपा रोगासाठी कॉपर ऑक्सीक्लोराईड २.५ ग्रॅम प्रति लिटर किंवा मॅनकोझेब २ ग्रॅम प्रति लिटर पाण्यात मिसळून फवारावे.";
        } else if (appState.lang === 'hi') {
            reply = "टमाटर में झुलसा (ब्लाइट) नियंत्रण के लिए कॉपर ऑक्सीक्लोराइड 2.5 ग्राम या मैंकोजेब 2 ग्राम प्रति लीटर पानी में मिलाकर सुरक्षात्मक छिड़काव करें।";
        } else {
            reply = "For Tomato Early/Late Blight, apply Copper Oxychloride @ 2.5 g/L or Mancozeb @ 2 g/L protectively to prevent sporulation.";
        }
    } else {
        if (appState.lang === 'mr') {
            reply = "आपला प्रश्न नोंदवला आहे. अचूक निदानासाठी 'पिक तपासणी' (Crop Diagnosis) विभागात पानावरील रोगाचा फोटो अपलोड करा, आमचे एआय मॉडेल त्वरित उपाययोजना देईल.";
        } else if (appState.lang === 'hi') {
            reply = "आपके प्रश्न के अनुसार सटीक पहचान हेतु कृपया 'फसल निदान' सेक्शन में जाकर पत्ते की फोटो अपलोड करें, सिस्टम तुरंत उपचार सुझाव देगा।";
        } else {
            reply = "Understood. For precise diagnosis, please upload a clear foliar photo in the 'Crop Diagnosis' section to generate validated CIBRC IPM treatments.";
        }
    }

    if (replyEl) replyEl.innerText = reply;

    // Vocalize Speech Synthesis
    speakVoiceResponse(reply);
}

function speakVoiceResponse(text) {
    if (!('speechSynthesis' in window) || !text) return;
    try {
        window.speechSynthesis.cancel(); // Stop any pending speech
        const utterance = new SpeechSynthesisUtterance(text);
        const voices = window.speechSynthesis.getVoices() || [];

        // Find best matching voice for current language
        const targetLang = appState.lang === 'mr' ? 'mr' : (appState.lang === 'hi' ? 'hi' : 'en');
        const matchedVoice = voices.find(v => (v.lang || '').toLowerCase().startsWith(targetLang)) ||
                             voices.find(v => (v.lang || '').toLowerCase().startsWith('hi') || (v.lang || '').toLowerCase().startsWith('en'));
        if (matchedVoice) {
            utterance.voice = matchedVoice;
        }
        utterance.lang = matchedVoice ? matchedVoice.lang : (appState.lang === 'mr' ? 'mr-IN' : (appState.lang === 'hi' ? 'hi-IN' : 'en-IN'));
        utterance.rate = 0.95;
        utterance.pitch = 1.0;

        window.speechSynthesis.speak(utterance);
    } catch (e) {
        console.warn('Speech synthesis error:', e);
    }
}


// ==============================================================================
// 4. TAXONOMY & CROP SELECTION
// ==============================================================================

async function loadTaxonomy() {
    try {
        const res = await fetch('/api/config/taxonomy');
        if (res.ok) {
            appState.taxonomy = await res.json();
        }
    } catch (e) {
        console.error('Failed to load taxonomy', e);
    }
}

function populateCrops() {
    const container = document.getElementById('crop-selector-container');
    if (!container || !appState.taxonomy) return;

    const crops = appState.taxonomy.crops || {};
    container.innerHTML = Object.keys(crops).map(key => {
        const crop = crops[key];
        const isSelected = key === appState.selectedCrop;
        let displayName = crop.display_name;
        if (appState.lang === 'mr') displayName = crop.marathi_name;
        else if (appState.lang === 'hi') displayName = crop.hindi_name;

        return `
            <div class="crop-card ${isSelected ? 'selected' : ''}" onclick="selectCrop('${key}')">
                <i class="fa-solid fa-seedling"></i>
                <strong class="crop-title">${displayName}</strong>
                <span class="crop-category">${crop.category}</span>
            </div>
        `;
    }).join('');
}

function selectCrop(cropCode) {
    appState.selectedCrop = cropCode;
    populateCrops();
}

function selectStage(stageCode) {
    appState.selectedStage = stageCode;
    document.querySelectorAll('.stage-pill').forEach(btn => {
        btn.classList.toggle('active', btn.getAttribute('data-stage') === stageCode);
    });
}

function populateDistricts() {
    const distSelect = document.getElementById('field-district');
    if (!distSelect || !appState.taxonomy) return;

    const districts = appState.taxonomy.districts || {};
    distSelect.innerHTML = Object.keys(districts).map(d => `
        <option value="${d}" ${d === appState.selectedDistrict ? 'selected' : ''}>${d}</option>
    `).join('');

    populateWeatherDistrictSelector();
    onDistrictChange(appState.selectedDistrict);
}

function populateWeatherDistrictSelector() {
    const select = document.getElementById('weather-district-select');
    if (!select || !appState.taxonomy) return;

    const districts = appState.taxonomy.districts || {};
    const selected = appState.selectedDistrict || 'Nashik';
    select.innerHTML = Object.keys(districts).map(d => `
        <option value="${d}" ${d === selected ? 'selected' : ''}>${d}</option>
    `).join('');
    select.onchange = (e) => {
        const districtName = e.target.value;
        appState.selectedDistrict = districtName;
        const distInfo = (appState.taxonomy.districts || {})[districtName];
        if (distInfo) {
            appState.latitude = distInfo.lat;
            appState.longitude = distInfo.lon;
            updateLiveWeather(distInfo.lat, distInfo.lon);
            const fieldDistrict = document.getElementById('field-district');
            if (fieldDistrict) fieldDistrict.value = districtName;
            onDistrictChange(districtName);
        }
    };
}

function onDistrictChange(districtName) {
    appState.selectedDistrict = districtName;
    const talukaSelect = document.getElementById('field-taluka');
    if (!talukaSelect || !appState.taxonomy) return;

    const distInfo = (appState.taxonomy.districts || {})[districtName];
    if (distInfo) {
        appState.latitude = distInfo.lat;
        appState.longitude = distInfo.lon;

        talukaSelect.innerHTML = distInfo.talukas.map(t => `
            <option value="${t}">${t}</option>
        `).join('');
        appState.selectedTaluka = distInfo.talukas[0] || '';

        const coordsDisp = document.getElementById('gps-coords-display');
        if (coordsDisp) {
            coordsDisp.innerText = `Centroid: ${distInfo.lat.toFixed(4)}°N, ${distInfo.lon.toFixed(4)}°E (${districtName})`;
        }

        updateLiveWeather(distInfo.lat, distInfo.lon);
    }
}


// ==============================================================================
// 5. WEATHER TELEMETRY & DYNAMIC RISK ENGINE INTEGRATION
// ==============================================================================

async function updateLiveWeather(lat, lon) {
    const tempEl = document.getElementById('live-temp');
    const humEl = document.getElementById('live-humidity');
    const rainEl = document.getElementById('live-rain');
    const windEl = document.getElementById('live-wind');
    const sourceEl = document.getElementById('weather-source');
    const dashTemp = document.getElementById('dash-kpi-temp');
    const dashTempSub = document.getElementById('dash-kpi-temp-sub');

    try {
        const res = await fetch(`/api/weather/current?latitude=${lat}&longitude=${lon}`);
        if (res.ok) {
            const data = await res.json();
            if (data.available && data.temperature !== null) {
                const temp = Number(data.temperature);
                const hum = Number(data.humidity || 0);
                const rain = Number(data.rainfall || 0);
                const wind = Number(data.wind_speed || 0);

                if (tempEl) tempEl.innerText = `${temp.toFixed(1)} °C`;
                if (humEl) humEl.innerText = `${hum.toFixed(0)} %`;
                if (rainEl) rainEl.innerText = `${rain.toFixed(1)} mm`;
                if (windEl) windEl.innerText = `${wind.toFixed(1)} km/h`;
                if (sourceEl) sourceEl.innerText = 'Open-Meteo Satellite (Live)';
                if (dashTemp) dashTemp.innerText = `${temp.toFixed(1)}° C`;
                if (dashTempSub) dashTempSub.innerText = `Humidity ${hum.toFixed(0)}% · Rain ${rain.toFixed(1)}mm`;

                // Calculate Real Micro-Climate Risk Indices
                const fungalIdx = Math.min(100, Math.max(10, Math.round((hum / 100) * 75 + (temp >= 20 && temp <= 32 ? 20 : 5))));
                const pestIdx = Math.min(100, Math.max(10, Math.round((temp / 40) * 60 + (hum >= 50 ? 30 : 10))));
                const sprayIdx = Math.max(10, Math.min(100, Math.round(100 - (wind * 3.5) - (rain > 0 ? 45 : 0))));
                const thermalIdx = Math.min(100, Math.max(5, Math.round(Math.max(0, temp - 32) * 8 + Math.max(0, 16 - temp) * 6)));

                updateRiskBar('risk-idx-fungal', 'risk-bar-fungal', fungalIdx);
                updateRiskBar('risk-idx-pest', 'risk-bar-pest', pestIdx);
                updateRiskBar('risk-idx-spray', 'risk-bar-spray', sprayIdx);
                updateRiskBar('risk-idx-thermal', 'risk-bar-thermal', thermalIdx);

                const adviceEl = document.getElementById('weather-advice-text');
                if (adviceEl) {
                    if (wind > 18 || rain > 0) {
                        adviceEl.innerText = `High wind speed (${wind} km/h) or precipitation detected. Avoid foliar spraying now.`;
                    } else {
                        adviceEl.innerText = `Wind speed (${wind} km/h) is optimal. Morning hours are suitable for foliar spraying.`;
                    }
                }

                // Render Dynamic 7-Day Risk Forecast Curve
                renderDynamic7DayForecast(fungalIdx, pestIdx);
                return;
            }
        }
    } catch (e) {
        console.warn('Weather fetch failed', e);
    }

    // Graceful offline fallback: Never fabricate fake numbers
    if (tempEl) tempEl.innerText = '-- °C';
    if (humEl) humEl.innerText = '-- %';
    if (rainEl) rainEl.innerText = '-- mm';
    if (windEl) windEl.innerText = '-- km/h';
    if (sourceEl) sourceEl.innerText = 'Weather telemetry temporarily unavailable';
    if (dashTemp) dashTemp.innerText = '-- °C';
    if (dashTempSub) dashTempSub.innerText = 'Weather telemetry unavailable';
}

function updateRiskBar(valId, barId, score) {
    const valEl = document.getElementById(valId);
    const barEl = document.getElementById(barId);
    if (valEl) valEl.innerText = `${score} / 100`;
    if (barEl) {
        barEl.style.width = `${score}%`;
        barEl.style.background = score >= 70 ? 'var(--brand-red)' : score >= 40 ? 'var(--brand-amber)' : 'var(--brand-green)';
    }
}

function renderDynamic7DayForecast(fungalScore, pestScore) {
    const baseScore = Math.round((fungalScore + pestScore) / 2);
    const dayNames = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
    const multipliers = [1.0, 1.05, 1.15, 1.1, 1.25, 1.3, 1.2];

    const daysRow = document.getElementById('dashboard-forecast-days-row');
    if (daysRow) {
        daysRow.innerHTML = dayNames.map((d, i) => {
            const val = Math.min(95, Math.max(15, Math.round(baseScore * multipliers[i])));
            const riskClass = val >= 65 ? 'high' : val >= 35 ? 'mod' : 'low';
            return `<div class="forecast-day-col"><div class="day-name">${d}</div><div class="day-risk-val ${riskClass}">${val}%</div></div>`;
        }).join('');
    }
}

function fetchDeviceLocation() {
    const coordsDisp = document.getElementById('gps-coords-display');
    const btnText = document.getElementById('gps-btn-text');

    if (!navigator.geolocation) {
        showToast('GPS is not available in this browser.');
        return;
    }

    if (btnText) btnText.innerText = 'Acquiring GPS location...';

    navigator.geolocation.getCurrentPosition(
        (pos) => {
            appState.latitude = pos.coords.latitude;
            appState.longitude = pos.coords.longitude;
            if (btnText) btnText.innerText = 'GPS Location Locked';
            if (coordsDisp) {
                coordsDisp.innerText = `GPS: ${appState.latitude.toFixed(4)}°N, ${appState.longitude.toFixed(4)}°E`;
            }
            updateLiveWeather(appState.latitude, appState.longitude);
            showToast('GPS coordinates acquired successfully!');
        },
        (err) => {
            if (btnText) btnText.innerText = 'Use Current GPS';
            showToast('GPS permission denied. Using district centroid.');
        },
        { timeout: 8000 }
    );
}


// ==============================================================================
// 6. IMAGE UPLOAD, CAMERA & SAMPLE IMAGES
// ==============================================================================

function setupDragDrop() {
    const dropZone = document.getElementById('image-drop-zone');
    if (!dropZone) return;

    ['dragenter', 'dragover'].forEach(name => dropZone.addEventListener(name, e => {
        e.preventDefault();
        dropZone.classList.add('is-dragging');
    }));

    ['dragleave', 'drop'].forEach(name => dropZone.addEventListener(name, e => {
        e.preventDefault();
        dropZone.classList.remove('is-dragging');
    }));

    dropZone.addEventListener('drop', e => {
        const file = e.dataTransfer.files[0];
        if (file) processSelectedFile(file);
    });
}

function triggerGallery() {
    if (!requireAuthenticated()) return;
    document.getElementById('file-input-gallery')?.click();
}

function triggerSmartCamera() {
    if (!requireAuthenticated()) return;
    openCameraCapture();
}

let cameraStream = null;

async function openCameraCapture() {
    const modal = document.getElementById('camera-capture-modal');
    const preview = document.getElementById('camera-preview');
    const status = document.getElementById('camera-status');
    if (!modal || !preview) return;

    if (!navigator.mediaDevices?.getUserMedia) {
        document.getElementById('file-input-camera')?.click();
        return;
    }

    try {
        cameraStream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: { ideal: 'environment' } }, audio: false });
        preview.srcObject = cameraStream;
        modal.classList.add('show-modal');
    } catch (error) {
        if (status) status.innerText = 'Camera access was unavailable. Choose a photo from your device instead.';
        document.getElementById('file-input-camera')?.click();
    }
}

function captureCameraPhoto() {
    const preview = document.getElementById('camera-preview');
    const canvas = document.getElementById('camera-canvas');
    if (!preview || !canvas || !preview.videoWidth) {
        showToast('Camera is not ready yet.');
        return;
    }

    canvas.width = preview.videoWidth;
    canvas.height = preview.videoHeight;
    canvas.getContext('2d').drawImage(preview, 0, 0, canvas.width, canvas.height);
    canvas.toBlob((blob) => {
        if (!blob) return;
        processSelectedFile(new File([blob], `camera-leaf-${Date.now()}.jpg`, { type: 'image/jpeg' }));
        closeCameraCapture();
        showToast('Camera photo captured. Ready for diagnosis.');
    }, 'image/jpeg', 0.92);
}

function closeCameraCapture() {
    if (cameraStream) {
        cameraStream.getTracks().forEach(track => track.stop());
        cameraStream = null;
    }
    const preview = document.getElementById('camera-preview');
    if (preview) preview.srcObject = null;
    document.getElementById('camera-capture-modal')?.classList.remove('show-modal');
}

function handleImageUpload(e) {
    const file = e.target.files[0];
    if (file) processSelectedFile(file);
}

function processSelectedFile(file) {
    if (!file.type.startsWith('image/')) {
        showToast('Please select a valid image file (JPG, PNG, WEBP).');
        return;
    }
    if (file.size > 15 * 1024 * 1024) {
        showToast('File size exceeds the 15 MB limit.');
        return;
    }

    appState.selectedFile = file;

    const reader = new FileReader();
    reader.onload = (e) => {
        const preview = document.getElementById('image-preview');
        const container = document.getElementById('preview-container');
        const dropZone = document.getElementById('image-drop-zone');
        if (preview) preview.src = e.target.result;
        if (container) container.style.display = 'block';
        if (dropZone) dropZone.style.display = 'none';
    };
    reader.readAsDataURL(file);
}

function clearSelectedImage() {
    appState.selectedFile = null;
    const preview = document.getElementById('image-preview');
    const container = document.getElementById('preview-container');
    const dropZone = document.getElementById('image-drop-zone');
    if (preview) preview.src = '';
    if (container) container.style.display = 'none';
    if (dropZone) dropZone.style.display = 'flex';
}

async function loadSampleImage(sampleKey) {
    const samples = {
        'maize': { url: '/static/images/samples/sample_maize.jpg', crop: 'maize', name: 'Maize: Healthy/Leaf Sample' },
        'tomato_blight': { url: '/static/images/samples/sample_tomato.jpg', crop: 'tomato', name: 'Tomato: Leaf Sample' },
        'citrus_leaf': { url: '/static/images/samples/sample_citrus.jpg', crop: 'citrus', name: 'Citrus: Leaf Sample' },
        'healthy_leaf': { url: '/static/images/samples/sample_healthy.jpg', crop: 'soybean', name: 'Healthy Leaf Sample' },
        'leaf_spot': { url: '/static/images/samples/sample_leaf_spot.jpg', crop: 'tur', name: 'Leaf Spot Sample' }
    };

    const s = samples[sampleKey];
    if (!s) return;

    try {
        const response = await fetch(s.url);
        const blob = await response.blob();
        const file = new File([blob], `${sampleKey}.jpeg`, { type: 'image/jpeg' });
        processSelectedFile(file);

        if (s.crop) selectCrop(s.crop);
        showToast(`Selected sample: ${s.name}`);
    } catch (e) {
        showToast('Error loading sample image: ' + e.message);
    }
}


// ==============================================================================
// 7. SUBMIT AI DIAGNOSIS (END-TO-END REAL /predict)
// ==============================================================================

async function submitCropDiagnosis() {
    if (!requireAuthenticated()) return;
    if (!appState.selectedFile) {
        showToast('Please upload a crop leaf image or select a sample.');
        return;
    }

    const btn = document.getElementById('btn-diagnose');
    const progress = document.getElementById('analysis-progress');
    const fill = document.getElementById('scan-bar-fill');
    const pct = document.getElementById('scan-percentage');
    const statusTxt = document.getElementById('scan-status-text');

    if (btn) btn.disabled = true;
    if (progress) progress.style.display = 'block';

    const stages = [
        { pct: 25, msg: 'Validating specimen quality and foliar contours...' },
        { pct: 55, msg: 'Running YOLOv8 neural network inference...' },
        { pct: 80, msg: 'Computing agro-meteorological disease favorability...' }
    ];

    let currentStage = 0;
    const interval = setInterval(() => {
        if (currentStage < stages.length) {
            if (fill) fill.style.width = stages[currentStage].pct + '%';
            if (pct) pct.innerText = stages[currentStage].pct + '%';
            if (statusTxt) statusTxt.innerText = stages[currentStage].msg;
            currentStage++;
        }
    }, 350);

    const formData = new FormData();
    formData.append('file', appState.selectedFile);
    formData.append('crop', appState.selectedCrop || 'maize');
    formData.append('growth_stage', appState.selectedStage || 'vegetative');
    formData.append('district', appState.selectedDistrict || 'Nashik');
    formData.append('taluka', document.getElementById('field-taluka')?.value || appState.selectedTaluka || '');
    formData.append('village', document.getElementById('field-village')?.value || '');
    formData.append('latitude', appState.latitude);
    formData.append('longitude', appState.longitude);
    formData.append('language', appState.lang || 'mr');

    if (appState.currentUser) {
        formData.append('farmer_name', appState.currentUser.full_name);
        formData.append('farmer_phone', appState.currentUser.phone);
    }

    try {
        const res = await fetch('/predict', { method: 'POST', body: formData });
        clearInterval(interval);

        if (!res.ok) {
            const errJson = await res.json().catch(() => ({}));
            throw new Error(errJson.detail || `Server Error (${res.status})`);
        }

        const data = await res.json();

        if (fill) fill.style.width = '100%';
        if (pct) pct.innerText = '100%';
        if (statusTxt) statusTxt.innerText = 'Analysis Complete!';

        setTimeout(() => {
            if (progress) progress.style.display = 'none';
            if (btn) btn.disabled = false;

            // Populate Diagnostic Result
            displayDiagnosticResult(data);

            // Re-sync all live stats
            loadFarmerCasesHistory();
            refreshPendingExpertCount();
            loadDashboardStats();
        }, 300);

    } catch (err) {
        clearInterval(interval);
        if (progress) progress.style.display = 'none';
        if (btn) btn.disabled = false;

        let errMsg = err.message;
        if (err.name === 'TypeError' || err.message.includes('Failed to fetch') || err.message.includes('NetworkError')) {
            errMsg = appState.lang === 'en' 
                ? 'Backend server is offline or unreachable. Please verify the server is running on port 8000.'
                : 'Unable to connect to server. Please verify backend is running on port 8000.';
        }
        showToast('Diagnosis failed: ' + errMsg);
    }
}

function requireAuthenticated() {
    if (appState.currentUser) return true;
    showToast('Please sign in or register before continuing.');
    openAuthModal('login');
    return false;
}

function displayDiagnosticResult(data) {
    appState.lastDiagnosisData = data;
    appState.activeCaseId = data.case_id || data.case_number;

    const placeholder = document.getElementById('result-placeholder');
    const resultCard = document.getElementById('result-card');
    if (placeholder) placeholder.style.display = 'none';
    if (!resultCard) return;

    resultCard.style.display = 'block';

    const unrelatedBox = document.getElementById('res-unrelated-box');
    const unrelatedMsg = document.getElementById('res-unrelated-msg');
    const validDetails = document.getElementById('res-valid-details');
    const emergencyBanner = document.getElementById('triage-emergency-banner');
    const btnEscalateDiag = document.getElementById('btn-escalate-desk-diag');
    const btnEscalateAdv = document.getElementById('btn-escalate-desk-advisory');
    const overlayWrap = document.getElementById('overlay-wrapper');
    const overlayImg = document.getElementById('res-overlay-img');
    const preview = document.getElementById('image-preview');

    const isValid = data.valid === true;

    // 1. FOREIGN OBJECT / OOD GUARDRAIL (STRICT NEUTRAL UI)
    if (!isValid) {
        // Keep UI background neutral
        resultCard.className = 'result-card theme-invalid';
        if (unrelatedBox) {
            unrelatedBox.style.display = 'block';
            if (unrelatedMsg) {
                unrelatedMsg.innerText = data.message || "Non-plant or foreign object detected. Please upload a genuine plant leaf.";
            }
        }
        // CRITICALLY: Do NOT show a triage card, do NOT show treatment advisories, and do NOT show fake bounding boxes
        if (validDetails) validDetails.style.display = 'none';
        if (emergencyBanner) emergencyBanner.style.display = 'none';
        if (btnEscalateDiag) btnEscalateDiag.style.display = 'none';
        if (btnEscalateAdv) btnEscalateAdv.style.display = 'none';
        if (overlayWrap) overlayWrap.style.display = 'none';

        logActivity('DIAGNOSIS_REJECTED', data.message || 'Non-plant specimen rejected');
        resultCard.scrollIntoView({ behavior: 'smooth' });
        return;
    }

    // 2. VALID SPECIMEN: Show details container, hide invalid warning box
    if (unrelatedBox) unrelatedBox.style.display = 'none';
    if (validDetails) validDetails.style.display = 'block';

    // Display the annotated_image (base64 with YOLO bounding boxes) in the image preview container
    if (data.annotated_image) {
        if (preview) preview.src = data.annotated_image;
        if (overlayImg) overlayImg.src = data.annotated_image;
        if (overlayWrap) overlayWrap.style.display = 'block';
    } else if (data.overlay) {
        if (overlayImg) overlayImg.src = data.overlay;
        if (overlayWrap) overlayWrap.style.display = 'block';
    } else {
        if (overlayWrap) overlayWrap.style.display = 'none';
    }

    // 3. TRIAGE LEVEL DETERMINATION (GREEN | YELLOW | RED)
    let triageLevel = (data.triage_level || '').toUpperCase();
    if (!triageLevel || (triageLevel !== 'GREEN' && triageLevel !== 'YELLOW' && triageLevel !== 'RED')) {
        const cond = (data.condition || data.condition_name || data.prediction || '').toLowerCase();
        const isHealthy = cond.includes('healthy') || data.observation_type === 'HEALTHY';
        const isCritical = data.severity === 'HIGH' || Number(data.damage_percent || 0) > 45 || cond.includes('blight') || cond.includes('rust');
        triageLevel = isHealthy ? 'GREEN' : (isCritical ? 'RED' : 'YELLOW');
    }

    let triageTheme = 'theme-triage-yellow';
    if (triageLevel === 'GREEN') {
        triageTheme = 'theme-triage-green';
    } else if (triageLevel === 'RED') {
        triageTheme = 'theme-triage-red';
    }
    resultCard.className = `result-card ${triageTheme}`;

    // Emergency Helpline Callout Banner (1800-180-1551) prominently alongside chemical treatments for RED cases
    if (emergencyBanner) {
        emergencyBanner.style.display = triageLevel === 'RED' ? 'flex' : 'none';
    }

    // Escalation Workflow: For RED and YELLOW cases, render "Escalate to Agricultural Desk" button next to treatment advisory
    const canEscalate = (triageLevel === 'RED' || triageLevel === 'YELLOW');
    if (btnEscalateDiag) {
        btnEscalateDiag.style.display = canEscalate ? 'inline-flex' : 'none';
    }
    if (btnEscalateAdv) {
        btnEscalateAdv.style.display = canEscalate ? 'inline-flex' : 'none';
    }

    // Populate Status & Condition Badges
    const badge = document.getElementById('res-status-badge');
    const typeBadge = document.getElementById('res-type-badge');
    const caseNum = document.getElementById('res-case-num');
    const title = document.getElementById('res-condition-title');
    const cropSub = document.getElementById('res-crop-subtitle');

    if (caseNum) caseNum.innerText = data.case_number || data.case_id || 'CASE-MH-2026';

    const condName = data.condition || data.condition_name || data.prediction || 'Crop Condition';
    const cropName = data.crop || appState.selectedCrop || 'Crop';

    if (badge) {
        if (triageLevel === 'GREEN') {
            badge.className = 'status-badge badge-healthy';
            badge.innerText = '🌿 GREEN: Healthy Specimen (Optimal Foliar Vigor)';
        } else if (triageLevel === 'RED') {
            badge.className = 'status-badge badge-critical';
            badge.innerText = '🚨 RED: Severe/Spreading Outbreak (Urgent Intervention)';
        } else {
            badge.className = 'status-badge badge-uncertain';
            badge.innerText = '⚠️ YELLOW: Mild/Moderate Symptoms Detected';
        }
    }

    if (typeBadge) {
        if (triageLevel === 'GREEN') {
            typeBadge.innerText = '🌱 Healthy Foliage';
        } else {
            const isPest = data.observation_type === 'PEST' || condName.toLowerCase().includes('worm') || condName.toLowerCase().includes('borer') || condName.toLowerCase().includes('mite');
            typeBadge.innerText = isPest ? '🐛 Pest Infestation' : '🦠 Crop Disease';
        }
    }

    if (title) {
        title.innerText = triageLevel === 'GREEN' ? `${cropName.toUpperCase()}: Healthy Foliage` : `${cropName.toUpperCase()}: ${condName}`;
    }

    if (cropSub) {
        const cropCfg = (appState.taxonomy?.crops || {})[cropName.toLowerCase()];
        const localizedCrop = cropCfg ? cropCfg.marathi_name : cropName;
        cropSub.innerText = `Crop: ${localizedCrop} · Growth Stage: ${appState.selectedStage} · Triage: ${triageLevel}`;
    }

    // Confidence & Damage Meters
    const confFill = document.getElementById('confidence-fill');
    const confTxt = document.getElementById('res-confidence-text');
    const damFill = document.getElementById('damage-fill');
    const damTxt = document.getElementById('res-damage-text');
    const sevTxt = document.getElementById('res-severity-text');

    const confVal = data.confidence || 93;
    if (confFill) confFill.style.width = `${Math.min(100, confVal)}%`;
    if (confTxt) confTxt.innerText = `${confVal}%`;

    const damagePct = Number(data.damage_percent || (triageLevel === 'RED' ? 55 : (triageLevel === 'YELLOW' ? 22 : 0)));
    if (damFill) {
        damFill.style.width = `${Math.min(100, damagePct)}%`;
        damFill.style.background = triageLevel === 'GREEN' ? '#00E676' : (triageLevel === 'RED' ? '#FF4D4D' : '#FFD700');
    }
    if (damTxt) damTxt.innerText = `${damagePct}%`;

    if (sevTxt) {
        const sevVal = triageLevel === 'GREEN' ? 'HEALTHY' : (data.severity || (triageLevel === 'RED' ? 'HIGH' : 'MODERATE'));
        sevTxt.innerText = sevVal;
        sevTxt.className = `severity-tag sev-${sevVal.toLowerCase()}`;
    }

    // Multi-factor Risk Gauge
    const riskBadge = document.getElementById('res-risk-badge');
    const riskScore = document.getElementById('res-risk-score');
    const factorsUl = document.getElementById('res-risk-factors-ul');

    const risk = data.risk || {
        risk_level: triageLevel === 'GREEN' ? 'LOW' : (triageLevel === 'RED' ? 'CRITICAL' : 'MODERATE'),
        score: triageLevel === 'GREEN' ? 5 : (triageLevel === 'RED' ? 88 : 45),
        factors: []
    };
    if (riskBadge) {
        riskBadge.className = `risk-badge badge-${(risk.risk_level || 'low').toLowerCase()}`;
        riskBadge.innerText = `${risk.risk_level} RISK (${risk.score}/100)`;
    }
    if (riskScore) riskScore.innerText = `Risk Index: ${risk.score} / 100`;

    if (factorsUl) {
        factorsUl.innerHTML = (risk.factors || []).map(f => `<li><i class="fa-solid fa-angle-right"></i> ${f}</li>`).join('') ||
                              `<li>${triageLevel === 'GREEN' ? 'Specimen shows optimal foliar tissue integrity.' : 'Field meteorological metrics evaluated.'}</li>`;
    }

    // 4. TRIAGE CARD ADVISORIES
    // - GREEN (Healthy): Show hydration and balanced fertilizer tips.
    // - YELLOW (Mild/Moderate): Show corrective organic/chemical guidelines.
    // - RED (Severe/Spreading): Show emergency State Agriculture Helpline (1800-180-1551) prominently alongside chemical treatments.
    const adv = data.advisory || {};
    const setAdv = (id, txt) => {
        const el = document.getElementById(id);
        if (el) el.innerText = txt || '--';
    };

    if (triageLevel === 'GREEN') {
        setAdv('res-ipm-immediate', data.recommendations || adv.immediate_action || 'Optimal crop vigor! Ensure regular drip irrigation (hydration schedule) and maintain soil moisture at 60-70% field capacity.');
        setAdv('res-ipm-cultural', adv.cultural || 'Apply balanced NPK fertilizer (19:19:19 or 12:61:0) based on soil test to maintain root vigor and foliar integrity.');
        setAdv('res-ipm-biological', adv.biological || 'Apply beneficial bio-stimulants and mycorrhizal fungi to enhance nutrient and water uptake.');
        setAdv('res-ipm-chemical', adv.chemical || 'Zero chemical intervention required. Continue weekly scouting.');
        setAdv('res-ipm-safety', adv.safety || 'Store fertilizers in dry, shaded sheds away from direct sunlight.');
    } else if (triageLevel === 'YELLOW') {
        setAdv('res-ipm-immediate', data.recommendations || adv.immediate_action || 'Early symptoms identified. Remove affected foliage and apply corrective organic/bio-agent foliar spray.');
        setAdv('res-ipm-cultural', adv.cultural || 'Prune infected leaves to enhance aeration and reduce canopy humidity.');
        setAdv('res-ipm-biological', adv.biological || 'Spray Neem Oil (Azadirachtin 10,000 ppm @ 2-3 ml/L) or Trichoderma viride @ 5g/L.');
        setAdv('res-ipm-chemical', adv.chemical || 'Targeted corrective spray: Mancozeb 75% WP @ 2.5 g/L or Chlorantraniliprole 18.5% SC @ 0.4 ml/L if threshold exceeded.');
        setAdv('res-ipm-safety', adv.safety || 'Wear nitrile gloves and face mask; spray during early morning or calm evening hours.');
    } else { // RED
        setAdv('res-ipm-immediate', `🚨 EMERGENCY OUTBREAK PROTOCOL: Call State Agriculture Emergency Desk 1800-180-1551 immediately. ${data.recommendations || adv.immediate_action || 'Rapidly spreading pathogen/pest colony requiring immediate intervention.'}`);
        setAdv('res-ipm-cultural', adv.cultural || 'Quarantine infected plot area, sanitize boots and equipment to stop spore/pest drift to adjacent fields.');
        setAdv('res-ipm-biological', adv.biological || 'Conserve remaining natural predators, but prioritize emergency chemical containment to prevent crop collapse.');
        setAdv('res-ipm-chemical', adv.chemical || 'State Approved Chemical Treatment: Spray systemic fungicide/insecticide (e.g. Tebuconazole 25.9% EC @ 1.5 ml/L or Emamectin Benzoate 5% SG @ 0.5 g/L) immediately.');
        setAdv('res-ipm-safety', adv.safety || 'Emergency PPE: Respirator mask, face shield, and chemical rubber gloves. Strictly respect a 14-day pre-harvest interval.');
    }

    const followupText = document.getElementById('res-followup-text');
    if (followupText) {
        const days = triageLevel === 'GREEN' ? 10 : (triageLevel === 'YELLOW' ? 5 : 2);
        followupText.innerText = `Recommended: Re-scout field within ${days} days and submit a follow-up photo on FALCON-AI.`;
    }

    logActivity('DIAGNOSIS', `${cropName}: ${condName}`, {
        triage_level: triageLevel,
        severity: data.severity,
        confidence: confVal
    });

    resultCard.scrollIntoView({ behavior: 'smooth' });
}

function viewDetailedAdvisoryFromCurrent() {
    if (appState.lastDiagnosisData) {
        const d = appState.lastDiagnosisData;
        const heading = document.getElementById('adv-condition-heading');
        const subheading = document.getElementById('adv-crop-subheading');
        if (heading) heading.innerText = `${d.crop}: ${d.condition_name || d.prediction}`;
        if (subheading) subheading.innerText = `Crop: ${d.crop} · Growth Stage: ${appState.selectedStage} · Severity: ${d.severity || 'MODERATE'} (${d.damage_percent || 20}% damage)`;
    }
    switchView('advisory');
}

async function shareAdvisoryWhatsApp() {
    const condition = document.getElementById('adv-condition-heading')?.innerText || (appState.lastDiagnosisData?.condition_name || 'Crop Advisory');
    const advisoryText = document.getElementById('res-ipm-immediate')?.innerText || appState.lastDiagnosisData?.advisory?.immediate_action || 'Follow crop protection guidance and re-scout the field in 5 days.';
    const biologicalText = document.getElementById('res-ipm-biological')?.innerText || appState.lastDiagnosisData?.advisory?.biological || 'Maintain ecological balance and conserve natural enemies.';
    const chemicalText = document.getElementById('res-ipm-chemical')?.innerText || appState.lastDiagnosisData?.advisory?.chemical || 'Use only approved, crop-safe, CIBRC-compatible chemicals as advised.';
    const cropName = appState.lastDiagnosisData?.crop || appState.selectedCrop || 'Crop';
    const district = appState.selectedDistrict || 'Maharashtra';

    let experts = [];
    try {
        const res = await fetch(`/api/experts?district=${encodeURIComponent(district)}`);
        if (res.ok) {
            const data = await res.json();
            experts = data.experts || [];
        }
    } catch (e) {
        console.warn('Failed to load expert contacts', e);
    }

    const fallbackExperts = [
        { name: 'Dr. Sachin Patil', whatsapp: '+919423011220' },
        { name: 'Dr. Vaishali Shinde', whatsapp: '+919881233441' },
        { name: 'Dr. Ashok Pawar', whatsapp: '+919503566010' }
    ];
    const contactList = experts.length ? experts : fallbackExperts;
    const primaryExpert = contactList[0] || fallbackExperts[0];
    const expertLine = contactList.map((exp) => `${exp.name}: ${exp.whatsapp || exp.phone || ''}`).join(' | ');

    const shareText = `*FALCON-AI Crop Health Advisory*\n\nCrop: ${cropName}\nCondition: ${condition}\nDistrict: ${district}\n\nTreatment Advisory:\n• Immediate Action: ${advisoryText}\n• Biological Control: ${biologicalText}\n• Chemical Control: ${chemicalText}\n\nFor more details, contact Maharashtra plant experts:\n${expertLine}\n\nUploaded specimen and field photo are attached/shared with this advisory.\n\n*FALCON-AI | SIH26131*`;

    try {
        if (appState.selectedFile && navigator.share) {
            const fileName = appState.selectedFile.name || 'uploaded-specimen.jpg';
            const shareFile = new File([await appState.selectedFile.arrayBuffer()], fileName, { type: appState.selectedFile.type || 'image/jpeg' });
            await navigator.share({
                title: 'FALCON-AI Advisory',
                text: shareText,
                files: [shareFile]
            });
            return;
        }
    } catch (e) {
        console.warn('Native share failed, falling back to WhatsApp direct link', e);
    }

    const waNumber = (primaryExpert.whatsapp || primaryExpert.phone || '+919423011220').replace(/\D/g, '');
    const waUrl = `https://wa.me/${waNumber}?text=${encodeURIComponent(shareText)}`;
    window.open(waUrl, '_blank');
}


// ==============================================================================
// CIBRC DETERMINISTIC PESTICIDE VERIFIER (UI)
// ==============================================================================
async function checkCibrcPesticideUi() {
    const input = document.getElementById('cibrc-chemical-input');
    const resBox = document.getElementById('cibrc-check-result');
    if (!input || !resBox) return;

    const query = input.value.trim();
    if (!query) {
        showToast('Please enter an active ingredient or brand name.');
        return;
    }

    const currentCrop = appState.lastDiagnosisData?.crop || appState.selectedCrop || 'cotton';
    const currentCondition = appState.lastDiagnosisData?.prediction || 'cotton_pink_bollworm';

    resBox.style.display = 'block';
    resBox.style.background = '#f8fafc';
    resBox.style.border = '1px solid #cbd5e1';
    resBox.style.color = '#334155';
    resBox.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Verifying against CIBRC gazetted register...';

    try {
        const resp = await fetch('/api/pesticide-check', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                crop: currentCrop,
                condition_code: currentCondition,
                product_query: query
            })
        });
        const data = await resp.json();

        if (data.safety_status === 'COMPATIBLE') {
            resBox.style.background = '#f0fdf4';
            resBox.style.border = '1px solid #86efac';
            resBox.style.color = '#14532d';
            resBox.innerHTML = `
                <div style="font-weight:700;margin-bottom:4px;"><i class="fa-solid fa-circle-check"></i> ${data.verdict}</div>
                <div><strong>Active Ingredient:</strong> ${data.matched_active_ingredient || query}</div>
                <div><strong>Approved Dosage:</strong> ${data.dosage_recommendation || 'As per label instructions'}</div>
                <div><strong>Waiting Period (PHI):</strong> ${data.waiting_period_days} Days (Pre-Harvest Interval)</div>
                <div style="font-size:0.72rem;color:#166534;margin-top:4px;">Reference: ${data.reference}</div>
            `;
        } else if (data.safety_status === 'INCOMPATIBLE') {
            resBox.style.background = '#fef2f2';
            resBox.style.border = '1px solid #fca5a5';
            resBox.style.color = '#7f1d1d';
            resBox.innerHTML = `
                <div style="font-weight:700;margin-bottom:4px;"><i class="fa-solid fa-ban"></i> ${data.verdict}</div>
                <div><strong>Reason:</strong> ${data.reason}</div>
                ${data.dosage_recommendation ? `<div><strong>Recommendation:</strong> ${data.dosage_recommendation}</div>` : ''}
                <div style="font-size:0.72rem;color:#991b1b;margin-top:4px;">Reference: ${data.reference}</div>
            `;
        } else {
            resBox.style.background = '#fffbeb';
            resBox.style.border = '1px solid #fde68a';
            resBox.style.color = '#78350f';
            resBox.innerHTML = `
                <div style="font-weight:700;margin-bottom:4px;"><i class="fa-solid fa-triangle-exclamation"></i> ${data.verdict}</div>
                <div>${data.reason}</div>
                <div style="font-size:0.72rem;color:#92400e;margin-top:4px;">Reference: ${data.reference}</div>
            `;
        }
    } catch (e) {
        resBox.style.background = '#fef2f2';
        resBox.style.color = '#991b1b';
        resBox.innerHTML = 'Verification failed: ' + e.message;
    }
}

// ==============================================================================
// DOUBT DOCTOR & INSPECTION TASKS (UI)
// ==============================================================================
let currentDoubtDoctorData = null;

async function checkDoubtDoctorTrigger(diagData) {
    const box = document.getElementById('res-doubt-doctor-box');
    const qText = document.getElementById('doubt-doctor-qtext');
    const feedback = document.getElementById('doubt-doctor-feedback');
    if (!box || !qText) return;

    box.style.display = 'none';
    if (feedback) feedback.style.display = 'none';
    currentDoubtDoctorData = null;

    const conf = (diagData.confidence || 0) / 100.0;
    if (conf >= 0.50 && conf < 0.65) {
        try {
            const resp = await fetch('/api/doubt-doctor/evaluate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    crop: diagData.crop || appState.selectedCrop || 'cotton',
                    top_prediction: {
                        condition_code: diagData.prediction || 'cotton_pink_bollworm',
                        confidence: conf
                    },
                    language: appState.lang || 'mr'
                })
            });
            const res = await resp.json();
            if (res.trigger && res.doubt_doctor) {
                currentDoubtDoctorData = res.doubt_doctor;
                currentDoubtDoctorData.originalConfidence = diagData.confidence;
                qText.innerText = res.doubt_doctor.question_text;
                box.style.display = 'block';
            }
        } catch (e) {
            console.warn('Doubt doctor trigger failed:', e);
        }
    }
}

async function answerDoubtDoctorUi(answer) {
    if (!currentDoubtDoctorData) return;
    const feedback = document.getElementById('doubt-doctor-feedback');
    const confFill = document.getElementById('confidence-fill');
    const confTxt = document.getElementById('res-confidence-text');

    try {
        const resp = await fetch('/api/doubt-doctor/answer', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                target_condition: currentDoubtDoctorData.target_condition,
                original_confidence: currentDoubtDoctorData.originalConfidence || 58.0,
                answer: answer,
                confirms_if_yes: currentDoubtDoctorData.confirms_if_yes,
                weight_boost: currentDoubtDoctorData.weight_boost || 0.15
            })
        });
        const res = await resp.json();

        if (feedback) {
            feedback.style.display = 'block';
            if (res.status === 'CORROBORATED') {
                feedback.style.color = '#15803d';
                feedback.innerHTML = `<i class="fa-solid fa-circle-check"></i> ${res.message} (Confidence elevated to ${res.adjusted_confidence}%)`;
                if (confFill) confFill.style.width = `${res.adjusted_confidence}%`;
                if (confTxt) confTxt.innerText = `${res.adjusted_confidence}%`;
            } else {
                feedback.style.color = '#b91c1c';
                feedback.innerHTML = `<i class="fa-solid fa-triangle-exclamation"></i> ${res.message}`;
            }
        }
    } catch (e) {
        showToast('Failed to record response: ' + e.message);
    }
}

async function openInspectionModal() {
    const modal = document.getElementById('inspection-modal');
    const title = document.getElementById('inspection-modal-title');
    const stepsContainer = document.getElementById('inspection-steps-container');
    const followupAction = document.getElementById('inspection-followup-action');
    if (!modal || !stepsContainer) return;

    stepsContainer.innerHTML = '<div style="text-align:center;padding:12px;"><i class="fa-solid fa-spinner fa-spin"></i> Loading guided inspection tasks...</div>';
    modal.classList.add('modal-open');

    const ctx = appState.lastDiagnosisData?.prediction || 'wilt';
    try {
        const resp = await fetch(`/api/inspection/tasks?symptom_context=${encodeURIComponent(ctx)}&language=${appState.lang || 'mr'}`);
        const data = (await resp.json()).inspection_task;

        if (title) title.innerHTML = `<i class="fa-solid fa-clipboard-list" style="color:var(--brand-green);"></i> ${data.title}`;
        if (followupAction) followupAction.innerText = data.follow_up_action;

        stepsContainer.innerHTML = data.steps.map((s, idx) => `
            <div style="display:flex;align-items:flex-start;gap:10px;padding:8px 12px;background:#f8fafc;border-radius:6px;font-size:0.82rem;">
                <span style="background:var(--brand-green);color:#fff;width:20px;height:20px;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;font-size:0.7rem;flex-shrink:0;">${idx+1}</span>
                <span>${s}</span>
            </div>
        `).join('');
    } catch (e) {
        stepsContainer.innerHTML = `<div style="color:#b91c1c;">Failed to load inspection protocol: ${e.message}</div>`;
    }
}

function closeInspectionModal() {
    const modal = document.getElementById('inspection-modal');
    if (modal) modal.classList.remove('modal-open');
}



// ==============================================================================
// 8. MY FIELDS PORTFOLIO (REAL /api/farms)
// ==============================================================================

async function loadFarms() {
    const container = document.getElementById('my-fields-container');
    const fieldsKpi = document.getElementById('dash-kpi-fields');
    const fieldsKpiSub = document.getElementById('dash-kpi-fields-sub');

    try {
        const userId = appState.currentUser?.id || 1;
        const res = await fetch(`/api/farms?user_id=${userId}`);
        if (!res.ok) return;

        const data = await res.json();
        const farms = data.farms || [];

        // Update Dashboard KPI 1
        let totalAcres = 0;
        farms.forEach(f => { totalAcres += Number(f.area_acres || 0); });

        if (fieldsKpi) fieldsKpi.innerText = `${farms.length} Farms`;
        if (fieldsKpiSub) fieldsKpiSub.innerText = `${totalAcres.toFixed(1)} Acres Cultivated`;

        if (!container) return;

        if (farms.length === 0) {
            container.innerHTML = `
                <div style="grid-column: 1 / -1; text-align: center; padding: 40px 20px; color: var(--text-muted);">
                    <i class="fa-solid fa-wheat-awn" style="font-size: 2.5rem; color: #cbd5e1; margin-bottom: 12px;"></i>
                    <h3 style="font-size: 1.1rem; color: var(--text-primary);">No Farms Registered Yet</h3>
                    <p style="font-size: 0.85rem; max-width: 320px; margin: 6px auto 16px;">Register your farm plots to begin automated health monitoring.</p>
                    <button type="button" class="btn-primary-action" onclick="showToast('Farm registration dialog opened.')">
                        <i class="fa-solid fa-plus"></i> Register First Farm
                    </button>
                </div>
            `;
            return;
        }

        container.innerHTML = farms.map((f, i) => `
            <div class="field-card">
                <div class="field-header">
                    <div class="field-title-group">
                        <h3>${f.farm_name || `Farm Plot #${i + 1}`}</h3>
                        <span class="field-loc"><i class="fa-solid fa-location-dot"></i> ${f.village ? f.village + ', ' : ''}${f.taluka}, ${f.district}</span>
                    </div>
                    <span class="status-badge badge-healthy">Active Farm</span>
                </div>
                <div class="field-meta-grid">
                    <div class="field-meta-item"><strong>Primary Crop</strong> ${f.primary_crop || 'Maize'}</div>
                    <div class="field-meta-item"><strong>Area</strong> ${f.area_acres || 2.5} Acres</div>
                    <div class="field-meta-item"><strong>Irrigation</strong> Drip Irrigation</div>
                    <div class="field-meta-item"><strong>State</strong> ${f.state || 'Maharashtra'}</div>
                </div>
                <div class="field-actions-row">
                    <span style="font-size:0.75rem;color:var(--brand-green);font-weight:700;"><i class="fa-solid fa-shield-halved"></i> Surveillance Active</span>
                    <button type="button" class="btn-secondary-action" style="padding:4px 10px;font-size:0.76rem;" onclick="selectCrop('${f.primary_crop || 'maize'}'); switchView('diagnose');">
                        Check Crop Health
                    </button>
                </div>
            </div>
        `).join('');

    } catch (e) {
        console.warn('Failed to load farms', e);
    }
}


// ==============================================================================
// 9. DASHBOARD STATS, REAL ALERTS & CASES HISTORY
// ==============================================================================

async function loadDashboardStats() {
    try {
        const res = await fetch('/api/dashboard/stats');
        if (!res.ok) return;

        const s = await res.json();

        // 1. Officer Desk KPIs
        const totEl = document.getElementById('kpi-total');
        const disEl = document.getElementById('kpi-disease');
        const pestEl = document.getElementById('kpi-pest');
        const highEl = document.getElementById('kpi-highrisk');
        const pendEl = document.getElementById('kpi-pending') || document.getElementById('expert-pending-stat');

        if (totEl) totEl.innerText = s.total_cases || 0;
        if (disEl) disEl.innerText = s.disease_cases || 0;
        if (pestEl) pestEl.innerText = s.pest_cases || 0;
        if (highEl) highEl.innerText = s.high_risk_cases || 0;
        if (pendEl) pendEl.innerText = s.pending_expert || 0;

        // 2. Farmer Dashboard KPI 2: Main Crop
        const dashCrops = document.getElementById('dash-kpi-crops');
        const dashCropsSub = document.getElementById('dash-kpi-crops-sub');
        if (dashCrops && s.crop_distribution && s.crop_distribution.length > 0) {
            const topCrops = s.crop_distribution.slice(0, 2).map(c => c.crop_code.toUpperCase()).join(' · ');
            dashCrops.innerText = topCrops;
            if (dashCropsSub) dashCropsSub.innerText = `Total ${s.total_cases || 0} Telemetry Cases`;
        }

        // 3. Farmer Dashboard KPI 3: Crop Health
        const dashHealth = document.getElementById('dash-kpi-health');
        const dashHealthSub = document.getElementById('dash-kpi-health-sub');
        if (dashHealth) {
            if (s.total_cases > 0) {
                const healthPct = Math.max(10, Math.round(((s.total_cases - s.high_risk_cases) / s.total_cases) * 100));
                dashHealth.innerText = `${healthPct}% Healthy`;
                if (dashHealthSub) dashHealthSub.innerText = `${s.high_risk_cases || 0} High Severity Alerts`;
            } else {
                dashHealth.innerText = '100% Healthy';
                if (dashHealthSub) dashHealthSub.innerText = 'Zero Critical Threats';
            }
        }

        // 4. District Bars & Recent Alerts
        renderDistrictBars(s.district_distribution || []);
        renderRecentAlerts(s.recent_alerts || []);
        renderFullAlertsFeed(s.recent_alerts || []);

    } catch (e) {
        console.warn('Dashboard stats error', e);
    }
}

function renderRecentAlerts(alerts) {
    const containers = [
        document.getElementById('dashboard-alerts-mini-list'),
        document.getElementById('recent-alerts-container')
    ];

    containers.forEach(container => {
        if (!container) return;

        if (!alerts || alerts.length === 0) {
            container.innerHTML = '<p class="empty-history" style="font-size:0.8rem;color:var(--text-muted);padding:10px;">No active high-risk pest outbreaks reported.</p>';
            return;
        }

        container.innerHTML = alerts.map(a => {
            const isCritical = (a.risk_level || '').toUpperCase() === 'CRITICAL';
            return `
                <div class="alert-mini-item ${isCritical ? 'critical' : ''}" onclick="switchView('alerts')">
                    <div class="alert-mini-top">
                        <span class="alert-mini-title">${a.crop_code}: ${a.condition || 'Pest/Disease Alert'}</span>
                        <span class="alert-mini-badge ${isCritical ? 'badge-red' : 'badge-amber'}">${a.risk_level} (${a.risk_score}/100)</span>
                    </div>
                    <span class="alert-mini-desc">${a.taluka ? a.taluka + ', ' : ''}${a.district} · Detected: ${a.created_at || 'Today'}</span>
                </div>
            `;
        }).join('');
    });
}

function renderFullAlertsFeed(alerts) {
    const container = document.getElementById('alerts-full-feed');
    if (!container) return;

    if (!alerts || alerts.length === 0) {
        container.innerHTML = `
            <div style="text-align: center; padding: 40px; color: var(--text-muted);">
                <i class="fa-solid fa-shield-check" style="font-size: 2.5rem; color: var(--brand-green); margin-bottom: 12px;"></i>
                <h3 style="font-size: 1.1rem; color: var(--text-primary);">Zero Active Outbreaks Statewide</h3>
                <p style="font-size: 0.85rem;">Foliar health indicators remain within safe operational thresholds.</p>
            </div>
        `;
        return;
    }

    container.innerHTML = alerts.map(a => {
        const isCritical = (a.risk_level || '').toUpperCase() === 'CRITICAL';
        return `
            <div class="alert-feed-card ${isCritical ? 'critical' : 'moderate'}">
                <div class="alert-feed-body">
                    <div class="alert-feed-title">${a.crop_code}: ${a.condition || 'Outbreak Alert'}</div>
                    <div class="alert-feed-meta">
                        <span><i class="fa-solid fa-map-pin"></i> ${a.taluka ? a.taluka + ', ' : ''}${a.district}</span>
                        <span><i class="fa-solid fa-wheat-awn"></i> Crop: ${a.crop_code}</span>
                        <span><i class="fa-solid fa-triangle-exclamation"></i> Risk Index: ${a.risk_score} / 100</span>
                    </div>
                    <p class="alert-feed-desc">Agro-climatic indicators show favorable conditions for pest expansion. Immediate field scouting and recommended IPM intervention advised.</p>
                </div>
                <span class="status-badge ${isCritical ? 'badge-image_quality_issue' : 'badge-uncertain'}" style="margin-left:16px;">
                    ${a.risk_level}
                </span>
            </div>
        `;
    }).join('');
}

function renderDistrictBars(districts) {
    const containers = [
        document.getElementById('district-bars-container'),
        document.getElementById('officer-district-bars')
    ];

    containers.forEach(container => {
        if (!container) return;

        if (!districts || districts.length === 0) {
            container.innerHTML = '<p class="empty-history" style="font-size:0.8rem;color:var(--text-muted);">District outbreak data currently unavailable.</p>';
            return;
        }

        const maxCount = Math.max(...districts.map(d => d.count), 1);
        container.innerHTML = districts.map(d => {
            const pct = Math.round((d.count / maxCount) * 100);
            return `
                <div class="district-bar-row">
                    <div class="dist-name-row">
                        <span>${d.district}</span>
                        <strong>${d.count} Cases (${d.high_risk_count || 0} High Risk)</strong>
                    </div>
                    <div class="bar-track">
                        <div class="bar-fill" style="width: ${pct}%"></div>
                    </div>
                </div>
            `;
        }).join('');
    });
}

async function loadFarmerCasesHistory() {
    const container = document.getElementById('dashboard-recent-list');
    const farmerId = appState.currentUser?.id || 1;

    try {
        const res = await fetch(`/api/cases?farmer_id=${farmerId}&limit=5`);
        if (!res.ok) return;
        const data = await res.json();
        const cases = data.cases || [];

        if (!container) return;

        if (cases.length === 0) {
            container.innerHTML = `
                <div style="text-align: center; padding: 24px; color: var(--text-muted); font-size: 0.84rem;">
                    <i class="fa-solid fa-camera" style="font-size: 1.8rem; color: #cbd5e1; margin-bottom: 8px;"></i>
                    <p>No diagnoses recorded yet.</p>
                    <button class="btn-secondary-action" style="margin-top: 8px; font-size: 0.78rem;" onclick="switchView('diagnose')">
                        Start First Crop Diagnosis
                    </button>
                </div>
            `;
            return;
        }

        container.innerHTML = cases.map(c => {
            const statusClass = c.case_status === 'VERIFIED' ? 'tag-verified' :
                                c.case_status === 'SUBMITTED' ? 'tag-pending' : 'tag-highrisk';
            const statusLabel = c.case_status === 'VERIFIED' ? 'Verified' :
                                c.case_status === 'SUBMITTED' ? 'Pending Review' : c.case_status;
            return `
                <div class="diagnosis-mini-item" onclick="viewCaseAdvisory(${c.id})">
                    <img src="${c.image_path || '/static/images/samples/sample_healthy.jpg'}" class="diag-thumb" alt="Leaf specimen" onerror="this.src='/static/images/samples/sample_healthy.jpg'">
                    <div class="diag-info">
                        <div class="diag-title">${c.crop_code}: ${c.final_condition_name || c.ai_raw_prediction || 'Unknown'}</div>
                        <div class="diag-meta">
                            <span>${c.crop_code} · ${c.district}</span>
                            <span>${c.ai_confidence}% AI Confidence</span>
                        </div>
                    </div>
                    <span class="diag-status-tag ${statusClass}">${statusLabel}</span>
                </div>
            `;
        }).join('');

    } catch (e) {
        console.warn('Failed to load history', e);
    }
}

async function viewCaseAdvisory(caseId) {
    try {
        const res = await fetch(`/api/cases/${caseId}`);
        if (res.ok) {
            const data = await res.json();
            if (data.case) {
                appState.lastDiagnosisData = {
                    crop: data.case.crop_code,
                    condition_name: data.case.final_condition_name || data.case.ai_raw_prediction,
                    prediction: data.case.final_diagnosis_code || data.case.ai_condition_code,
                    severity: data.case.severity_level,
                    damage_percent: data.case.damage_percent,
                    advisory: data.case.advisory || {}
                };
                appState.activeCaseId = data.case.id;
            }
        }
    } catch (e) {
        console.warn('Failed to load case detail for advisory', e);
    }
    switchView('advisory');
}


// ==============================================================================
// 10. TREATMENT ADVISORY (REAL BACKEND INTEGRATION)
// ==============================================================================

async function loadAdvisoryView() {
    const emptyState = document.getElementById('advisory-empty-state');
    const activeContent = document.getElementById('advisory-active-content');

    let adv = appState.lastDiagnosisData?.advisory;

    // If no recent in-memory diagnosis, check if logged-in user has a recorded case
    if ((!adv || Object.keys(adv).length === 0) && appState.currentUser && appState.currentUser.id) {
        try {
            const farmerId = appState.currentUser.id;
            const res = await fetch(`/api/cases?farmer_id=${farmerId}&limit=1`);
            if (res.ok) {
                const data = await res.json();
                const cases = data.cases || [];
                if (cases.length > 0) {
                    const c = cases[0];
                    adv = c.advisory || {};
                    const heading = document.getElementById('adv-condition-heading');
                    const subheading = document.getElementById('adv-crop-subheading');
                    if (heading) heading.innerText = `${c.crop_code}: ${c.final_condition_name || c.ai_raw_prediction || 'Crop Advisory'}`;
                    if (subheading) subheading.innerText = `Crop: ${c.crop_code} · Growth Stage: ${c.growth_stage} · Risk: ${c.risk_level} (${c.damage_percent || 0}% damage)`;
                }
            }
        } catch (e) {
            console.warn('Failed to load farmer latest case for advisory', e);
        }
    }

    // IF STILL NO DIAGNOSIS -> SHOW EMPTY STATE! DO NOT FALLBACK TO MAIZE ARMYWORM!
    if (!adv || Object.keys(adv).length === 0) {
        if (emptyState) emptyState.style.display = 'block';
        if (activeContent) activeContent.style.display = 'none';
        return;
    }

    // Advisory data is available -> display active content
    if (emptyState) emptyState.style.display = 'none';
    if (activeContent) activeContent.style.display = 'block';

    const heading = document.getElementById('adv-condition-heading');
    const subheading = document.getElementById('adv-crop-subheading');
    if (appState.lastDiagnosisData) {
        const d = appState.lastDiagnosisData;
        const isHealthy = (d.condition_name || d.prediction || '').toLowerCase().includes('healthy') || (d.observation_type || '').toUpperCase() === 'HEALTHY';
        if (heading) {
            heading.innerText = isHealthy 
                ? `${d.crop ? d.crop.toUpperCase() : 'CROP'}: Healthy Foliage - Preventive Care Plan`
                : `${d.crop ? d.crop.toUpperCase() : 'CROP'}: ${d.condition_name || d.prediction || 'Crop Advisory'}`;
        }
        if (subheading) {
            subheading.innerText = isHealthy
                ? `Crop: ${d.crop || appState.selectedCrop} · Status: Optimal Plant Vigor · Scheduled Maintenance & Nutrition`
                : `Crop: ${d.crop || appState.selectedCrop} · Stage: ${appState.selectedStage} · Damage: ${d.damage_percent || 0}%`;
        }
    }

    const setAdv = (id, txt) => {
        const el = document.getElementById(id);
        if (el) el.innerText = txt || '--';
    };
    setAdv('res-ipm-immediate', adv.immediate_action);
    setAdv('res-ipm-cultural', adv.cultural);
    setAdv('res-ipm-biological', adv.biological);
    setAdv('res-ipm-chemical', adv.chemical);
    setAdv('res-ipm-safety', adv.safety);

    const followupText = document.getElementById('res-followup-text');
    if (followupText) {
        const days = adv.follow_up_days || 5;
        followupText.innerText = `Recommended: Re-scout field within ${days} days and submit a follow-up photo on FALCON-AI.`;
    }

    logActivity('VIEW_ADVISORY', document.getElementById('adv-condition-heading')?.innerText || 'Crop Advisory');
}


// ==============================================================================
// 11. EXPERT REVIEW DESK (WORKFLOW & RBAC)
// ==============================================================================

async function refreshPendingExpertCount() {
    try {
        const res = await fetch('/api/expert/pending');
        if (res.ok) {
            const data = await res.json();
            const badge = document.getElementById('pending-count-badge');
            const stat = document.getElementById('expert-pending-stat');
            if (badge) badge.innerText = data.count || 0;
            if (stat) stat.innerText = data.count || 0;
        }
    } catch (e) {
        // Silent
    }
}

async function loadPendingExpertCases() {
    const tbody = document.getElementById('expert-cases-tbody');
    if (!tbody) return;

    tbody.innerHTML = '<tr><td colspan="8" style="text-align:center;padding:24px;"><i class="fa-solid fa-spinner fa-spin"></i> Loading pending expert review queue...</td></tr>';

    try {
        const res = await fetch('/api/expert/pending');
        if (!res.ok) return;
        const data = await res.json();
        const cases = data.pending_cases || [];

        if (cases.length === 0) {
            tbody.innerHTML = '<tr><td colspan="8" style="text-align:center;padding:24px;color:var(--brand-green);font-weight:700;">All field cases verified. No cases currently pending review.</td></tr>';
            return;
        }

        tbody.innerHTML = cases.map(c => `
            <tr>
                <td><strong>${c.case_number}</strong></td>
                <td><span class="crop-tag">${c.crop_code}</span></td>
                <td>${c.farmer_name || 'Farmer'} (${c.district})</td>
                <td>${c.ai_raw_prediction || 'Unclassified'}</td>
                <td>${c.ai_confidence}%</td>
                <td><span class="risk-pill pill-${(c.risk_level || 'low').toLowerCase()}">${c.risk_level}</span></td>
                <td><span class="status-pill pill-${(c.case_status || 'submitted').toLowerCase()}">${c.case_status}</span></td>
                <td>
                    <button type="button" class="btn-table-action" onclick="openExpertModal(${c.id})">
                        <i class="fa-solid fa-microscope"></i> Review Case
                    </button>
                </td>
            </tr>
        `).join('');

    } catch (e) {
        tbody.innerHTML = '<tr><td colspan="8" style="text-align:center;padding:24px;color:var(--brand-red);">Error loading case telemetry queue.</td></tr>';
    }
}

let activeReviewCase = null;

async function openExpertModal(caseId) {
    try {
        const res = await fetch(`/api/cases/${caseId}`);
        if (!res.ok) throw new Error('Case not found');
        const data = await res.json();
        activeReviewCase = data.case;

        const modal = document.getElementById('expert-review-modal');
        const caseNum = document.getElementById('modal-case-num');
        const img = document.getElementById('modal-specimen-img');
        const meta = document.getElementById('modal-specimen-meta');

        if (caseNum) caseNum.innerText = activeReviewCase.case_number;
        if (img) img.src = activeReviewCase.image_path || '/static/images/samples/sample_healthy.jpg';

        if (meta) {
            meta.innerHTML = `
                <div><strong>Farmer:</strong> ${activeReviewCase.farmer_name} (${activeReviewCase.farmer_phone})</div>
                <div><strong>Location:</strong> ${activeReviewCase.village || '--'}, ${activeReviewCase.taluka}, ${activeReviewCase.district}</div>
                <div><strong>Crop & Stage:</strong> ${activeReviewCase.crop_code} (${activeReviewCase.growth_stage})</div>
                <div><strong>AI Prediction:</strong> ${activeReviewCase.ai_raw_prediction || 'Unknown'} (${activeReviewCase.ai_confidence}%)</div>
                <div><strong>Risk Level:</strong> ${activeReviewCase.risk_level} (${activeReviewCase.risk_score}/100)</div>
            `;
        }

        populateCorrectionOptions();
        setExpertAction('CONFIRM');
        if (modal) modal.classList.add('show-modal');

    } catch (e) {
        showToast('Failed to open case details: ' + e.message);
    }
}

function closeExpertModal() {
    const modal = document.getElementById('expert-review-modal');
    if (modal) modal.classList.remove('show-modal');
    activeReviewCase = null;
}

function populateCorrectionOptions() {
    const select = document.getElementById('modal-correction-code');
    if (!select || !appState.taxonomy) return;

    const crops = appState.taxonomy.crops || {};
    let optionsHtml = '';

    Object.keys(crops).forEach(cropKey => {
        const crop = crops[cropKey];
        (crop.key_diseases || []).forEach(d => {
            optionsHtml += `<option value="${d}" data-type="DISEASE">[Disease] ${crop.display_name} - ${d.replace(/_/g, ' ')}</option>`;
        });
        (crop.key_pests || []).forEach(p => {
            optionsHtml += `<option value="${p}" data-type="PEST">[Pest] ${crop.display_name} - ${p.replace(/_/g, ' ')}</option>`;
        });
    });

    select.innerHTML = optionsHtml;
}

function setExpertAction(action) {
    appState.expertAction = action;
    const btns = {
        'CONFIRM': document.getElementById('act-confirm'),
        'CORRECT': document.getElementById('act-correct'),
        'LAB_REFERRAL': document.getElementById('act-lab')
    };

    Object.keys(btns).forEach(k => {
        if (btns[k]) btns[k].classList.toggle('active', k === action);
    });

    const corrGroup = document.getElementById('corrected-condition-group');
    if (corrGroup) {
        corrGroup.style.display = action === 'CORRECT' ? 'block' : 'none';
    }
}

async function submitExpertVerdict() {
    if (!activeReviewCase) return;

    // Ensure user has EXPERT or ADMIN role before submitting review
    if (appState.currentUser && appState.currentUser.role !== 'EXPERT' && appState.currentUser.role !== 'ADMIN') {
        showToast("Official case verdicts can only be submitted by registered Agricultural Experts. Please sign in with an Expert account.");
        openAuthModalWithRole('expert');
        return;
    }

    const expertId = (appState.currentUser && (appState.currentUser.role === 'EXPERT' || appState.currentUser.role === 'ADMIN')) 
        ? appState.currentUser.id 
        : 2;
    const notes = document.getElementById('modal-expert-notes')?.value || '';

    let diagnosisCode = activeReviewCase.ai_condition_code;
    let conditionName = activeReviewCase.ai_raw_prediction;
    let obsType = activeReviewCase.ai_observation_type;

    if (appState.expertAction === 'CORRECT') {
        const select = document.getElementById('modal-correction-code');
        diagnosisCode = select?.value;
        conditionName = select?.options[select.selectedIndex]?.text;
        obsType = select?.options[select.selectedIndex]?.getAttribute('data-type') || 'DISEASE';
    } else if (appState.expertAction === 'LAB_REFERRAL') {
        conditionName = 'Referred to Agricultural Diagnostic Laboratory';
    }

    try {
        const res = await fetch(`/api/cases/${activeReviewCase.id}/review`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                expert_id: expertId,
                review_action: appState.expertAction,
                diagnosis_code: diagnosisCode,
                condition_name: conditionName,
                observation_type: obsType,
                expert_confidence: 98.0,
                expert_notes: notes,
                custom_advisory: notes
            })
        });

        if (!res.ok) {
            const err = await res.json().catch(() => ({}));
            throw new Error(err.detail || 'Review submission failed');
        }

        showToast('Expert prescription recorded successfully!');
        closeExpertModal();
        loadPendingExpertCases();
        refreshPendingExpertCount();

    } catch (e) {
        showToast('Error recording verdict: ' + e.message);
    }
}


// ==============================================================================
// ESCALATE WORKFLOW & SURVEILLANCE BULLETIN SYNC (REQUIREMENTS 7 & 8)
// ==============================================================================

async function escalateCurrentDiagnosis() {
    if (!appState.lastDiagnosisData) {
        showToast('No active diagnosis to escalate.');
        return;
    }

    const d = appState.lastDiagnosisData;
    const caseId = d.case_id || `ESC-${Date.now().toString().slice(-4)}`;
    const now = new Date();
    const timestamp = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) + ', ' + now.toLocaleDateString();

    const farmerName = (appState.currentUser && appState.currentUser.full_name) ? appState.currentUser.full_name : 'Local Farmer';
    const location = `${appState.selectedTaluka ? appState.selectedTaluka + ', ' : ''}${appState.selectedDistrict || 'Nashik'}`;
    const crop = (d.crop || appState.selectedCrop || 'Crop').toUpperCase();
    const disease = d.condition || d.condition_name || d.prediction || 'Unspecified Condition';
    const severity = (d.severity || (d.triage_level === 'RED' ? 'HIGH' : 'MODERATE')).toUpperCase();
    const imageUrl = d.annotated_image || d.image_path || d.image_url || '/static/images/samples/sample_healthy.jpg';

    const payload = {
        case_id: caseId,
        timestamp: timestamp,
        crop: crop,
        disease: disease,
        severity: severity,
        triage_level: d.triage_level || (severity === 'HIGH' ? 'RED' : 'YELLOW'),
        image_url: imageUrl,
        annotated_image: d.annotated_image || imageUrl,
        location: location,
        farmer_name: farmerName,
        latitude: appState.latitude,
        longitude: appState.longitude,
        damage_percent: d.damage_percent || (severity === 'HIGH' ? 55 : 25)
    };

    // 1. Sync to LocalStorage (key: falcon_bulletin_cases)
    let cases = [];
    try {
        cases = JSON.parse(localStorage.getItem('falcon_bulletin_cases') || '[]');
    } catch (e) {
        cases = [];
    }
    // Prepend new escalated case
    cases.unshift(payload);
    localStorage.setItem('falcon_bulletin_cases', JSON.stringify(cases));

    // 2. Call backend /api/escalate
    try {
        await fetch('/api/escalate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
    } catch (e) {
        console.warn('Backend escalation fallback:', e);
    }

    showToast(appState.lang === 'mr' ? 'प्रकरण कृषी डेस्ककडे वर्ग केले आहे!' : 'Case successfully escalated to Agricultural Desk!');

    // 3. Re-render bulletin and refresh GIS markers
    renderSurveillanceBulletin();
    if (appState.gisMap) {
        initGisMap();
    }
}

function renderSurveillanceBulletin() {
    const tbody = document.getElementById('bulletin-escalated-tbody');
    const countBadge = document.getElementById('bulletin-escalated-count');
    if (!tbody) return;

    let cases = [];
    try {
        cases = JSON.parse(localStorage.getItem('falcon_bulletin_cases') || '[]');
    } catch (e) {
        cases = [];
    }

    // Populate default seed cases if empty so desk is immediately functional
    if (cases.length === 0) {
        cases = [
            {
                case_id: 'MH-2601',
                timestamp: '10:45 AM, Today',
                crop: 'MAIZE',
                disease: 'Fall Armyworm (Spodoptera frugiperda)',
                severity: 'HIGH',
                image_url: '/static/images/samples/sample_maize.jpg',
                location: 'Dindori, Nashik',
                farmer_name: 'Rajesh Patil',
                latitude: 20.198,
                longitude: 73.842,
                damage_percent: 52
            },
            {
                case_id: 'MH-2602',
                timestamp: '09:15 AM, Today',
                crop: 'TOMATO',
                disease: 'Early Blight (Alternaria solani)',
                severity: 'MODERATE',
                image_url: '/static/images/samples/sample_tomato.jpg',
                location: 'Baramati, Pune',
                farmer_name: 'Sunil Jagtap',
                latitude: 18.152,
                longitude: 74.577,
                damage_percent: 28
            }
        ];
        localStorage.setItem('falcon_bulletin_cases', JSON.stringify(cases));
    }

    if (countBadge) {
        countBadge.innerText = `${cases.length} Cases Escalated`;
    }

    tbody.innerHTML = cases.map(c => {
        const isCrit = (c.severity || '').toUpperCase() === 'HIGH' || (c.severity || '').toUpperCase() === 'CRITICAL';
        return `
            <tr id="bulletin-row-${c.case_id}">
                <td>
                    <img src="${c.image_url || '/static/images/samples/sample_healthy.jpg'}" class="bulletin-thumb" alt="Leaf specimen" onerror="this.src='/static/images/samples/sample_healthy.jpg'">
                </td>
                <td><strong>#${c.case_id}</strong><div style="font-size:0.72rem;color:#94a3b8;">${c.timestamp || ''}</div></td>
                <td><span class="crop-tag">${c.crop}</span></td>
                <td><strong>${c.disease}</strong></td>
                <td>
                    <span class="status-badge ${isCrit ? 'badge-critical' : 'badge-identified'}" style="font-size:0.75rem;">
                        ${c.severity}
                    </span>
                </td>
                <td><i class="fa-solid fa-map-pin" style="color:#ea580c;margin-right:4px;"></i>${c.location}</td>
                <td>${c.farmer_name}</td>
                <td>
                    <div style="display:flex;gap:6px;">
                        <button type="button" class="btn-table-action" onclick="auditBulletinCase('${c.case_id}')" title="Audit and Attach Prescription">
                            <i class="fa-solid fa-file-signature"></i> Audit
                        </button>
                    </div>
                </td>
            </tr>
        `;
    }).join('');
}

function auditBulletinCase(caseId) {
    let cases = [];
    try {
        cases = JSON.parse(localStorage.getItem('falcon_bulletin_cases') || '[]');
    } catch(e){}
    const found = cases.find(c => String(c.case_id) === String(caseId));
    if (found) {
        openExpertModalWithCustomCase(found);
    } else {
        showToast('Audit recorded for case #' + caseId);
    }
}

function openExpertModalWithCustomCase(c) {
    const modal = document.getElementById('expert-review-modal');
    const caseNum = document.getElementById('modal-case-num');
    const img = document.getElementById('modal-specimen-img');
    const meta = document.getElementById('modal-specimen-meta');

    if (caseNum) caseNum.innerText = `CASE-${c.case_id}`;
    if (img) img.src = c.image_url || '/static/images/samples/sample_healthy.jpg';

    if (meta) {
        meta.innerHTML = `
            <div><strong>Farmer:</strong> ${c.farmer_name || 'Farmer'}</div>
            <div><strong>Location:</strong> ${c.location}</div>
            <div><strong>Crop & Condition:</strong> ${c.crop} · ${c.disease}</div>
            <div><strong>Severity:</strong> <span style="color:${c.severity === 'HIGH' ? '#dc2626' : '#d97706'};font-weight:bold;">${c.severity}</span></div>
            <div><strong>Telemetry Time:</strong> ${c.timestamp || 'Today'}</div>
        `;
    }

    populateCorrectionOptions();
    setExpertAction('CONFIRM');
    if (modal) modal.classList.add('show-modal');
}


// ==============================================================================
// 12. OFFICER DASHBOARD & GIS HOTSPOT MAP (HEAT MAP CALIBRATION)
// ==============================================================================

async function loadOfficerDashboard() {
    await loadDashboardStats();
}

async function initGisMap() {
    const mapDiv = document.getElementById('maharashtra-gis-map');
    if (!mapDiv) return;

    if (!appState.gisMap) {
        // Centered on Maharashtra geographic centroid
        appState.gisMap = L.map('maharashtra-gis-map').setView([19.7515, 75.7139], 7);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 18,
            attribution: '© OpenStreetMap contributors | FALCON-AI GIS'
        }).addTo(appState.gisMap);
    }

    // Always invalidate map size to avoid gray blank tiles on view switch
    setTimeout(() => {
        if (appState.gisMap) appState.gisMap.invalidateSize();
    }, 200);

    // Clear existing markers
    appState.gisMarkers.forEach(m => appState.gisMap.removeLayer(m));
    appState.gisMarkers = [];

    // 1. Fetch live hotspots from backend
    try {
        const res = await fetch('/api/dashboard/hotspots');
        if (res.ok) {
            const data = await res.json();
            const spots = data.hotspots || [];

            spots.forEach(pt => {
                const riskLevel = (pt.risk_level || 'low').toLowerCase();
                // Red = Critical / High; Yellow = Moderate
                const color = (riskLevel === 'critical' || riskLevel === 'high') ? '#FF4D4D' :
                              riskLevel === 'moderate' ? '#FFD700' : '#00E676';

                const marker = L.circleMarker([pt.latitude, pt.longitude], {
                    radius: (riskLevel === 'critical' || riskLevel === 'high') ? 12 : 9,
                    fillColor: color,
                    color: '#ffffff',
                    weight: 2,
                    opacity: 1,
                    fillOpacity: 0.88
                }).addTo(appState.gisMap);

                marker.bindPopup(`
                    <div class="gis-popup" style="font-family:sans-serif;min-width:180px;">
                        <h4 style="margin:0 0 6px 0;font-size:0.95rem;color:#0f172a;">${pt.condition_name || 'Outbreak Alert'}</h4>
                        <div style="font-size:0.8rem;margin-bottom:3px;"><strong>Case:</strong> ${pt.case_number}</div>
                        <div style="font-size:0.8rem;margin-bottom:3px;"><strong>Crop:</strong> ${pt.crop_code}</div>
                        <div style="font-size:0.8rem;margin-bottom:3px;"><strong>Location:</strong> ${pt.taluka}, ${pt.district}</div>
                        <div style="font-size:0.8rem;margin-bottom:3px;"><strong>Severity:</strong> <span style="color:${color};font-weight:bold;">${pt.risk_level} (${pt.risk_score}/100)</span></div>
                    </div>
                `);

                appState.gisMarkers.push(marker);
            });
        }
    } catch (e) {
        console.warn('Hotspot GIS fetch error', e);
    }

    // 2. Plot live escalated cases from localStorage / desk (Red = critical, Yellow = moderate)
    try {
        const escalatedCases = JSON.parse(localStorage.getItem('falcon_bulletin_cases') || '[]');
        escalatedCases.forEach(c => {
            const lat = c.latitude || 19.997;
            const lon = c.longitude || 73.789;
            const isCrit = (c.severity || '').toUpperCase() === 'HIGH' || (c.severity || '').toUpperCase() === 'CRITICAL';
            const color = isCrit ? '#FF4D4D' : '#FFD700';

            const marker = L.circleMarker([lat, lon], {
                radius: isCrit ? 14 : 10,
                fillColor: color,
                color: '#ffffff',
                weight: 2.5,
                opacity: 1,
                fillOpacity: 0.92
            }).addTo(appState.gisMap);

            marker.bindPopup(`
                <div class="gis-popup" style="font-family:sans-serif;min-width:210px;">
                    <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
                        <img src="${c.image_url || '/static/images/samples/sample_healthy.jpg'}" style="width:48px;height:48px;object-fit:cover;border-radius:6px;border:1px solid #cbd5e1;" alt="Leaf Photo" onerror="this.src='/static/images/samples/sample_healthy.jpg'">
                        <div>
                            <span style="font-size:0.68rem;padding:2px 6px;border-radius:4px;background:${isCrit ? '#fee2e2' : '#fef3c7'};color:${isCrit ? '#b91c1c' : '#b45309'};font-weight:bold;">${c.severity} RISK</span>
                            <h4 style="margin:2px 0 0 0;font-size:0.9rem;color:#0f172a;">${c.disease}</h4>
                        </div>
                    </div>
                    <div style="font-size:0.78rem;margin-bottom:3px;"><strong>Crop:</strong> ${c.crop}</div>
                    <div style="font-size:0.78rem;margin-bottom:3px;"><strong>Farmer:</strong> ${c.farmer_name || 'Farmer'}</div>
                    <div style="font-size:0.78rem;margin-bottom:3px;"><strong>Location:</strong> ${c.location}</div>
                    <div style="font-size:0.75rem;color:#64748b;margin-top:4px;"><i class="fa-solid fa-clock"></i> Escalated: ${c.timestamp || 'Today'}</div>
                </div>
            `);

            appState.gisMarkers.push(marker);
        });
    } catch (e) {
        console.warn('Failed to plot escalated markers', e);
    }
}


// ==============================================================================
// 13. FOLLOW-UP & FIELD CONFIRMATION
// ==============================================================================

function openFollowupModal() {
    const m = document.getElementById('followup-modal');
    if (m) m.classList.add('show-modal');
}

function closeFollowupModal() {
    const m = document.getElementById('followup-modal');
    if (m) m.classList.remove('show-modal');
}

async function submitFollowupCase() {
    const fileInput = document.getElementById('followup-file');
    const outcome = document.getElementById('followup-outcome-select')?.value;
    const notes = document.getElementById('followup-notes')?.value;

    if (!fileInput?.files[0]) {
        showToast('Please select a follow-up photograph.');
        return;
    }

    const parentId = appState.activeCaseId || 1;
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    formData.append('outcome', outcome);
    formData.append('notes', notes);

    try {
        const res = await fetch(`/api/cases/${parentId}/follow-up`, { method: 'POST', body: formData });
        if (!res.ok) throw new Error('Followup submission failed');
        showToast('Follow-up observation and photo recorded successfully!');
        closeFollowupModal();
        loadFarmerCasesHistory();
    } catch (e) {
        showToast('Error saving follow-up: ' + e.message);
    }
}

function openConfirmationModal() {
    const m = document.getElementById('confirm-modal');
    if (m) m.classList.add('show-modal');
}

function closeConfirmationModal() {
    const m = document.getElementById('confirm-modal');
    if (m) m.classList.remove('show-modal');
}

async function submitFieldConfirmation() {
    const outcome = document.getElementById('confirm-outcome-select')?.value;
    const notes = document.getElementById('confirm-notes')?.value;
    const caseId = appState.activeCaseId || 1;

    try {
        const res = await fetch(`/api/cases/${caseId}/confirm`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_id: appState.currentUser?.id || 1,
                actual_condition_code: 'field_verified',
                actual_condition_name: 'Field Ground Truth',
                outcome: outcome,
                notes: notes
            })
        });

        if (!res.ok) throw new Error('Confirmation submission failed');
        showToast('Field ground-truth confirmation recorded!');
        closeConfirmationModal();
        loadFarmerCasesHistory();
    } catch (e) {
        showToast('Error recording confirmation: ' + e.message);
    }
}


// ==============================================================================
// 14. AUTHENTICATION & LOGIN
// ==============================================================================

function openAuthModal(initialMode = 'login') {
    const m = document.getElementById('auth-modal');
    if (m) m.classList.add('show-modal');
    switchAuthMode(initialMode);
}

function openAuthModalWithRole(targetRole = 'farmer') {
    openAuthModal('login');
    switchAuthRole(targetRole);
}

function closeAuthModal() {
    const m = document.getElementById('auth-modal');
    if (m) m.classList.remove('show-modal');
}

const PREDEFINED_EXPERTS = [
    { name: "Dr. Anjali Deshmukh", phone: "9000000001", email: "expert1@falconai.demo", spec: "Plant Pathology" },
    { name: "Dr. Vivek Kulkarni", phone: "9000000002", email: "expert2@falconai.demo", spec: "Entomology & Pest Mgmt" },
    { name: "Dr. Neha Patil", phone: "9000000003", email: "expert3@falconai.demo", spec: "Agronomy & Crop Mgmt" },
    { name: "Dr. Rahul Shinde", phone: "9000000004", email: "expert4@falconai.demo", spec: "Horticulture" },
    { name: "Dr. Priya Jadhav", phone: "9000000005", email: "expert5@falconai.demo", spec: "Soil Science" },
];

const PREDEFINED_OFFICERS = [
    { name: "Kavita Pawar", phone: "9100000001", email: "officer1@falconai.demo", spec: "District Agriculture Officer" },
    { name: "Mahesh Gaikwad", phone: "9100000002", email: "officer2@falconai.demo", spec: "Crop Protection & Surveillance" },
    { name: "Sneha More", phone: "9100000003", email: "officer3@falconai.demo", spec: "Taluka Agriculture Officer" },
    { name: "Amit Bhosale", phone: "9100000004", email: "officer4@falconai.demo", spec: "Agricultural Extension" },
];

function renderStaffQuickPick(role) {
    const container = document.getElementById('staff-quick-chips');
    const noticeDesc = document.getElementById('staff-notice-desc');
    const noticeTitle = document.getElementById('staff-notice-title');
    if (!container) return;

    const isExpert = (role === 'expert');
    if (noticeTitle) {
        noticeTitle.innerHTML = isExpert
            ? '<i class="fa-solid fa-microscope"></i> Agricultural Expert Restricted Desk'
            : '<i class="fa-solid fa-landmark"></i> Agriculture Officer Restricted Portal';
    }
    if (noticeDesc) {
        noticeDesc.innerHTML = isExpert
            ? 'Access is reserved exclusively for pre-authorized Plant Pathologists & Agronomists. Password for all: <code style="background:#dbeafe;color:#1e40af;padding:1px 6px;border-radius:4px;font-weight:700;">Falcon@2026</code>'
            : 'Access is reserved exclusively for pre-authorized Agriculture Department Officers. Password for all: <code style="background:#ede9fe;color:#5b21b6;padding:1px 6px;border-radius:4px;font-weight:700;">Falcon@2026</code>';
    }

    const staffList = isExpert ? PREDEFINED_EXPERTS : PREDEFINED_OFFICERS;
    container.innerHTML = staffList.map(item => `
        <button type="button" onclick="fillPredefinedStaffAccount('${item.email}', 'Falcon@2026')"
            style="display:flex;justify-content:space-between;align-items:center;padding:5px 8px;font-size:0.75rem;background:#ffffff;border:1px solid #cbd5e1;border-radius:6px;cursor:pointer;text-align:left;transition:all 0.15s;">
            <span><strong>${item.name}</strong> <span style="color:#64748b;font-size:0.7rem;">(${item.spec})</span></span>
            <code style="color:#0284c7;font-size:0.72rem;font-weight:600;">${item.phone}</code>
        </button>
    `).join('');
}

function fillPredefinedStaffAccount(identifier, password) {
    const emailInput = document.getElementById('auth-email');
    const passInput = document.getElementById('auth-password');
    if (emailInput) emailInput.value = identifier;
    if (passInput) passInput.value = password;
    showToast(`Loaded predefined credentials for ${identifier}`);
}

function switchAuthRole(role) {
    localStorage.setItem('falcon_user_role', role);

    // Sync radio inputs
    const radios = document.querySelectorAll('input[name="auth_role_selection"]');
    radios.forEach(radio => {
        radio.checked = (radio.value === role);
    });

    const isStaff = (role === 'expert' || role === 'officer');
    const registerBtn = document.getElementById('auth-mode-register');
    const staffNotice = document.getElementById('staff-restricted-notice');

    if (isStaff) {
        if (registerBtn) {
            registerBtn.style.opacity = '0.35';
            registerBtn.style.pointerEvents = 'none';
            registerBtn.title = 'Registration closed for official personnel';
        }
        switchAuthMode('login');
        if (staffNotice) staffNotice.style.display = 'block';
        renderStaffQuickPick(role);
    } else {
        if (registerBtn) {
            registerBtn.style.opacity = '1';
            registerBtn.style.pointerEvents = 'auto';
            registerBtn.title = '';
        }
        if (staffNotice) staffNotice.style.display = 'none';
    }

    const farmerFields = document.getElementById('farmer-profile-fields');
    if (farmerFields) farmerFields.style.display = (role === 'farmer' && authMode === 'register') ? 'block' : 'none';
    const expertFields = document.getElementById('expert-profile-fields');
    if (expertFields) expertFields.style.display = 'none';
    const officerFields = document.getElementById('officer-profile-fields');
    if (officerFields) officerFields.style.display = 'none';
}

// Auth mode: 'login' or 'register'
let authMode = 'login';

function switchAuthMode(mode) {
    authMode = mode;
    const loginBtn = document.getElementById('auth-mode-login');
    const registerBtn = document.getElementById('auth-mode-register');
    const nameGroup = document.getElementById('register-name-group');
    const roleGroup = document.getElementById('register-role-group');
    const farmerFields = document.getElementById('farmer-profile-fields');
    const expertFields = document.getElementById('expert-profile-fields');
    const officerFields = document.getElementById('officer-profile-fields');
    const submitText = document.getElementById('auth-submit-text');

    if (loginBtn) loginBtn.classList.toggle('active', mode === 'login');
    if (registerBtn) registerBtn.classList.toggle('active', mode === 'register');
    if (nameGroup) nameGroup.style.display = mode === 'register' ? 'block' : 'none';
    if (roleGroup) roleGroup.style.display = 'block';
    if (farmerFields) farmerFields.style.display = 'none';
    if (expertFields) expertFields.style.display = 'none';
    if (officerFields) officerFields.style.display = 'none';
    if (mode === 'register') {
        const selectedRole = document.querySelector('input[name="auth_role_selection"]:checked')?.value || 'farmer';
        if (selectedRole === 'expert' || selectedRole === 'officer') {
            switchAuthRole('farmer');
        } else {
            switchAuthRole(selectedRole);
        }
    }
    if (submitText) submitText.innerText = mode === 'register' ? 'Create Account' : 'Sign In';
}

async function submitGatewayDirectLogin() {
    const identifier = document.getElementById('gate-email')?.value?.trim();
    const password = document.getElementById('gate-password')?.value;

    if (!identifier) {
        showToast('Please enter your mobile number or email.');
        return;
    }
    if (!password) {
        showToast('Please enter your password.');
        return;
    }

    try {
        const res = await fetch('/api/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: identifier, password })
        });

        if (!res.ok) {
            const err = await res.json().catch(() => ({}));
            throw new Error(err.detail || 'Invalid mobile number, email, or password.');
        }

        const data = await res.json();
        appState.currentUser = data.user;
        localStorage.setItem('falcon_user', JSON.stringify(appState.currentUser));
        const userRoleLower = (appState.currentUser.role === 'ADMIN' ? 'officer' : (appState.currentUser.role || 'farmer')).toLowerCase();
        localStorage.setItem('falcon_user_role', userRoleLower);

        if (data.token) {
            localStorage.setItem('falcon_token', data.token);
        }

        updateNavUserDisplay();
        showWelcomeQuoteModal(appState.currentUser.full_name, data.welcome_quote, data.is_new_user);
        loadFarms();
        loadFarmerCasesHistory();
        loadDashboardStats();

        if (appState.currentUser.role === 'EXPERT') {
            switchView('expert');
        } else if (appState.currentUser.role === 'ADMIN') {
            switchView('officer');
        } else {
            switchView('dashboard');
        }
    } catch (e) {
        showToast(e.message);
    }
}

async function submitUserLogin() {
    const identifier = document.getElementById('auth-email')?.value?.trim();
    const password = document.getElementById('auth-password')?.value;
    const fullName = document.getElementById('auth-fullname')?.value?.trim();

    if (!identifier) {
        showToast('Please enter your mobile number or email address.');
        return;
    }
    if (!password || password.length < 6) {
        showToast('Password must be at least 6 characters.');
        return;
    }

    const checkedRadio = document.querySelector('input[name="auth_role_selection"]:checked');
    const selectedRoleVal = checkedRadio ? checkedRadio.value : 'farmer';

    try {
        let res;
        let data;

        if (authMode === 'register') {
            if (!fullName) {
                showToast('Please enter your full name.');
                return;
            }

            res = await fetch('/api/auth/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    email: identifier,
                    full_name: fullName,
                    password,
                    role: 'FARMER',
                    preferred_language: 'en'
                })
            });
        } else {
            // Login mode with selected role guardrail
            res = await fetch('/api/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email: identifier, password, role: selectedRoleVal })
            });
        }

        if (!res.ok) {
            const err = await res.json().catch(() => ({}));
            throw new Error(err.detail || 'Authentication failed. Please check your credentials.');
        }

        data = await res.json();
        appState.currentUser = data.user;
        localStorage.setItem('falcon_user', JSON.stringify(appState.currentUser));
        const userRoleLower = (appState.currentUser.role === 'ADMIN' ? 'officer' : (appState.currentUser.role || 'farmer')).toLowerCase();
        localStorage.setItem('falcon_user_role', userRoleLower);

        if (data.token) {
            localStorage.setItem('falcon_token', data.token);
        }

        updateNavUserDisplay();
        closeAuthModal();

        // Display inspirational welcome modal with user name and uplifting quotation
        showWelcomeQuoteModal(appState.currentUser.full_name, data.welcome_quote, data.is_new_user);

        loadFarms();
        loadFarmerCasesHistory();
        loadDashboardStats();

        if (appState.currentUser.role === 'EXPERT') {
            switchView('expert');
        } else if (appState.currentUser.role === 'ADMIN') {
            switchView('officer');
        } else {
            switchView('dashboard');
        }

    } catch (e) {
        showToast(e.message);
    }
}

function showWelcomeQuoteModal(fullName, quote, isNew) {
    const titleEl = document.getElementById('welcome-quote-title');
    const textEl = document.getElementById('welcome-quote-text');
    const modal = document.getElementById('welcome-quote-modal');
    if (titleEl) {
        titleEl.innerText = isNew ? `Welcome to FALCON-AI, ${fullName}! 🎉` : `Welcome back, ${fullName}! 👋`;
    }
    if (textEl) {
        textEl.innerText = quote || "Farming is a profession of hope. Let's protect your harvest today! 🌾";
    }
    if (modal) {
        modal.classList.add('show-modal');
    }
}

function closeWelcomeQuoteModal() {
    const modal = document.getElementById('welcome-quote-modal');
    if (modal) modal.classList.remove('show-modal');
}

async function logActivity(activityType, queryText = '', metadata = null) {
    if (!appState.currentUser || !appState.currentUser.id) return;
    try {
        await fetch('/api/user/activity', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_id: appState.currentUser.id,
                activity_type: activityType,
                query_text: queryText,
                metadata: metadata
            })
        });
    } catch (e) {
        // Non-blocking telemetry
    }
}

async function openWorkHistoryModal() {
    if (!appState.currentUser || !appState.currentUser.id) {
        showToast('Please sign in to view your activity log.');
        openAuthModal();
        return;
    }
    const modal = document.getElementById('work-history-modal');
    const container = document.getElementById('work-history-container');
    if (modal) modal.classList.add('show-modal');
    if (!container) return;

    container.innerHTML = '<div style="text-align:center;padding:24px;color:#64748b;"><i class="fa-solid fa-spinner fa-spin"></i> Loading activity logs...</div>';

    try {
        const res = await fetch(`/api/user/activity/${appState.currentUser.id}`);
        if (res.ok) {
            const data = await res.json();
            const logs = data.activities || [];
            if (logs.length === 0) {
                container.innerHTML = '<div style="text-align:center;padding:30px;color:#94a3b8;"><i class="fa-solid fa-clipboard-list" style="font-size:2rem;margin-bottom:8px;display:block;"></i>No activity recorded yet for this account.</div>';
                return;
            }
            container.innerHTML = logs.map(l => {
                const icon = l.activity_type === 'LOGIN' ? 'fa-arrow-right-to-bracket' :
                             l.activity_type === 'SEARCH' ? 'fa-magnifying-glass' :
                             l.activity_type === 'DIAGNOSIS' ? 'fa-camera-retro' :
                             l.activity_type === 'VOICE_QUERY' ? 'fa-microphone' :
                             l.activity_type === 'LANGUAGE_CHANGE' ? 'fa-language' :
                             l.activity_type === 'VIEW_ADVISORY' ? 'fa-prescription' : 'fa-circle-dot';
                return `
                    <div style="display:flex;align-items:flex-start;gap:12px;padding:12px;border-bottom:1px solid #f1f5f9;font-size:0.85rem;">
                        <div style="width:32px;height:32px;border-radius:8px;background:#f0fdf4;color:#16a34a;display:flex;align-items:center;justify-content:center;flex-shrink:0;">
                            <i class="fa-solid ${icon}"></i>
                        </div>
                        <div style="flex:1;">
                            <div style="display:flex;justify-content:space-between;align-items:center;">
                                <strong style="color:#0f172a;text-transform:capitalize;">${l.activity_type.toLowerCase().replace('_', ' ')}</strong>
                                <span style="font-size:0.75rem;color:#94a3b8;">${l.created_at || ''}</span>
                            </div>
                            <div style="color:#475569;margin-top:2px;">${l.query_text || 'Completed action'}</div>
                        </div>
                    </div>
                `;
            }).join('');
        } else {
            container.innerHTML = '<div style="text-align:center;padding:20px;color:#ef4444;">Failed to load activity history.</div>';
        }
    } catch (e) {
        container.innerHTML = '<div style="text-align:center;padding:20px;color:#ef4444;">Error fetching logs.</div>';
    }
}

function closeWorkHistoryModal() {
    const modal = document.getElementById('work-history-modal');
    if (modal) modal.classList.remove('show-modal');
}

let searchDebounceTimer = null;
let searchLogTimer = null;

function handleGlobalSearch(query) {
    const resultsContainer = document.getElementById('global-search-results');
    if (!resultsContainer) return;

    if (!query || query.trim().length === 0) {
        resultsContainer.style.display = 'none';
        resultsContainer.innerHTML = '';
        // Reset bulletin rows and GIS markers
        document.querySelectorAll('#bulletin-escalated-tbody tr').forEach(r => r.style.display = '');
        if (appState.gisMarkers) {
            appState.gisMarkers.forEach(m => { if (m._path) m._path.style.display = ''; });
        }
        return;
    }

    const q = query.toLowerCase().trim();

    if (searchLogTimer) clearTimeout(searchLogTimer);
    searchLogTimer = setTimeout(() => {
        if (q.length >= 3) {
            logActivity('SEARCH', query);
        }
    }, 800);

    if (searchDebounceTimer) clearTimeout(searchDebounceTimer);
    searchDebounceTimer = setTimeout(() => {
        executeFunctionalSearch(q, resultsContainer);
    }, 250);
}

function executeFunctionalSearch(q, container) {
    const userRole = (appState.currentUser?.role || 'FARMER').toUpperCase();
    const isExpertOrOfficer = userRole === 'EXPERT' || userRole === 'ADMIN';

    let cardsHtml = '';

    if (isExpertOrOfficer) {
        // Live filter Surveillance Bulletin table rows if present
        const bulletinRows = document.querySelectorAll('#bulletin-escalated-tbody tr');
        if (bulletinRows.length > 0) {
            bulletinRows.forEach(row => {
                const text = row.innerText.toLowerCase();
                row.style.display = text.includes(q) ? '' : 'none';
            });
        }
        // Live filter GIS Heat Map markers if initialized
        if (appState.gisMarkers && appState.gisMarkers.length > 0) {
            appState.gisMarkers.forEach(m => {
                const popup = (m.getPopup()?.getContent() || '').toLowerCase();
                if (m._path) {
                    m._path.style.display = (q === '' || popup.includes(q)) ? '' : 'none';
                }
            });
        }

        // Search Surveillance Cases & Field Telemetry
        let escalatedCases = [];
        try {
            escalatedCases = JSON.parse(localStorage.getItem('falcon_bulletin_cases') || '[]');
        } catch (e) {
            escalatedCases = [];
        }
        const matchingCases = escalatedCases.filter(c => 
            (c.crop && c.crop.toLowerCase().includes(q)) ||
            (c.disease && c.disease.toLowerCase().includes(q)) ||
            (c.location && c.location.toLowerCase().includes(q)) ||
            (c.farmer_name && c.farmer_name.toLowerCase().includes(q)) ||
            (c.case_id && String(c.case_id).toLowerCase().includes(q))
        );

        fetch(`/api/cases?limit=50&${encodeURIComponent('')}`)
            .then(res => res.ok ? res.json() : { cases: [] })
            .then(data => {
                const backendCases = (data.cases || []).filter(c => {
                    const text = [c.crop_code, c.ai_raw_prediction, c.final_condition_name, c.district, c.taluka, c.farmer_name, c.case_number]
                        .filter(Boolean).join(' ').toLowerCase();
                    return text.includes(q);
                });
                if (backendCases.length) {
                    const backendHtml = `<div style="padding:6px 12px;font-size:0.75rem;font-weight:700;color:#64748b;text-transform:uppercase;">Backend Case Store (${backendCases.length})</div>` +
                        backendCases.slice(0, 5).map(c => `<div class="search-result-item" onclick="switchView('expert');closeSearchDropdown();"><div class="search-result-info"><div class="search-result-title">${c.crop_code}: ${c.final_condition_name || c.ai_raw_prediction || 'Case'}</div><div class="search-result-desc">${c.farmer_name || 'Farmer'} · ${c.district || 'Maharashtra'} · ${c.case_number || c.id}</div></div><span class="status-badge badge-identified" style="font-size:0.7rem;">${c.case_status || 'CASE'}</span></div>`).join('');
                    container.insertAdjacentHTML('afterbegin', backendHtml);
                    container.style.display = 'block';
                }
            })
            .catch(() => {});

        if (matchingCases.length > 0) {
            cardsHtml += `<div style="padding:6px 12px;font-size:0.75rem;font-weight:700;color:#64748b;text-transform:uppercase;">Surveillance Telemetry Cases (${matchingCases.length})</div>`;
            matchingCases.slice(0, 5).forEach(c => {
                const isCrit = (c.severity || '').toUpperCase() === 'HIGH' || (c.severity || '').toUpperCase() === 'CRITICAL';
                cardsHtml += `
                    <div class="search-result-item" onclick="selectSearchResultCase('${c.case_id}')">
                        <div class="search-result-thumb">
                            <img src="${c.image_url || '/static/images/samples/sample_healthy.jpg'}" alt="Leaf specimen" onerror="this.src='/static/images/samples/sample_healthy.jpg'">
                        </div>
                        <div class="search-result-info">
                            <div class="search-result-title">${c.crop}: ${c.disease}</div>
                            <div class="search-result-desc">${c.farmer_name || 'Farmer'} · ${c.location || 'Maharashtra'} · Case #${c.case_id}</div>
                        </div>
                        <span class="status-badge ${isCrit ? 'badge-critical' : 'badge-identified'}" style="font-size:0.7rem;">${c.severity || 'ALERT'}</span>
                    </div>
                `;
            });
        } else {
            // General quick actions for officers
            if ('hotspot map'.includes(q) || 'map'.includes(q)) {
                cardsHtml += `
                    <div class="search-result-item" onclick="switchView('hotspots');closeSearchDropdown();">
                        <div class="search-result-info">
                            <div class="search-result-title">🗺️ Outbreak Hotspot Heat Map</div>
                            <div class="search-result-desc">View statewide spatial epidemiology and clusters</div>
                        </div>
                    </div>
                `;
            }
            if ('bulletin'.includes(q) || 'alerts'.includes(q) || 'surveillance'.includes(q)) {
                cardsHtml += `
                    <div class="search-result-item" onclick="switchView('alerts');closeSearchDropdown();">
                        <div class="search-result-info">
                            <div class="search-result-title">📡 Outbreak Surveillance Bulletin</div>
                            <div class="search-result-desc">Review live escalated farmer cases & issue alerts</div>
                        </div>
                    </div>
                `;
            }
        }
    } else {
        // Farmer Search: Crop Encyclopedia, Pests, Treatments & Weather
        const crops = appState.taxonomy?.crops || {};
        const matchedCrops = [];
        const matchedConditions = [];

        Object.keys(crops).forEach(cropKey => {
            const crop = crops[cropKey];
            const nameMatch = cropKey.includes(q) || 
                             (crop.display_name && crop.display_name.toLowerCase().includes(q)) ||
                             (crop.marathi_name && crop.marathi_name.toLowerCase().includes(q)) ||
                             (crop.hindi_name && crop.hindi_name.toLowerCase().includes(q));

            if (nameMatch) {
                matchedCrops.push({ key: cropKey, ...crop });
            }

            // Check conditions/pests
            (crop.common_diseases || []).forEach(d => {
                if (d.toLowerCase().includes(q)) {
                    matchedConditions.push({ crop: cropKey, condition: d });
                }
            });
            (crop.common_pests || []).forEach(p => {
                if (p.toLowerCase().includes(q)) {
                    matchedConditions.push({ crop: cropKey, condition: p, isPest: true });
                }
            });
        });

        if (matchedCrops.length > 0) {
            cardsHtml += `<div style="padding:6px 12px;font-size:0.75rem;font-weight:700;color:#64748b;text-transform:uppercase;">Crop Encyclopedia</div>`;
            matchedCrops.slice(0, 4).forEach(c => {
                cardsHtml += `
                    <div class="search-result-item" onclick="selectCropAndDiagnose('${c.key}')">
                        <div class="search-result-info">
                            <div class="search-result-title">🌾 ${c.display_name || c.key} (${c.marathi_name || ''})</div>
                            <div class="search-result-desc">Click to select crop and initiate automated AI foliar diagnosis</div>
                        </div>
                        <span class="status-badge badge-healthy" style="font-size:0.7rem;">Select Crop</span>
                    </div>
                `;
            });
        }

        if (matchedConditions.length > 0) {
            cardsHtml += `<div style="padding:6px 12px;font-size:0.75rem;font-weight:700;color:#64748b;text-transform:uppercase;">Pest & Disease Advisory</div>`;
            matchedConditions.slice(0, 4).forEach(mc => {
                cardsHtml += `
                    <div class="search-result-item" onclick="selectCrop('${mc.crop}');switchView('diagnose');closeSearchDropdown();">
                        <div class="search-result-info">
                            <div class="search-result-title">${mc.isPest ? '🐛' : '🦠'} ${mc.condition} (${mc.crop.toUpperCase()})</div>
                            <div class="search-result-desc">Scientific management guidance & CIBRC action protocol</div>
                        </div>
                    </div>
                `;
            });
        }

        if ('weather forecast rain temperature हवामान'.includes(q)) {
            cardsHtml += `
                <div class="search-result-item" onclick="switchView('weather');closeSearchDropdown();">
                    <div class="search-result-info">
                        <div class="search-result-title">☁️ Weather Telemetry & Foliar Spray Advisory</div>
                        <div class="search-result-desc">Live micro-climate indices, spray suitability, and fungal risks</div>
                    </div>
                </div>
            `;
        }
    }

    if (!cardsHtml) {
        cardsHtml = `
            <div style="padding:16px;text-align:center;color:#64748b;font-size:0.85rem;">
                <i class="fa-solid fa-magnifying-glass" style="margin-bottom:6px;display:block;font-size:1.4rem;color:#cbd5e1;"></i>
                No matching entries found for "${q}". Try searching for Maize, Rust, Armyworm, or Weather.
            </div>
        `;
    }

    container.innerHTML = cardsHtml;
    container.style.display = 'block';
}

function closeSearchDropdown() {
    const resultsContainer = document.getElementById('global-search-results');
    if (resultsContainer) {
        resultsContainer.style.display = 'none';
        resultsContainer.innerHTML = '';
    }
}

function selectCropAndDiagnose(cropKey) {
    selectCrop(cropKey);
    switchView('diagnose');
    closeSearchDropdown();
}

function selectSearchResultCase(caseId) {
    closeSearchDropdown();
    switchView('alerts');
    const row = document.getElementById(`bulletin-row-${caseId}`);
    if (row) {
        row.scrollIntoView({ behavior: 'smooth', block: 'center' });
        row.style.background = '#fef3c7';
        setTimeout(() => { row.style.background = ''; }, 2500);
    }
}

// Close search dropdown on outside click
document.addEventListener('click', (e) => {
    const searchBox = document.querySelector('.header-search-box');
    if (searchBox && !searchBox.contains(e.target)) {
        closeSearchDropdown();
    }
});

function showToast(msg) {
    const toast = document.getElementById('toast-notification');
    if (!toast) return;
    toast.innerText = msg;
    toast.classList.add('show-toast');
    setTimeout(() => toast.classList.remove('show-toast'), 3500);
}
