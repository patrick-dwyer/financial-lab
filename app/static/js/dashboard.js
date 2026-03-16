function collectData() {
    console.log("Calculate clicked - gathering data from blocks...");
    const container = document.getElementById('block-container');
    const blocks = Array.from(container.getElementsByClassName('block'));

    // Create an empty list to store our cleaned-up data
    const eventData = [];

    blocks.forEach(block => {
        // Skip the "Base Mortgage" block since it doesn't have the event inputs
        if (block.classList.contains('base')) return;

        // Find the type (Lump Sum or Rate Change) from the <strong> tag
        const type = block.querySelector('strong').innerText;

        // Extract values from the specific inputs we built earlier
        const month = block.querySelector('.block-month').value;
        const value = block.querySelector('.block-amount').value;

        // Only add to our list if the user actually typed something
        if (month && value) {
            eventData.push({
                type: type,
                month: parseInt(month),
                value: parseFloat(value)
            });
        }
    });

    // --- THE HANDSHAKE START ---
    fetch('/calculate', {
        method: 'POST', // Telling the server we are "Posting" a package
        headers: {
            'Content-Type': 'application/json', // Telling Python the package contains JSON
        },
        body: JSON.stringify(eventData), // Turning the list into a string for transport
    })
    .then(response => response.json()) // Waiting for Python to answer and parsing its JSON
    .then(data => {
        console.log("Python Calculation Result:", data);
        // This is where we will eventually update the chart and stats!
    })
    .catch(error => console.error('Error:', error)); // Error handling if the server is down
    

    console.log("Cleaned Data for Python:", eventData);
    return eventData;
}

function addBlock(type) {
    const container = document.getElementById('block-container');
    const newBlock = document.createElement('div');
    newBlock.className = 'block';
    
    const label = type === "Lump Sum" ? "Amount:" : "New Percent:";
    const placeholder = type === "Lump Sum" ? "$" : "%";

    
    newBlock.innerHTML = `
        <div style="display: flex; justify-content: space-between;">
            <strong>${type}</strong>
            <button onclick="this.parentElement.parentElement.remove(); sortBlocks();" 
                    style="background:none; border:none; color:red; cursor:pointer;">✕</button>
        </div>
        <div style="margin-top:10px;">
            <label>Month:</label>
            <input type="number" class="block-month" placeholder="60" onchange="sortBlocks()" style="width:60px">
        </div>
        <div style="margin-top:5px;">
            <label>${label}</label>
            <input type="number" class="block-amount" placeholder="${placeholder}" style="width:80px">
        </div>
    `;
    
    container.appendChild(newBlock);
}

function sortBlocks() {
    const container = document.getElementById('block-container');
    const blocks = Array.from(container.getElementsByClassName('block'));

    // Keep the "Base Mortgage" at the very top
    const baseBlock = blocks.find(b => b.classList.contains('base'));
    const dynamicBlocks = blocks.filter(b => !b.classList.contains('base'));

    dynamicBlocks.sort((a, b) => {
        const valA = parseInt(a.querySelector('.block-month').value) || 0;
        const valB = parseInt(b.querySelector('.block-month').value) || 0;
        return valA - valB;
    });

    container.innerHTML = '';
    if (baseBlock) container.appendChild(baseBlock);
    dynamicBlocks.forEach(block => container.appendChild(block));
}