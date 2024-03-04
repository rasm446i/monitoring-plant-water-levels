// Fetch moisture levels from the endpoint and update the colors
async function updateColors() {
    try {
        const response = await fetch("http://10.0.70.233:5000/get_soil_moisture_hourly");
        const moistureData = await response.json();

        // Check if moistureData is an array
        if (!Array.isArray(moistureData)) {
            console.error("Invalid data format. Expected an array.");
            return;
        }

        // Loop through each microcontroller entry
        for (const entry of moistureData) {
            const microcontrollerId = entry.microcontroller_id;
            const moistureLevel = entry.moisture_level;

            // Ensure microcontrollerId is a valid number greater than 0
            const numericMicrocontrollerId = parseInt(microcontrollerId, 10);
            if (isNaN(numericMicrocontrollerId) || numericMicrocontrollerId <= 0) {
                console.error(`Invalid microcontrollerId: ${microcontrollerId}`);
                continue;
            }

            const clickableBox = document.querySelector(`.clickable-box[data-microcontroller-id="${numericMicrocontrollerId}"]`);

            // Check if clickableBox is not null and moistureLevel is defined before updating style
            if (clickableBox !== null && moistureLevel !== undefined) {
                // Update color based on moisture level
                if (moistureLevel < 1000) {
                    clickableBox.style.backgroundColor = "#2B287E"; // High moisture
                    clickableBox.style.color = "white";
                } else if (moistureLevel >= 1000 && moistureLevel < 1500) {
                    clickableBox.style.backgroundColor = "#676ECE"; // Medium-high moisture
                    clickableBox.style.color = "white";
                } else if (moistureLevel >= 1500 && moistureLevel < 2500) {
                    clickableBox.style.backgroundColor = "green"; // Medium moisture
                    clickableBox.style.color = "white";
                } else if (moistureLevel >= 2500 && moistureLevel <= 3000) {
                    clickableBox.style.backgroundColor = "#E3D644"; // Medium-low moisture
                    clickableBox.style.color = "black";
                } else {
                    clickableBox.style.backgroundColor = "#F4A460"; // Low moisture
                    clickableBox.style.color = "white";
                }
            } else {
                console.error(`Element with data-microcontroller-id="${numericMicrocontrollerId}" not found or moistureLevel undefined.`);
            }
        }

        return Promise.resolve(); // Resolve the promise if everything is successful
    } catch (error) {
        console.error("Error updating colors:", error);
        return Promise.reject(error); // Reject the promise if there's an error
    }
}

// Call the updateColors function when the script is loaded
updateColors().then(() => {
    console.log("Colors updated successfully");
}).catch(error => {
    console.error("Error updating colors:", error);
});