import { uploadCSV } from "../api/database.js";


document.addEventListener(
    "DOMContentLoaded",
    function() {
        // Bind the submit event of the form to the uploadCSV function
        document.getElementById("csvForm").addEventListener(
            "submit",
            function(event) {
                event.preventDefault(); // Prevent the form from submitting normally
                var token = document.getElementById("token").value;
                uploadCSV(token); // Call the uploadCSV function
            }
        );
    }
);