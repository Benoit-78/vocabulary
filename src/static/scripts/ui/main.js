export { updateTextFields };
import { goToRoot, changeLanguage } from "../api/main.js";


document.addEventListener("DOMContentLoaded", function() {
    const languageSelect = document.getElementById("languageSelect");
    const token = document.body.dataset.token;
    const currentPath = window.location.pathname;
    // const currentPath = document.URL

    languageSelect.addEventListener("change", function() {
        const selectedLanguage = languageSelect.value;
        const textData = getTextData();
        changeLanguage(token, selectedLanguage, textData, currentPath);
    });
});


function getTextData() {
    const textFields = document.querySelectorAll(".translatable-text");
    const textData = {};
    textFields.forEach(function(element) {
        textData[element.id || element.className] = element.textContent;
    });
    return textData;
}


function updateTextFields(selectedLanguage, translations_dict) {
    const translatableElements = document.querySelectorAll(".translatable-text");

    // Iterate over each element and update its text content based on the selected language
    translatableElements.forEach(element => {
        const originalText = element.textContent.trim();
        const translatedText = translations_dict[originalText] ? translations_dict[originalText][selectedLanguage] : originalText;
        element.textContent = translatedText;
    });
}


document.addEventListener("DOMContentLoaded", function() {
    const quitButton = document.getElementById("quitButton");
    const token = document.body.dataset.token;

    quitButton.addEventListener("click", function() {
        goToRoot(token);
    });
});
