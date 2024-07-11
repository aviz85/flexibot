document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('create-chatbot-form');
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData(form);
        const chatbotData = Object.fromEntries(formData.entries());

        fetch('/api/chatbot', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(chatbotData),
        })
        .then(response => response.json())
        .then(data => {
            if (data.id) {
                alert('Chatbot created successfully!');
                window.location.reload();  // Refresh the page to show the new chatbot
            } else {
                alert('Error creating chatbot: ' + data.error);
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            alert('An error occurred while creating the chatbot.');
        });
    });
});