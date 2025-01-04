// app/static/js/main.js

// Function to add new option input field
function addOption() {
    const container = document.querySelector('.option-inputs');
    const input = document.createElement('input');
    input.type = 'text';
    input.name = 'options';
    input.required = true;
    container.appendChild(input);
}

// Function to copy text to clipboard
function copyToClipboard(elementId) {
    const element = document.getElementById(elementId);
    element.select();
    document.execCommand('copy');
    
    // Show feedback
    const button = element.nextElementSibling;
    const originalText = button.textContent;
    button.textContent = 'Copied!';
    setTimeout(() => {
        button.textContent = originalText;
    }, 2000);
}

// Function to save poll to cookies
function savePollToCookies(pollId, adminCode, question) {
    let polls = getPollsFromCookies();
    polls[pollId] = {
        adminCode: adminCode,
        question: question
    };
    
    // Save for 30 days
    const expiryDate = new Date();
    expiryDate.setDate(expiryDate.getDate() + 30);
    
    document.cookie = `polls=${JSON.stringify(polls)};expires=${expiryDate.toUTCString()};path=/`;
}

// Function to get polls from cookies
function getPollsFromCookies() {
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith('polls='));
    
    if (cookieValue) {
        try {
            return JSON.parse(cookieValue.split('=')[1]);
        } catch (e) {
            return {};
        }
    }
    return {};
}

// Function to delete poll from cookies
function deletePoll(pollId) {
    let polls = getPollsFromCookies();
    delete polls[pollId];
    
    document.cookie = `polls=${JSON.stringify(polls)};path=/`;
    
    // Remove the poll from the UI
    const pollElement = document.getElementById(`poll-${pollId}`);
    if (pollElement) {
        pollElement.remove();
    }
    
    // Hide your polls section if empty
    const polls_list = document.querySelector('.your-polls-list');
    if (polls_list && polls_list.children.length === 0) {
        document.querySelector('.your-polls').style.display = 'none';
    }
}

// On page load, check if we need to save a new poll
// Function to load and display user's polls
function displayUserPolls() {
    const polls = getPollsFromCookies();
    const pollsList = document.querySelector('.your-polls-list');
    const yourPollsSection = document.querySelector('.your-polls');
    
    if (!pollsList || Object.keys(polls).length === 0) {
        if (yourPollsSection) {
            yourPollsSection.style.display = 'none';
        }
        return;
    }

    yourPollsSection.style.display = 'block';
    pollsList.innerHTML = '';

    for (const [pollId, pollData] of Object.entries(polls)) {
        const pollElement = document.createElement('div');
        pollElement.id = `poll-${pollId}`;
        pollElement.className = 'poll-item';
        pollElement.innerHTML = `
            <div class="poll-info">
                <div class="poll-details">
                    <span class="poll-question">${pollData.question}</span>
                    <span class="poll-id">ID: ${pollId}</span>
                </div>
                <div class="poll-actions">
                    <a href="/poll/${pollId}" class="btn-secondary btn-small">View Poll</a>
                    <a href="/results?poll_id=${pollId}&admin_code=${pollData.adminCode}" class="btn-secondary btn-small">Results</a>
                    <button onclick="deletePoll('${pollId}')" class="btn-danger btn-small">Delete</button>
                </div>
            </div>
        `;
        pollsList.appendChild(pollElement);
    }
}

document.addEventListener('DOMContentLoaded', function() {
    // If we're on the poll created page, save the new poll
    const pollId = document.getElementById('poll-id');
    const adminCode = document.getElementById('admin-code');
    if (pollId && adminCode) {
        savePollToCookies(pollId.value, adminCode.value);
    }
    
    // Display user's polls if we're on the home page
    displayUserPolls();
});