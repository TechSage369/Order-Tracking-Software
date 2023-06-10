const dailyChart = document.getElementById('dailyChart');

new Chart(dailyChart, {
  type: 'line',
  data: {
    labels: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '25', '26', '27', '28', '29', '30', '31'],
    datasets: [{
      width: '100%',
      label: 'Day Income',
      title: 'Daily',
      // just malipulate the data nothing else....

      data: [4, 3, 2, 5, 1],

      borderWidth: 1,
      customCanvasBackgroundColor: {
        color: 'lightGreen',
      }


    }]
  },
  options: {
    scales: {
      y: {
        beginAtZero: false
      }
    }
  }
});
const weeklyChart = document.getElementById('weeklyChart');

new Chart(weeklyChart, {
  type: 'bar',
  data: {
    labels: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
    datasets: [{
      label: 'Weekly Income',
      title: 'Daily',
      // just malipulate the data nothing else....
      data: [12, 19, 3, 5, 7, 3, 4],
      borderWidth: 1,
      customCanvasBackgroundColor: {
        color: 'lightGreen',
      }


    }]
  },
  options: {
    scales: {
      y: {
        beginAtZero: false
      }
    }
  }
});
const monthlyChart = document.getElementById('monthlyChart');

new Chart(monthlyChart, {
  type: 'bar',
  data: {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    datasets: [{
      label: 'Monthly Income',
      title: 'Daily',
      // just malipulate the data nothing else....
      data: [12, 19, 3, 5, 7, 3, 4, 8, 4, 5, 8, 9],
      borderWidth: 1,


    }]
  },
  options: {
    scales: {
      y: {
        beginAtZero: false
      }
    }
  }
});
const yearlyChart = document.getElementById('yearlyChart');

new Chart(yearlyChart, {
  type: 'line',
  data: {
    labels: ['2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030'],
    datasets: [{
      label: 'Monthly Income',
      title: 'Daily',
      // just malipulate the data nothing else....
      data: [12, 19, 3, 5, 7, 3, 4, 8, 4, 5, 8, 9],
      borderWidth: 1,


    }]
  },
  options: {
    scales: {
      y: {
        beginAtZero: false
      }
    }
  }
});

