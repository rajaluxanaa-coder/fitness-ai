// Auto Language Translation - No data-i18n needed!
let currentLang = localStorage.getItem('language') || 'en';
let translations = {};

// Common words to translate (add more as needed)
const commonWords = {
    'en': {},
    'hi': {
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
        "Update Progress": "प्रगति अपडेट करें",
        "Goal Progress": "लक्ष्य प्रगति",
        "Start Weight": "शुरुआती वजन",
        "Goal Weight": "लक्ष्य वजन",
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
        "Log Workout": "वर्कआउट लॉग करें",
        "Log Meal": "भोजन लॉग करें",
        "View Progress": "प्रगति देखें",
        "Recent Workouts": "हाल के वर्कआउट",
        "Recent Meals": "हाल के भोजन",
        "Recommended Meals": "अनुशंसित भोजन",
        "Quick Tips": "त्वरित सुझाव",
        "Save All Settings": "सभी सेटिंग्स सहेजें",
        "Dark Mode": "डार्क मोड",
        "Light Mode": "लाइट मोड",
        "Notifications": "सूचनाएं",
        "Enable Notifications": "सूचनाएं सक्षम करें",
        "Workout Reminder": "वर्कआउट रिमाइंडर",
        "Meal Reminder": "भोजन रिमाइंडर",
        "Daily Calorie Goal": "दैनिक कैलोरी लक्ष्य",
        "Daily Water Goal": "दैनिक पानी लक्ष्य",
        "Profile Visibility": "प्रोफाइल दृश्यता",
        "Public": "सार्वजनिक",
        "Friends Only": "केवल मित्र",
        "Private": "निजी",
        "Challenges": "चुनौतियाँ",
        "Leaderboard": "लीडरबोर्ड",
        "Find Friends": "मित्र खोजें",
        "Friend Requests": "मित्र अनुरोध",
        "My Friends": "मेरे मित्र",
        "Activity Feed": "गतिविधि फीड"
    },
    'ta': {
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
        "Update Progress": "முன்னேற்றத்தை புதுப்பிக்கவும்",
        "Goal Progress": "இலக்கு முன்னேற்றம்",
        "Start Weight": "தொடக்க எடை",
        "Goal Weight": "இலக்கு எடை",
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
        "Log Workout": "பயிற்சியை பதிவு செய்யவும்",
        "Log Meal": "உணவை பதிவு செய்யவும்",
        "View Progress": "முன்னேற்றத்தை காண்க",
        "Recent Workouts": "சமீபத்திய பயிற்சிகள்",
        "Recent Meals": "சமீபத்திய உணவுகள்",
        "Recommended Meals": "பரிந்துரைக்கப்பட்ட உணவுகள்",
        "Quick Tips": "விரைவு குறிப்புகள்",
        "Save All Settings": "அனைத்து அமைப்புகளையும் சேமிக்கவும்",
        "Dark Mode": "இருண்ட முறை",
        "Light Mode": "ஒளி முறை",
        "Notifications": "அறிவிப்புகள்",
        "Enable Notifications": "அறிவிப்புகளை இயக்கு",
        "Workout Reminder": "பயிற்சி நினைவூட்டல்",
        "Meal Reminder": "உணவு நினைவூட்டல்",
        "Daily Calorie Goal": "தினசரி கலோரி இலக்கு",
        "Daily Water Goal": "தினசரி நீர் இலக்கு",
        "Profile Visibility": "சுயவிவர தெரிவுநிலை",
        "Public": "பொது",
        "Friends Only": "நண்பர்கள் மட்டும்",
        "Private": "தனிப்பட்ட",
        "Challenges": "சவால்கள்",
        "Leaderboard": "முன்னணி பட்டியல்",
        "Find Friends": "நண்பர்களை தேடு",
        "Friend Requests": "நண்பர் கோரிக்கைகள்",
        "My Friends": "என் நண்பர்கள்",
        "Activity Feed": "செயல்பாட்டு ஊட்டம்"
    }
};

// Load translations
async function loadTranslations(lang) {
    currentLang = lang;
    applyTranslations();
    updateActiveLanguageButton();
}

// Apply translations to the page
function applyTranslations() {
    if (currentLang === 'en') return;
    
    const dict = commonWords[currentLang];
    if (!dict) return;
    
    // Find all text nodes and translate
    document.querySelectorAll('h1, h2, h3, h4, p, span, button, a, label, div').forEach(element => {
        const originalText = element.innerText.trim();
        if (originalText && dict[originalText] && !element.querySelector('*')) {
            element.innerText = dict[originalText];
        }
    });
    
    // Update document title
    if (dict['FitAI']) {
        document.title = dict['FitAI'];
    }
}

// Change language
function changeLanguage(lang) {
    localStorage.setItem('language', lang);
    location.reload();
}

// Update active language button
function updateActiveLanguageButton() {
    const currentLang = localStorage.getItem('language') || 'en';
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

// Load on page load
document.addEventListener('DOMContentLoaded', () => {
    const savedLang = localStorage.getItem('language') || 'en';
    currentLang = savedLang;
    applyTranslations();
    updateActiveLanguageButton();
});