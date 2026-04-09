// variable to hold the chart instance
let mortgageChart = null;
let scenarios = [{ id: 0 }]; // Track active scenarios
let activeScenarioIndex = 0;

function addScenario() {
    const newIndex = scenarios.length;
    const currentContainer = document.getElementById(`scenario-${activeScenarioIndex}`);
    
    // 1. Perform the clone
    const newContainer = currentContainer.cloneNode(true);
    newContainer.id = `scenario-${newIndex}`;
    newContainer.style.display = 'none';

    // 2. MANUAL VALUE SYNC: cloneNode doesn't copy current input values
    const currentInputs = currentContainer.querySelectorAll('input, select');
    const newInputs = newContainer.querySelectorAll('input, select');
    
    currentInputs.forEach((input, i) => {
        newInputs[i].value = input.value;
    });

    document.getElementById('scenario-wrapper').appendChild(newContainer);
    
    // Create the Tab button
    const tabBtn = document.createElement('button');
    tabBtn.className = 'tab-btn';
    tabBtn.innerText = `S${newIndex + 1}`;
    tabBtn.onclick = () => switchScenario(newIndex);
    
    const tabsArea = document.getElementById('scenario-tabs');
    tabsArea.insertBefore(tabBtn, tabsArea.lastElementChild);
    
    scenarios.push({ id: newIndex });
}

function switchScenario(index) {
    // 1. Hide all scenario containers and show the selected one
    scenarios.forEach((s, i) => {
        const container = document.getElementById(`scenario-${i}`);
        if (container) {
            container.style.display = (i === index) ? 'flex' : 'none';
        }
    });

    // 2. Update the activeScenarioIndex so addBlock knows where to go
    activeScenarioIndex = index;

    // 3. Toggle the "active" class on the tab buttons
    const tabs = document.querySelectorAll('.tab-btn');
    tabs.forEach((btn, i) => {
        if (i === index) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });

    // refresh results to reflect user choice for highlight
    if (window.lastResults) {
        updateComparisonTable(window.lastResults);
    }
}

function collectData() {
    // Loop through every scenario container
    const payload = scenarios.map((scenario, index) => {
        const container = document.getElementById(`scenario-${index}`);
        const blocks = Array.from(container.getElementsByClassName('block'));
        
        let baseSettings = {};
        const eventBlocks = [];

        blocks.forEach(block => {
            if (block.classList.contains('base')) {
                // Extract base mortgage settings
                baseSettings = {
                    principal: parseFloat(block.querySelector('.base-principal').value),
                    amortization: parseFloat(block.querySelector('.base-amortization').value),
                    interest: parseFloat(block.querySelector('.base-interest').value) / 100,
                    payment: block.querySelector('.base-payment').value
                };
            } else {
                // Extract event block type and value
                const type = block.querySelector('strong').innerText
                const month = parseInt(block.querySelector('.block-month').value)
                let rawValue = parseFloat(block.querySelector('.block-amount').value)

                eventBlocks.push({
                    type: type,
                    month: month,
                    value: type === "Rate Change" ? rawValue / 100 : rawValue
                });
            }
        });
        return { base: baseSettings, events: eventBlocks };
    });

    // Send the list of scenarios to Python
    fetch('/calculate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
    })
    .then(response => response.json())
    .then(data => {
    
    if (data.status === "success") {
        // Pass the entire list of scenarios to the chart
        updateChart(data.scenarios);
        window.lastResults = data.scenarios; // Store results so we can refresh on tab switch
        updateComparisonTable(data.scenarios);
    }
})
    .catch(error => {
        console.error('Handshake failed:', error);
    });
    

    console.log("Cleaned Data for Python:", eventData);
    return eventData;
}

