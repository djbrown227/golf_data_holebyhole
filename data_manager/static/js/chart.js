async function loadTopGolfers(fileName) {
    try {
        // Fetch data from the server
        const response = await fetch(`/fetch_golf_data?file_name=${fileName}`);
        
        // Check if the response is successful (status 200)
        if (!response.ok) {
            throw new Error('Failed to fetch data from the server');
        }
        
        // Parse the JSON data
        const data = await response.json();
        
        // Log the entire data for debugging purposes
        console.log('Full Data:', data);

        // Log top golfers
        console.log('Top Golfers:', data.top_golfers);

        // Check if the expected data is present
        if (!data.top_golfers) {
            throw new Error('Missing required data fields');
        }

        // Extract the relevant golfers
        const golfers = data.top_golfers;

        // Check if data is valid
        if (!Array.isArray(golfers) || golfers.length === 0) {
            throw new Error('Invalid data format');
        }

        // Calculate cumulative scores and add them to the golfer data
        golfers.forEach(golfer => {
            // Assuming golfer.scores is an array of scores for each hole
            if (golfer.scores && Array.isArray(golfer.scores)) {
                const cumulativeScore = golfer.scores.reduce((acc, score) => acc + score, 0);
                golfer.cumulativeScore = cumulativeScore;
            } else {
                golfer.cumulativeScore = 0; // If no scores, assume 0 cumulative score
            }
        });

        // Sort golfers by cumulative score (ascending)
        golfers.sort((a, b) => a.cumulativeScore - b.cumulativeScore);

        // Take the top 10 golfers
        const top10Golfers = golfers.slice(0, 10);

        // Generate HTML to display top 10 golfers and their cumulative scores
        const golferList = document.getElementById('golferList');
        golferList.innerHTML = ''; // Clear any previous content

        top10Golfers.forEach(golfer => {
            const golferItem = document.createElement('li');
            golferItem.textContent = `${golfer.name} - Cumulative Score: ${golfer.cumulativeScore}`;
            golferList.appendChild(golferItem);
        });
    } catch (error) {
        console.error('Error loading top golfers:', error);
        alert('Failed to load top golfers. Please check the console for details.');
    }
}
