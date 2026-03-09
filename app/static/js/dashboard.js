// Placeholder to prevent errors when clicking the Calculate button
function collectData() {
    console.log("Calculate clicked - gathering data from blocks...");
}

function addBlock(type) {
    const container = document.getElementById('block-container');
    const newBlock = document.createElement('div');
    newBlock.className = 'block';
    
    const label = type === "Lump Sum" ? "Amount:" : "New Percent:";
    const placeholder = type === "Lump Sum" ? "$" : "%";

    // Added the Delete (✕) button logic back in
    newBlock.innerHTML = `
        <div style="display: flex; justify-content: space-between;">
            <strong>${type}</strong>
            <button onclick="this.parentElement.parentElement.remove(); sortBlocks();" 
                    style="background:none; border:none; color:red; cursor:pointer;">✕</button>
        </div>
        <div style="margin-top:10px;">
            <label>Month:</label>
            <input type="number" class="block-month" placeholder="60" oninput="sortBlocks()" style="width:60px">
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