function addBlock(type) {
    // Target the active scenario container
    const container = document.getElementById(`scenario-${activeScenarioIndex}`);
    
    const newBlock = document.createElement('div');
    newBlock.className = 'block';
    
    let label = "Amount:";
    let placeholder = "$";

    if (type === "Rate Change") {
        label = "New Percent:";
        placeholder = "%";
    } else if (type === "Payment Change") {
        label = "New Monthly:";
        placeholder = "$";
    }
    
    // Updated button to include sortBlocks()
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
    // Only sort the blocks for the active scenario
    const container = document.getElementById(`scenario-${activeScenarioIndex}`);
    const blocks = Array.from(container.getElementsByClassName('block'));

    const baseBlock = blocks.find(b => b.classList.contains('base'));
    const dynamicBlocks = blocks.filter(b => !b.classList.contains('base'));

    dynamicBlocks.sort((a, b) => {
        const valA = parseInt(a.querySelector('.block-month').value) || 0;
        const valB = parseInt(b.querySelector('.block-month').value) || 0;
        return valA - valB;
    });

    // Re-append only to the active container
    container.innerHTML = '';
    if (baseBlock) container.appendChild(baseBlock);
    dynamicBlocks.forEach(block => container.appendChild(block));
}

function updateChart(scenarioResults) {
    const ctx = document.getElementById('mortgageChart').getContext('2d');
    if (mortgageChart) { mortgageChart.destroy(); }

    // 1. Determine the longest timeline among all scenarios
    const maxMonths = Math.max(...scenarioResults.map(s => s.visual_principal_list.length));
    const labels = Array.from({length: maxMonths}, (_, i) => i);

    // 2. Define a set of colors for different scenarios
    const colors = [
        { border: '#4bc0c0', bg: 'rgba(75, 192, 192, 0.1)' }, // Teal (S1)
        { border: '#ff6384', bg: 'rgba(255, 99, 132, 0.1)' }, // Pink (S2)
        { border: '#36a2eb', bg: 'rgba(54, 162, 235, 0.1)' }, // Blue (S3)
        { border: '#ffce56', bg: 'rgba(255, 206, 86, 0.1)' }  // Yellow (S4)
    ];

    // 3. Map the scenario results into Chart.js datasets
    const datasets = scenarioResults.map((result, index) => {
        const color = colors[index % colors.length]; // Cycle colors if > 4 scenarios
        return {
            label: `Scenario ${index + 1}`,
            data: result.visual_principal_list,
            borderColor: color.border,
            backgroundColor: color.bg,
            borderWidth: 2,
            pointRadius: 0,
            fill: true
        };
    });

    // 4. Initialize the Chart
    mortgageChart = new Chart(ctx, {
        type: 'line',
        data: { labels: labels, datasets: datasets },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { callback: (value) => '$' + value.toLocaleString() },
                    title: { display: true, text: 'Remaining Principal ($)' }
                },
                x: { title: { display: true, text: 'Month' } }
            }
        }
    });
}

// function to update summary table of scenarios
function updateComparisonTable(scenarioResults) {
    const tableBody = document.getElementById('comparison-table-body');
    if (!tableBody) return;

    tableBody.innerHTML = ''; // Clear old data

    scenarioResults.forEach((result, index) => {
        // Calculate variables
        const initialPrincipal = result.visual_principal_list[0];
        const totalInterest = result.total_interest;
        const totalCost = initialPrincipal + totalInterest;
        
        const years = Math.floor(result.payoff_month / 12);
        const months = result.payoff_month % 12;
        const timeString = `${years}y ${months}m`;

        // Check if this is the scenario currently selected in the sidebar
        const isActive = (index === activeScenarioIndex);
        const rowStyle = isActive ? 'background: #252525; border-left: 4px solid #2ecc71;' : '';

        const row = `
            <tr style="border-bottom: 1px solid #333; ${rowStyle}">
                <td style="padding: 15px; font-weight: bold;">Scenario ${index + 1}</td>
                <td style="color: #ff6384;">$${totalInterest.toLocaleString(undefined, {minimumFractionDigits: 2})}</td>
                <td>${timeString}</td>
                <td style="color: #2ecc71; font-weight: bold;">$${totalCost.toLocaleString(undefined, {minimumFractionDigits: 2})}</td>
            </tr>
        `;
        tableBody.insertAdjacentHTML('beforeend', row);
    });
}