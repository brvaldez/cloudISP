async function fetchViewCount() {
    try {
        const response = await fetch('https://<your-function-app-url>/api/getViewCount');
        const data = await response.json();
        document.getElementById('view-count').textContent = `This website has been viewed ${data.viewCount} times.`;
    } catch (error) {
        console.error('Error fetching view count:', error);
        document.getElementById('view-count').textContent = 'Unable to load view count.';
    }
}

window.onload = fetchViewCount;
