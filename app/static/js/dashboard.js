// Dashboard javascript logic for mortgage lab. Includes the following functions:
// - addScenario: add a new scenario to compare to existing scenarios
// - switchScenario: highlight  which scenario is currently selected on screen and show details of that scenario in sidebar
// - collectData: take user input details (base mortgage + any blocks) and send/receive data to/from Python backend
// - addBlock: add a new block to the scenario to impact outcome of calculations
// - sortBlocks: sort blocks for scenario based on month in descending order
// - updateChart: ensure chart is updated with all scenarios plotted
// - updateComparisonTable: update comparison table with all scenarios for their columns

let mortgageChart = null; // variable to hold the chart instance
let scenarios = [{ id: 0 }]; // track active scenarios
let activeScenarioIndex = 0; // default to scenario 1

const max_scenarios = 5; // cap on scenarios to not overload the sidebar

function addScenario() {

    // Check if scenarios are maxed out before continuing
    if (scenarios.length >= max_scenarios) {
        return; // Exits function with no changes
    }

    const newIndex = scenarios.length; // determine how many scenarios are present
    const currentContainer = document.getElementById(`scenario-${activeScenarioIndex}`); // find current scenario
    
    // Perform the clone
    const newContainer = currentContainer.cloneNode(true); // clone scneario with same features
    newContainer.id = `scenario-${newIndex}`; // provide new unique id number based on scenario number
    newContainer.style.display = 'none'; // hide it initially, do not force it to open

    // Manual sync value
    const currentInputs = currentContainer.querySelectorAll('input, select'); // copy input values as selected scneario
    const newInputs = newContainer.querySelectorAll('input, select'); // make list of all empty values of new scenario
    
    // Loop to replace all new values with current scenario values
    currentInputs.forEach((input, i) => {
        newInputs[i].value = input.value;
    });


    document.getElementById('scenario-wrapper').appendChild(newContainer); // add to sidebar as last child of element
    
    // Create the Tab button
    const tabBtn = document.createElement('button'); // make button element
    tabBtn.className = 'tab-btn'; // give class name
    tabBtn.innerText = `S${newIndex + 1}`; // provide visual name with current number
    tabBtn.onclick = () => switchScenario(newIndex); // button click activates switchScenario function
    
    const tabsArea = document.getElementById('scenario-tabs'); // get list of all current tabs
    tabsArea.insertBefore(tabBtn, tabsArea.lastElementChild); // place new scenario button to far right side
    
    scenarios.push({ id: newIndex }); //add new scenario to scenario list

    // Check if we need to disable the scenario button for user
    checkScenarioLimit()

}

// Helper function to disable scenario button if max limit is reached (5 scenarios)
function checkScenarioLimit() {
    const addBtn = document.getElementById('add-scenario-btn') // find scenario button on page

    if (scenarios.length >= max_scenarios) {
        addBtn.ariaDisabled = true // disable button from working
        addBtn.style.opacity = '0.5'; // add styling to make it look different
        addBtn.style.cursor = 'not-allowed'; // make cursor change shape
        addBtn.title = "Maximum sceanrios reached." // text to display with cursor hover?
    } else {
        addBtn.ariaDisabled = false // enable button to work
        addBtn.style.opacity = '1'; // add styling to make it look "normal"
        addBtn.style.cursor = 'pointer'; // normal cursor when hovering over
        addBtn.title = "Add new comparison scenario" // text to display with cursor hover?

    }
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
        const container = document.getElementById(`scenario-${index}`); // make container for scenario
        const blocks = Array.from(container.getElementsByClassName('block')); // create block arrray for each scenario
        
        let baseSettings = {}; // empty object for base
        const eventBlocks = []; // empty array for blocks

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

                // push block values to block array eventBlocks
                eventBlocks.push({
                    type: type,
                    month: month,
                    value: type === "Rate Change" ? rawValue / 100 : rawValue // special case of Rate Change being percent
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
    .then(response => response.json()) // wait for response from python
    .then(data => {
    // with the data received, update chart and scenarios table
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
    
    const newBlock = document.createElement('div'); // make new div
    newBlock.className = 'block'; // add class name to div
    
    // default case of Lump Sum
    let label = "Amount:";
    let placeholder = "$";

    // case if Rate Change
    if (type === "Rate Change") {
        label = "New Percent:";
        placeholder = "%";

    // case if Payment Change
    } else if (type === "Payment Change") {
        label = "Payment Amount:";
        placeholder = "$";
    }
    
    // HTML to inject. Includes div for block, sortBlocks() function
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
    
    container.appendChild(newBlock); // add block to container of blocks for that scenario
}

function sortBlocks() {
    // Only sort the blocks for the active scenario
    const container = document.getElementById(`scenario-${activeScenarioIndex}`); // get active scenario
    const blocks = Array.from(container.getElementsByClassName('block')); // get array of current blocks

    const baseBlock = blocks.find(b => b.classList.contains('base')); // find base block
    const dynamicBlocks = blocks.filter(b => !b.classList.contains('base')); // find not base blocks for remainder

    // sort blocks based on month value from subtraction value
    dynamicBlocks.sort((a, b) => {
        const valA = parseInt(a.querySelector('.block-month').value) || 0;
        const valB = parseInt(b.querySelector('.block-month').value) || 0;
        return valA - valB;
    });

    // Re-append only to the active container
    container.innerHTML = '';
    if (baseBlock) container.appendChild(baseBlock); // add base block as first
    dynamicBlocks.forEach(block => container.appendChild(block)); // add sorted blocks
}

function updateChart(scenarioResults) {
        
    const ctx = document.getElementById('mortgageChart').getContext('2d'); // define canvas area for chart
    if (mortgageChart) { mortgageChart.destroy(); } // refresh with fresh chart

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
            pointRadius: 0,// function to update summary table of scenarios
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

function updateComparisonTable(scenarioResults) {

    const tableBody = document.getElementById('comparison-table-body'); // define comparison table
    if (!tableBody) return; // check if there is any data for the table

    tableBody.innerHTML = ''; // clear old data

    // look at each scenario loop
    scenarioResults.forEach((result, index) => {
        
        // Calculate variables
        const initialPrincipal = result.visual_principal_list[0];
        const totalInterest = result.total_interest;
        const totalCost = initialPrincipal + totalInterest;
        
        // convert months to years
        const years = Math.floor(result.payoff_month / 12);
        const months = result.payoff_month % 12;
        const timeString = `${years}y ${months}m`;

        // Check if this is the scenario currently selected in the sidebar
        const isActive = (index === activeScenarioIndex);
        const rowStyle = isActive ? 'background: #252525; border-left: 4px solid #2ecc71;' : '';
        
        // HTML injection to allow it to be highlighted when scenario selected
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