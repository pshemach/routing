const API_BASE_URL = "http://127.0.0.1:8085"; // Backend API URL

// Upload CSV File
async function uploadMatrix() {
    let fileInput = document.getElementById("csvFile");
    let uploadStatus = document.getElementById("uploadStatus");

    if (!fileInput.files.length) {
        uploadStatus.innerText = "Please select a CSV file.";
        return;
    }

    let formData = new FormData();
    formData.append("file", fileInput.files[0]);

    uploadStatus.innerText = "Uploading...";

    try {
        let response = await fetch(`${API_BASE_URL}/upload_matrix`, {
            method: "POST",
            body: formData
        });

        let result = await response.json();

        if (response.ok) {
            uploadStatus.innerText = `Upload Successful! Session ID: ${result.session_id}`;
        } else {
            uploadStatus.innerText = `Error: ${result.detail}`;
        }
    } catch (error) {
        uploadStatus.innerText = `Error: ${error.message}`;
    }
}

// Solve TSP
async function solveTSP() {
    let sessionId = document.getElementById("tspSessionId").value;
    let tspResult = document.getElementById("tspResult");

    if (!sessionId) {
        tspResult.innerText = "Please enter a valid Session ID.";
        return;
    }

    tspResult.innerText = "Solving TSP...";

    try {
        let response = await fetch(`${API_BASE_URL}/solve_tsp?session_id=${sessionId}`, {
            method: "POST"
        });

        let result = await response.json();

        if (response.ok) {
            tspResult.innerText = `TSP Route: ${result.route_order.join(" → ")}\nTotal Distance: ${result.total_distance} km`;
        } else {
            tspResult.innerText = `Error: ${result.detail}`;
        }
    } catch (error) {
        tspResult.innerText = `Error: ${error.message}`;
    }
}

// Delete Matrix
async function deleteMatrix() {
    let sessionId = document.getElementById("deleteSessionId").value;
    let deleteStatus = document.getElementById("deleteStatus");

    if (!sessionId) {
        deleteStatus.innerText = "Please enter a valid Session ID.";
        return;
    }

    deleteStatus.innerText = "Deleting...";

    try {
        let response = await fetch(`${API_BASE_URL}/delete_matrix?session_id=${sessionId}`, {
            method: "DELETE"
        });

        let result = await response.json();

        if (response.ok) {
            deleteStatus.innerText = result.message;
        } else {
            deleteStatus.innerText = `Error: ${result.detail}`;
        }
    } catch (error) {
        deleteStatus.innerText = `Error: ${error.message}`;
    }
}