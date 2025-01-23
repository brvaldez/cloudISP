const API_URL = "AccountEndpoint=https://bruno-ispdata.documents.azure.com:443/;AccountKey=Q5tIDXHfEHUxV6xxSy6v7GJrsE7OSKt5QTxxiTW4ywetb161zzfxHcWowmoWoEa0Wx8jWGVB9UQQACDbeEocKw==;";

async function updateVisitorCounter() {
    try {
        // Make a GET request to fetch the current visitor count
        const response = await fetch(API_URL);
        if (!response.ok) {
            throw new Error("Failed to fetch visitor count.");
        }

        // Parse the JSON response
        const data = await response.json();
        const count = data.count; // Assuming the API returns { "count": 123 }

        // Update the DOM with the visitor count
        document.getElementById("counter").textContent = count;
    } catch (error) {
        console.error("Error updating visitor counter:", error);
        document.getElementById("counter").textContent =
            "Error loading counter.";
    }
}

// Call the function to update the counter on page load
updateVisitorCounter();
