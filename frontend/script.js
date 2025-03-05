const API_BASE_URL = "http://127.0.0.1:8086";

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
      body: formData,
    });

    let result = await response.json();
    if (response.ok) {
      uploadStatus.innerText = "Upload Successful!";
      updateLocations(result.data.locations);
    } else {
      uploadStatus.innerText = `Error: ${result.detail}`;
    }
  } catch (error) {
    uploadStatus.innerText = `Error: ${error.message}`;
  }
}

// Function to Update Location Dropdowns
function updateLocations(locations) {
  let locationDropdowns = [
    "restrictedRoadStart",
    "restrictedRoadEnd",
    "restrictedLocation",
    "vehicleRestrictedRoadStart",
    "vehicleRestrictedRoadEnd",
  ];

  locationDropdowns.forEach((dropdownId) => {
    let dropdown = document.getElementById(dropdownId);
    dropdown.innerHTML = ""; // Clear existing options
    locations.forEach((location) => {
      let option = document.createElement("option");
      option.value = location;
      option.textContent = location;
      dropdown.appendChild(option);
    });
  });
}

// Add Shop
async function addShop() {
  let shopName = document.getElementById("shopName").value;
  let shopDemand = document.getElementById("shopDemand").value;

  if (!shopName || !shopDemand) {
    alert("Please enter shop name and demand.");
    return;
  }

  let response = await fetch(`${API_BASE_URL}/add_shop`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      shop_name: shopName,
      shop_demand: parseInt(shopDemand),
    }),
  });

  let result = await response.json();

  if (response.ok) {
    alert(result.message); // Show success message
    document.getElementById(
      "shopList"
    ).innerHTML += `<li>${shopName} - Demand: ${shopDemand}</li>`;
  } else {
    alert(`Error: ${result.detail}`);
  }
}

// Add Vehicle
async function addVehicle() {
  let vehicleName = document.getElementById("vehicleName").value;
  let vehicleCapacity = document.getElementById("vehicleCapacity").value;

  if (!vehicleName || !vehicleCapacity) {
    alert("Please enter vehicle name and capacity.");
    return;
  }

  let response = await fetch(`${API_BASE_URL}/add_vehicle`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      vehicle_name: vehicleName,
      vehicle_capacity: parseInt(vehicleCapacity),
    }),
  });

  let result = await response.json();
  alert(result.message);
}

// Solve TSP
async function solveTSP() {
  let tspResult = document.getElementById("tspResult");
  tspResult.innerText = "Solving TSP...";

  try {
    let response = await fetch(`${API_BASE_URL}/solve_tsp`, { method: "POST" });
    let result = await response.json();
    tspResult.innerText = response.ok
      ? `TSP Route: ${result.route_order.join(" → ")}\nTotal Distance: ${
          result.total_distance
        } km`
      : `Error: ${result.detail}`;
  } catch (error) {
    tspResult.innerText = `Error: ${error.message}`;
  }
}

// Solve VRP
async function solveVRP() {
  let vrpResult = document.getElementById("vrpResult");
  vrpResult.innerText = "Solving VRP...";

  try {
    let response = await fetch(`${API_BASE_URL}/solve_vrp`, { method: "POST" });
    let result = await response.json();
    vrpResult.innerText = response.ok
      ? `VRP Routes: ${JSON.stringify(result.routes)}\nTotal Distance: ${
          result.total_distance
        } km`
      : `Error: ${result.detail}`;
  } catch (error) {
    vrpResult.innerText = `Error: ${error.message}`;
  }
}
