// variable to hold the chart instance
let mortgageChart = null;

function collectData() {
    console.log("Calculate clicked - gathering data from blocks...");
    const container = document.getElementById('block-container');
    const blocks = Array.from(container.getElementsByClassName('block'));

    // Create an empty list to store our cleaned-up data
    const eventData = [];

    blocks.forEach(block => {
        
        // Base mortgage calculations
        if (block.classList.contains('base')) {

            // extract values from base mortgage block
            const type = block.querySelector('strong').innerText;
            let principal = block.querySelector('.base-principal').value;
            let amortization = block.querySelector('.base-amortization').value;
            let interest = block.querySelector('.base-interest').value;
            let payment = block.querySelector('.base-payment').value;

            // convert whole number interst to decimal for calculations
            interest = interest / 100

            // Only add to block data if all fields completed
            if (type && principal && amortization && interest && payment) {
                eventData.push({
                    type: type,
                    principal: parseFloat(principal),
                    amortization: parseFloat(amortization),
                    interest: parseFloat(interest),
                    payment: payment
                })
            }

        } else {
            // Find the type (Lump Sum or Rate Change) from the <strong> tag
            const type = block.querySelector('strong').innerText;

            // Extract values from the specific inputs we built earlier
            const month = block.querySelector('.block-month').value;
            let value = block.querySelector('.block-amount').value;

            // Only add to our list if the user actually typed something
            if (month && value) {            

                if (type === "Rate Change") {
                    value = value / 100
                }

                eventData.push({
                    type: type,
                    month: parseInt(month),
                    value: parseFloat(value)
                });
            }

        };        
    });

    // --- THE HANDSHAKE START ---
    fetch('/calculate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(eventData),
    })
    .then(response => response.json())
    .then(data => {
        // 1. Log the result so we can see it in the console
        console.log("Python Calculation Result:", data);
        
        // 2. TRIGGER THE VISUALS
        // Make sure these names match exactly what Python sends back in jsonify()
        updateChart(data.base_principal, data.scenario_principal);
        
        
        // 3. UPDATE THE STAT CARDS
        // I'm assuming you have an ID for your interest saved display
        const savedElement = document.getElementById('interest-saved-val');
        if (savedElement) {
            savedElement.innerText = `$${data.interest_saved.toLocaleString(undefined, {minimumFractionDigits: 2})}`;
        }
    })
    .catch(error => {
        console.error('Handshake failed:', error);
    });
    

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

function updateChart(baseBalances, scenarioBalances) {
    const ctx = document.getElementById('mortgageChart').getContext('2d');

    // if chart already exists, destroy it before making a new one
    if (mortgageChart) {
        mortgageChart.destroy();
    }

    // 3. Create X-axis labels (Month 0, 1, 2, 3...)
    const maxMonths = Math.max(baseBalances.length, scenarioBalances.length);
    const labels = Array.from({length: maxMonths}, (_, i) => i);

    // 4. Initialize the Chart
    mortgageChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Original Mortgage',
                    data: baseBalances,
                    borderColor: 'rgba(75, 192, 192, 1)', // Teal
                    backgroundColor: 'rgba(75, 192, 192, 0.1)',
                    borderWidth: 2,
                    pointRadius: 0, // Hides dots for a clean line
                    fill: true
                },
                {
                    label: 'With Blocks',
                    data: scenarioBalances,
                    borderColor: 'rgba(255, 99, 132, 1)', // Pink/Red
                    backgroundColor: 'rgba(255, 99, 132, 0.1)',
                    borderWidth: 2,
                    pointRadius: 0,
                    fill: true
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false, // allows chart to fill full container height
            scales: {
                y: {
                    beginAtZero: true,
                    min: 0,
                    ticks: {
                        callback: function(value) {
                            return '$' + value.toLocaleString();
                        }
                    },
                    title: { display: true, text: 'Remaining Principal ($)' }
                },
                x: {
                    title: { display: true, text: 'Month' }
                }
            }
        }
    });
}