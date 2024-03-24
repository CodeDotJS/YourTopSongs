let currentAudio = null;
let audioCtx = null;
let lastHoveredDiv = null;


function displayErrorMessage(message) {
    const errorMessage = document.getElementById('errorMessage');
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
    setTimeout(() => {
        errorMessage.style.display = 'none';
    }, 2000)
}

function displayLoadingBar() {
    const loadingBarContainer = document.getElementById('loadingBarContainer');
    loadingBarContainer.style.display = 'block';
}

function updateLoadingProgress(progress) {
    const loadingBar = document.getElementById('loadingBar');
    loadingBar.style.width = progress + '%';
}

function hideLoadingBar() {
    const loadingBarContainer = document.getElementById('loadingBarContainer');
    loadingBarContainer.style.display = 'none';
}

function getRandomColor() {
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}

async function getPreviewUrl(trackUrl) {
    try {
        const trackId = trackUrl.split('/').pop();
        const response = await fetch(`/preview-url/${trackId}`);
        if (!response.ok) {
            throw new Error('Error fetching preview URL.');
        }
        const data = await response.json();
        const unquote = data.previewUrl.replace(/"/g, '');
        return unquote;
    } catch (error) {
        console.error('Error fetching preview URL:', error);
        displayErrorMessage('Error fetching preview URL. Please try again later.');
        return null;
    }
}

async function playPreview(trackUrl) {
    const previewUrl = await getPreviewUrl(trackUrl);
    if (previewUrl) {
        const audio = new Audio(previewUrl);
        audio.crossOrigin = 'anonymous';

        if (currentAudio && !currentAudio.paused) {
            currentAudio.pause();
            audioCtx.close();
        }

        audioCtx = new(window.AudioContext || window.webkitAudioContext)();
        audio.play();
        currentAudio = audio;

        audio.addEventListener('ended', () => {
            audioCtx.close();
        });
    } else {
        console.error('Preview URL not available.');
    }
}

function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
}

async function fetchData() {
    try {
        displayLoadingBar();
        const response = await fetch('/data/playlist_data.json');
        if (!response.ok) {
            throw new Error('Error fetching playlist data.');
        }
        return response.json();
    } catch (error) {
        console.error('Error fetching JSON:', error);
        displayErrorMessage('Error fetching playlist data. Please try again later.');
        throw error;
    } finally {
        hideLoadingBar();
    }
}

// Function to generate tracks
async function generateTracks() {
    try {
        displayLoadingBar();
        const data = await fetchData();
        let tracks = data.reduce((totalTracks, playlist) => totalTracks.concat(playlist.tracks), []);
        tracks = shuffleArray(tracks).slice(0, 25);
        const container = document.getElementById('container');
        container.innerHTML = ''; // Clear existing tracks

        tracks.forEach(track => {
            const div = document.createElement('div');
            div.className = 'track-box';
            div.style.setProperty('--random-color', getRandomColor());
            div.innerHTML = `
                            <img src="${track.cover_image}" alt="" class="cover-image">
                        `;
            div.addEventListener('mouseenter', () => {
                div.classList.add('hovered');
                playPreview(track.track_url);
                lastHoveredDiv = div;
            });
            div.addEventListener('mouseleave', () => {
                if (currentAudio) {
                    currentAudio.pause();
                    audioCtx.close();
                    const setSpotifyLink = document.getElementById('spotify');
                    setSpotifyLink.href = track.track_url;
                }
            });
            document.body.addEventListener('click', function() {
                currentAudio.pause();
            });
            container.appendChild(div);
        });
    } catch (error) {
        console.error('Error generating tracks:', error);
        displayErrorMessage("FAILED TO LOAD. PLEASE TRY AGAIN!");
    } finally {
        hideLoadingBar();
    }
}

// Call generateTracks on page load
window.onload = generateTracks;

// Event listener for the "SET" button
const setButton = document.getElementById('set');
setButton.addEventListener('click', generateTracks);

const shuffle = document.getElementById('refresh');
shuffle.addEventListener('click', function() {
    const container = document.getElementById('container');
    const tracks = Array.from(container.children);
    const shuffledTracks = shuffleArray(tracks);
    shuffledTracks.forEach((track, index) => {
        setTimeout(() => {
            container.appendChild(track);
        }, index * 100);
    });
});
