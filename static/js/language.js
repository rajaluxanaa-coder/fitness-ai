// Central Language Management - Auto Translation
let currentLang = localStorage.getItem('language') || 'en';
let translations = {};

// Translation dictionary for common phrases
const fallbackTranslations = {
    en: {},
    hi: {
        "Dashboard": "डैशबोर्ड",
        "Profile": "प्रोफाइल",
        "Analytics": "विश्लेषण",
        "Achievements": "उपलब्धियाँ",
        "Community": "समुदाय",
        "Goals": "लक्ष्य",
        "Calendar": "कैलेंडर",
        "Music": "संगीत",
        "Videos": "वीडियो",
        "Settings": "सेटिंग्स",
        "Logout": "लॉगआउट",
        "Current Weight": "वर्तमान वजन",
        "Workouts Done": "किए गए वर्कआउट",
        "Calories Burned": "जली हुई कैलोरी",
        "Minutes": "मिनट",
        "Generate New Workout Plan": "नया वर्कआउट प्लान बनाएं",
        "Your Progress": "आपकी प्रगति",
        "Goal Progress": "लक्ष्य प्रगति",
        "Start Weight": "शुरुआती वजन",
        "Goal Weight": "लक्ष्य वजन",
        "Update Progress": "प्रगति अपडेट करें",
        "Today's Fitness Tip": "आज की फिटनेस टिप",
        "Your BMI": "आपका बीएमआई",
        "Height": "ऊंचाई",
        "Weight": "वजन",
        "Underweight": "कम वजन",
        "Normal Weight": "सामान्य वजन",
        "Overweight": "अधिक वजन",
        "Obese": "मोटापा",
        "Water Intake": "पानी का सेवन",
        "Nutrition Tips": "पोषण टिप्स",
        "Current Streak": "वर्तमान स्ट्रीक",
        "Best Streak": "सर्वश्रेष्ठ स्ट्रीक",
        "Dark Mode": "डार्क मोड",
        "Light Mode": "लाइट मोड",
        "Notifications": "सूचनाएं",
        "Save Settings": "सेटिंग्स सहेजें",
        "Log Workout": "वर्कआउट लॉग करें",
        "Log Meal": "भोजन लॉग करें",
        "View Progress": "प्रगति देखें",
        "Back to Dashboard": "डैशबोर्ड पर वापस जाएं",
        "Create Account": "खाता बनाएं",
        "Sign In": "साइन इन करें",
        "Sign Up": "साइन अप करें",
        "Email": "ईमेल",
        "Password": "पासवर्ड",
        "Forgot Password": "पासवर्ड भूल गए",
        "Send OTP": "ओटीपी भेजें",
        "Verify OTP": "ओटीपी सत्यापित करें",
        "Resend OTP": "ओटीपी पुनः भेजें"
    },
    ta: {
        "Dashboard": "டாஷ்போர்டு",
        "Profile": "சுயவிவரம்",
        "Analytics": "பகுப்பாய்வு",
        "Achievements": "சாதனைகள்",
        "Community": "சமூகம்",
        "Goals": "இலக்குகள்",
        "Calendar": "நாட்காட்டி",
        "Music": "இசை",
        "Videos": "வீடியோக்கள்",
        "Settings": "அமைப்புகள்",
        "Logout": "வெளியேறு",
        "Current Weight": "தற்போதைய எடை",
        "Workouts Done": "முடிக்கப்பட்ட பயிற்சிகள்",
        "Calories Burned": "எரிந்த கலோரிகள்",
        "Minutes": "நிமிடங்கள்",
        "Generate New Workout Plan": "புதிய பயிற்சி திட்டத்தை உருவாக்கு",
        "Your Progress": "உங்கள் முன்னேற்றம்",
        "Goal Progress": "இலக்கு முன்னேற்றம்",
        "Start Weight": "தொடக்க எடை",
        "Goal Weight": "இலக்கு எடை",
        "Update Progress": "முன்னேற்றத்தை புதுப்பிக்கவும்",
        "Today's Fitness Tip": "இன்றைய உடற்பயிற்சி குறிப்பு",
        "Your BMI": "உங்கள் பிஎம்ஐ",
        "Height": "உயரம்",
        "Weight": "எடை",
        "Underweight": "குறைந்த எடை",
        "Normal Weight": "சாதாரண எடை",
        "Overweight": "அதிக எடை",
        "Obese": "உடல் பருமன்",
        "Water Intake": "நீர் உட்கொள்ளல்",
        "Nutrition Tips": "ஊட்டச்சத்து குறிப்புகள்",
        "Current Streak": "தற்போதைய தொடர்",
        "Best Streak": "சிறந்த தொடர்",
        "Dark Mode": "இருண்ட முறை",
        "Light Mode": "ஒளி முறை",
        "Notifications": "அறிவிப்புகள்",
        "Save Settings": "அமைப்புகளை சேமிக்கவும்",
        "Log Workout": "பயிற்சியை பதிவு செய்யவும்",
        "Log Meal": "உணவை பதிவு செய்யவும்",
        "View Progress": "முன்னேற்றத்தை காண்க",
        "Back to Dashboard": "டாஷ்போர்டுக்கு திரும்பு",
        "Create Account": "கணக்கை உருவாக்கு",
        "Sign In": "உள்நுழைக",
        "Sign Up": "பதிவு செய்க",
        "Email": "மின்னஞ்சல்",
        "Password": "கடவுச்சொல்",
        "Forgot Password": "கடவுச்சொல் மறந்துவிட்டீர்களா",
        "Send OTP": "ஓடிபி அனுப்பு",
        "Verify OTP": "ஓடிபியை சரிபார்க்கவும்",
        "Resend OTP": "ஓடிபியை மீண்டும் அனுப்பு"
    }
};

