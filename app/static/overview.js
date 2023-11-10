// When the DOM is fully loaded, we set up our event listeners and initial state
document.addEventListener('DOMContentLoaded', function() {

  // Set up the initial date range for the 'From' and 'To' inputs
  setupInitialDateRange();
  fetchAllCategoriesData();

  // Event listener for when a category is selected from the dropdown
  document.getElementById('category-dropdown').addEventListener('change', function(event) {
      var selectedCategoryId = event.target.value;
      if (selectedCategoryId === 'all') {
        fetchAllCategoriesData(); // Fetch and sum up data for all categories
    } else {
      fetchCategoryData(selectedCategoryId);
    }
  });

  // Event listeners for date range changes
  document.getElementById('category-dropdown').addEventListener('change', updateDateRange);
  document.getElementById('from-date').addEventListener('change', updateDateRange);
  document.getElementById('to-date').addEventListener('change', updateDateRange);
});

// This function updates the budget, expenses, and remainder in the UI
function updateValues(budget, expenses, remainder) {
  document.getElementById('budget').textContent = budget + 'kr';
  document.getElementById('expenses').textContent = expenses + 'kr';
  document.getElementById('remainder').textContent = remainder + 'kr';
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
}

// Function to handle updating data when date range inputs are changed
function updateDateRange(event) {
  let fromDate = document.getElementById('from-date').value;
  let toDate = document.getElementById('to-date').value;
  let selectedCategoryId = document.getElementById('category-dropdown').value;

  // If you are using the 'selectedCategoryId', pass it to your Flask route as a query parameter
  fetch(`/get-date-range-data?from=${fromDate}&to=${toDate}&categoryId=${selectedCategoryId}`)
    .then(response => response.json())
    .then(data => {
      // Assuming you have functions defined to update the charts
      createInProgressSpendingChart(data.inProgressSpending);
      createForecastSpendingChart(data.forecastSpending);
    })
    .catch(error => {
      console.error('Error fetching data: ', error);
    });
}



// Call the change event listener on category dropdown to load initial category data
document.getElementById('category-dropdown').dispatchEvent(new Event('change'));

function fetchAllCategoriesData() {
  fetch('/get-all-categories-data')
    .then(response => response.json())
    .then(data => {
        updateValues(data.totalBudget, data.totalExpenses, data.totalRemainder);

        // Assuming the data for the charts comes in the structure needed:
        createInProgressSpendingChart({
          labels: data.inProgressSpending.labels,
          values: data.inProgressSpending.values
        });

        createForecastSpendingChart({
          labels: data.forecastSpending.labels,
          values: data.forecastSpending.values
        });
    })
    .catch(error => {
        console.error('Error fetching data for all categories: ', error);
    });
}

function fetchCategoryData(categoryId) {
  fetch('/get-category-data/' + categoryId)
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
  const inProgressSpendingChart = new Chart(ctx, {
    type: 'bar', // or 'line', 'doughnut', etc.
    data: {
      labels: data.labels, // Array of labels (e.g., dates or categories)
      datasets: [{
        label: 'In Progress Spending',
        data: data.values, // Array of values
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
  const forecastSpendingChart = new Chart(ctx, {
    type: 'line', // This might be a line chart for forecast visualisation
    data: {
      labels: data.labels, // Array of labels (e.g., future dates or periods)
      datasets: [{
        label: 'Forecast Spending',
        data: data.values, // Array of forecasted values
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        borderColor: 'rgba(255, 99, 132, 1)',
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

// Function to fetch in-progress spending data
function fetchInProgressSpendingData(fromDate, toDate, selectedCategoryId) {
  // Prepare the payload with the date range and category ID
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
    createInProgressSpendingChart({
      labels: data.labels,
      values: data.values
    });
  })
  .catch(error => {
    console.error('Error fetching in-progress spending data: ', error);
  });
}

// Function to fetch forecast spending data
function fetchForecastSpendingData(fromDate, toDate, selectedCategoryId) {
  // Prepare the payload with the date range and category ID
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
    createForecastSpendingChart({
      labels: data.labels,
      values: data.values
    });
  })
  .catch(error => {
    console.error('Error fetching forecast spending data: ', error);
  });
}

