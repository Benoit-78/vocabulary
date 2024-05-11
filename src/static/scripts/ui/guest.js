import { sendGuestSettings, showTranslation, sendUserAnswer, nextGuess } from "../api/guest.js";


document.addEventListener(
    "DOMContentLoaded",
    function () {
        const progressBar = document.getElementById("progress-bar");
        progressBar.style.width = `${progressBar}%`;
    }
);

// English
document.addEventListener("DOMContentLoaded", function() {
    const englishButton = document.getElementById("englishButton");
    const token = document.body.dataset.token;
    console.log(token)

    englishButton.addEventListener("click", function() {
        sendGuestSettings(token, "English");
    });
});

// German
document.addEventListener("DOMContentLoaded", function() {
    const germanButton = document.getElementById("germanButton");
    const token = document.body.dataset.token;

    germanButton.addEventListener("click", function() {
        sendGuestSettings(token, "German");
    });
});

// Dutch
document.addEventListener("DOMContentLoaded", function() {
    const dutchButton = document.getElementById("dutchButton");
    const token = document.body.dataset.token;

    dutchButton.addEventListener("click", function() {
        sendGuestSettings(token, "Dutch");
    });
});

// Spanish
document.addEventListener("DOMContentLoaded", function() {
    const spanishButton = document.getElementById("spanishButton");
    const token = document.body.dataset.token;

    spanishButton.addEventListener("click", function() {
        sendGuestSettings(token, "Spanish");
    });
});

// Portuguese
document.addEventListener("DOMContentLoaded", function() {
    const portugueseButton = document.getElementById("portugueseButton");
    const token = document.body.dataset.token;

    portugueseButton.addEventListener("click", function() {
        sendGuestSettings(token, "Portuguese");
    });
});

// Russian
document.addEventListener("DOMContentLoaded", function() {
    const russianButton = document.getElementById("russianButton");
    const token = document.body.dataset.token;

    russianButton.addEventListener("click", function() {
        sendGuestSettings(token, "Russian");
    });
});

// Arabic
document.addEventListener("DOMContentLoaded", function() {
    const arabicButton = document.getElementById("arabicButton");
    const token = document.body.dataset.token;

    arabicButton.addEventListener("click", function() {
        sendGuestSettings(token, "Arabic");
    });
});

// Hebrew
document.addEventListener("DOMContentLoaded", function() {
    const hebrewButton = document.getElementById("hebrewButton");
    const token = document.body.dataset.token;

    hebrewButton.addEventListener("click", function() {
        sendGuestSettings(token, "Hebrew");
    });
});

// Chinese
document.addEventListener("DOMContentLoaded", function() {
    const chineseButton = document.getElementById("chineseButton");
    const token = document.body.dataset.token;

    chineseButton.addEventListener("click", function() {
        sendGuestSettings(token, "Chinese");
    });
});

// Latin
document.addEventListener("DOMContentLoaded", function() {
    const latinButton = document.getElementById("latinButton");
    const token = document.body.dataset.token;

    latinButton.addEventListener("click", function() {
        sendGuestSettings(token, "Latin");
    });
});

// Greek
document.addEventListener("DOMContentLoaded", function() {
    const greekButton = document.getElementById("greekButton");
    const token = document.body.dataset.token;

    greekButton.addEventListener("click", function() {
        sendGuestSettings(token, "Greek");
    });
});


// ============================================================
// ============================================================
// ============================================================
document.addEventListener("DOMContentLoaded", function() {
    const showTranslationButton = document.getElementById("showTranslationButton");
    const token = document.body.dataset.token;

    showTranslationButton.addEventListener("click", function() {
        showTranslation(numWords, count, score, token, language);
    });
});


document.addEventListener("DOMContentLoaded", function() {
    const yesButton = document.getElementById("yesButton");
    const token = document.body.dataset.token;

    yesButton.addEventListener("click", function() {
        sendUserAnswer(
            'Yes', numWords, count, score, content_box1, content_box2, token, language
        );
    });
});

document.addEventListener("DOMContentLoaded", function() {
    const noButton = document.getElementById("noButton");
    const token = document.body.dataset.token;

    noButton.addEventListener("click", function() {
        sendUserAnswer(
            'No', numWords, count, score, content_box1, content_box2, token, language
        );
    });
});


document.addEventListener("DOMContentLoaded", function() {
    const rattrapsButton = document.getElementById("rattrapsButton");
    const token = document.body.dataset.token;

    rattrapsButton.addEventListener("click", function() {
        nextGuess(
            newWords, newCount, newScore, token, language
        );
    });
});