// Load translations from JSON file (or use fallback)
async function loadTranslations(lang) {
    try {
        const response = await fetch(`/static/lang/${lang}.json`);
        translations = await response.json();
    } catch (error) {
        console.log('Using fallback translations');
        translations = fallbackTranslations[lang] || {};
    }
    applyTranslations();
    localStorage.setItem('language', lang);
    currentLang = lang;
    updateActiveLanguageButton();
}

// Apply translations to all text on the page
function applyTranslations() {
    // Translate all elements that contain text
    const elementsToTranslate = document.querySelectorAll('h1, h2, h3, h4, h5, h6, p, span, button, a, label, div');
    
    elementsToTranslate.forEach(element => {
        // Skip elements that already have translation or are empty
        if (element.hasAttribute('data-translated')) return;
        if (!element.innerText || element.innerText.trim() === '') return;
        
        const originalText = element.innerText.trim();
        
        // Check if this exact text needs translation
        if (translations[originalText]) {
            element.innerText = translations[originalText];
            element.setAttribute('data-translated', 'true');
        }
    });
    
    // Also translate placeholder text
    document.querySelectorAll('input, textarea').forEach(input => {
        if (input.placeholder && translations[input.placeholder]) {
            input.placeholder = translations[input.placeholder];
        }
    });
    
    // Update document title
    if (translations['FitAI']) {
        document.title = translations['FitAI'];
    }
}

// Change language (called from settings)
function changeLanguage(lang) {
    loadTranslations(lang);
}

// Update active button in settings panel
function updateActiveLanguageButton() {
    const langEn = document.getElementById('langEn');
    const langHi = document.getElementById('langHi');
    const langTa = document.getElementById('langTa');
    
    if (langEn) {
        langEn.classList.remove('active');
        langHi.classList.remove('active');
        langTa.classList.remove('active');
        
        if (currentLang === 'en') langEn.classList.add('active');
        if (currentLang === 'hi') langHi.classList.add('active');
        if (currentLang === 'ta') langTa.classList.add('active');
    }
}

// Observer to translate dynamically added content
const observer = new MutationObserver(() => {
    if (currentLang !== 'en') {
        applyTranslations();
    }
});
observer.observe(document.body, { childList: true, subtree: true });

// Load language on page load
document.addEventListener('DOMContentLoaded', () => {
    loadTranslations(currentLang);
});