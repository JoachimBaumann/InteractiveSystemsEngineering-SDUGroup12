// When the DOM is fully loaded, we set up our event listeners and initial state
document.addEventListener('DOMContentLoaded', function() {

  // Set up the initial date range for the 'From' and 'To' inputs
  setupInitialDateRange();
  fetchAllCategoriesData();
  // Fetch initial chart data for default date range
  const initialFromDate = document.getElementById('from-date').value;
  const initialToDate = document.getElementById('to-date').value;
  fetchInitialChartData(initialFromDate, initialToDate);

  // Event listener for when a category is selected from the dropdown
  document.getElementById('category-dropdown').addEventListener('change', function(event) {
    var selectedCategoryId = event.target.value;
    var fromDate = document.getElementById('from-date').value;
    var toDate = document.getElementById('to-date').value;
    if (selectedCategoryId === 'all') {
      fetchAllCategoriesData(); // Fetch and sum up data for all categories
    } else {
      fetchCategoryData(selectedCategoryId);
    }
  
    // Fetch new spending data for the selected category
    fetchInProgressSpendingData(fromDate, toDate, selectedCategoryId);
    fetchForecastSpendingData(fromDate, toDate, selectedCategoryId);
  });

  // Event listeners for date range changes
  document.getElementById('from-date').addEventListener('change', updateDateRange);
  document.getElementById('to-date').addEventListener('change', updateDateRange);
});

// This function updates the budget, expenses, and remainder in the UI
function updateValues(budget, expenses, remainder) {
  document.getElementById('budget').textContent = budget + 'kr';
  document.getElementById('expenses').textContent = expenses + 'kr';
  document.getElementById('remainder').textContent = remainder + 'kr';
}

function fetchInitialChartData(fromDate, toDate) {
  // Log the date range being used to fetch initial chart data
  console.log('Fetching initial chart data for date range:', fromDate, toDate);

  fetchInProgressSpendingData(fromDate, toDate, 'all');
  fetchForecastSpendingData(fromDate, toDate, 'all');
}


// Function to set up the initial date range on the date inputs
function setupInitialDateRange() {
  let initialFromDate = new Date();
  initialFromDate.setDate(1); // Set to the first day of the current month
  document.getElementById('from-date').valueAsDate = initialFromDate;

  let initialToDate = new Date(initialFromDate);
  initialToDate.setMonth(initialFromDate.getMonth() + 1);
  initialToDate.setDate(0); // Set to the last day of the current month
  document.getElementById('to-date').valueAsDate = initialToDate;

  // Log the initial date range values
  console.log('Initial From Date:', initialFromDate.toISOString().substring(0, 10));
  console.log('Initial To Date:', initialToDate.toISOString().substring(0, 10));
}


// Function to handle updating data when date range inputs are changed
function updateDateRange(event) {
  let fromDate = document.getElementById('from-date').value;
  let toDate = document.getElementById('to-date').value;
  let selectedCategoryId = document.getElementById('category-dropdown').value;

  fetchInProgressSpendingData(fromDate, toDate, selectedCategoryId);
  fetchForecastSpendingData(fromDate, toDate, selectedCategoryId);
}

// Call the change event listener on category dropdown to load initial category data
const categoryDropdown = document.getElementById('category-dropdown');
if (categoryDropdown) {
  categoryDropdown.dispatchEvent(new Event('change'));
} else {
  console.error('Category dropdown not found');
}


function fetchAllCategoriesData() {
  fetch('/get-all-categories-data')
    .then(response => response.json())
    .then(data => {
        updateValues(data.totalBudget, data.totalExpenses, data.totalRemainder);
        // Log the data fetched for all categories
        console.log('Data for all categories:', data);
    })
    .catch(error => {
        console.error('Error fetching data for all categories: ', error);
    });
}


function fetchCategoryData(categoryId) {
  fetch(`/get-category-data/${categoryId}`)
      .then(response => response.json())
      .then(data => {
          updateValues(data.budget, data.expenses, data.remainder);
      })
      .catch(error => {
          console.error('Error fetching data: ', error);
      });
}

function createInProgressSpendingChart(data) {
  const ctx = document.getElementById('inProgressSpendingChart').getContext('2d');

  // Destroy the old chart if it exists
  if (window.inProgressChart) {
    window.inProgressChart.destroy();
  }

  // Create a new chart
  window.inProgressChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: data.labels,
      datasets: [{
        label: 'In Progress Spending',
        data: data.values,
        backgroundColor: 'rgba(54, 162, 235, 0.2)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
}


function createForecastSpendingChart(data) {
  const ctx = document.getElementById('forecastSpendingChart').getContext('2d');

  // Destroy the old chart if it exists
  if (window.forecastChart) {
    window.forecastChart.destroy();
  }

  // Create a new chart
  window.forecastChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: data.labels,
      datasets: [{
        label: 'Forecast Spending',
        data: data.values,
        backgroundColor: 'rgba(255, 206, 86, 0.2)',
        borderColor: 'rgba(255, 206, 86, 1)',
        borderDash: [5, 5], // Creates a dashed line for the forecast data
        borderWidth: 2
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: false, // Allow the chart to auto-scale
          ticks: {
            callback: function(value, index, values) {
              // Custom formatting can go here
              return value.toLocaleString(); // This will format ticks values as local string
            }
          }
        }
      },
      tooltips: {
        mode: 'index',
        intersect: false,
        callbacks: {
          label: function(tooltipItem, chart) {
            var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
            return datasetLabel + ': ' + tooltipItem.yLabel.toLocaleString();
          }
        }
      },
      hover: {
        mode: 'nearest',
        intersect: true
      },
      elements: {
        line: {
          tension: 0 // Disables bezier curves to make the line straight
        }
      }
    }
  });
}




function fetchInProgressSpendingData(fromDate, toDate, selectedCategoryId) {
  const payload = {
    startDate: fromDate,
    endDate: toDate,
    categoryId: selectedCategoryId === 'all' ? null : selectedCategoryId
  };

  fetch('/get-in-progress-spending', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(payload)
  })
  .then(response => response.json())
  .then(data => {
    // Log the in-progress spending data received
    console.log('In-Progress spending data:', data);
    createInProgressSpendingChart(data);
  })
  .catch(error => {
    console.error('Error fetching in-progress spending data: ', error);
  });
}

function fetchForecastSpendingData(fromDate, toDate, selectedCategoryId) {
  const payload = {
    startDate: fromDate,
    endDate: toDate,
    categoryId: selectedCategoryId === 'all' ? null : selectedCategoryId
  };

  fetch('/get-forecast-spending', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(payload)
  })
  .then(response => response.json())
  .then(data => {
    // Log the received forecast spending data
    console.log('Forecast spending data:', data);

    // Check if the data contains 'labels' and 'values'
    if (data && data.labels && data.values) {
      createForecastSpendingChart({
        labels: data.labels,
        values: data.values
      });
    } else {
      // Log an error or handle the absence of 'labels' and 'values' appropriately
      console.error('Forecast spending data is missing `labels` or `values`:', data);
    }
  })
  .catch(error => {
    console.error('Error fetching forecast spending data: ', error);
  });
}
