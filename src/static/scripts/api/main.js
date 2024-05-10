export { goToRoot, changeLanguage };
import { updateTextFields } from "../ui/main.js";


function changeLanguage(token, selectedLanguage, textData, currentPath) {
    fetch(
        `/common/change-language?token=${token}`,
        {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                texts: textData,
                path: currentPath,
            }),
        }
    )
    .then(response => {
        if (!response.ok) {
            throw new Error("Failed to change language");
        }
        return response.json();
    })
    .then(data => {
        updateTextFields(selectedLanguage, data.translations_dict);
        // location.reload();
        console.log("Language changed successfully");
    })
    .catch(error => {
        console.log(token);
        console.log(selectedLanguage);
        console.log(textData);
        console.log(currentPath);
        console.error("Error changing language:", error);
    });
}


function goToRoot(token) {
    window.location.href = `/welcome?token=${token}`;
}
