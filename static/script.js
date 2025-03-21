
async function askChatbot(question){
    try{
        const response = await fetch('/', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'}, 
            body: JSON.stringify(question),
           });
        if (!response.ok){
            throw new Error('HTTP Error, Status ${response.status}');
        }
        const data = await response.json();
    } catch(error){
        console.error('Error:', error);
    }
    console.log(response);
}


async function handlePromptSubmission(event){
    // Stop page reload
    event.preventDefault();  
    // Get the content of the input field
    const question = document.getElementById("user-question").value.trim();
    console.log("User Question:", userQuestion);
    response = await askChatbot(question);

}
document.findElementById('chat-form').addEventListener("submit", handlePromptSubmission)