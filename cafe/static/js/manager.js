
document.addEventListener('DOMContentLoaded', function() {
    fetch('/popular_items/')
    .then(response => response.json())
    .then(data => {
        const ctx = document.getElementById('popularItemsChart').getContext('2d');
        const chart = new Chart(ctx, {
            type: 'pie', 
            data: {
                labels: data.product_names,
                datasets: [{
                    label: 'Popular Items',
                    data: data.quantities,
                    backgroundColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(153, 102, 255, 1)'
                    ]
                }]
            }
        });
    });
});

document.addEventListener('DOMContentLoaded', function() {

    fetch('/sales_by_customer/')
    .then(response => response.json())
    .then(data => {
        const ctx = document.getElementById('salesByCustomerChart').getContext('2d');
        const chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.customer_numbers,
                datasets: [{
                    label: 'Sales by Customer $',
                    data: data.total_sales,
                    backgroundColor: 'rgba(255, 99, 132, 1)', 
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
    });
});




document.addEventListener('DOMContentLoaded', function() {
    fetch('/peak_business_hour/') 
    .then(response => response.json())
    .then(data => {
        const hoursData = data.peak_hour;

        const hours = hoursData.map(entry => entry.hour);
        const orderCounts = hoursData.map(entry => entry.order_count);

        const ctx = document.getElementById('peakBusinessHourChart').getContext('2d');
        const chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: hours,
                datasets: [{
                    label: 'Orders Count',
                    data: orderCounts,
                    fill: false,
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1
                }]
            },
            options: {
                scales: {
                    x: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Hour of the Day'
                        }
                    },
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Number of Orders'
                        }
                    }
                }
            }
        });
    });
});

document.addEventListener('DOMContentLoaded', function() {
    fetch('/sales_by_category/') 
    .then(response => response.json())
    .then(data => {
        const ctx = document.getElementById('salesByCategoryChart').getContext('2d');
        const chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.category_names,
                datasets: [{
                    label: 'Sales by Category',
                    data: data.total_sales,
                    backgroundColor: 'rgba(153, 102, 255, 0.2)',
                    borderColor: 'rgba(153, 102, 255, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    x: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Category Names'
                        }
                    },
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Total Sales'
                        }
                    }
                }
            }
        });
    });
});

document.addEventListener('DOMContentLoaded', function() {
    fetch('/sales_by_employee/')  
    .then(response => response.json())
    .then(data => {
        const ctx = document.getElementById('salesByEmployeeChart').getContext('2d');
        const chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.phone_numbers,
                datasets: [{
                    label: 'Sales by Employee',
                    data: data.total_sales,
                    backgroundColor: 'rgba(255, 206, 86, 0.2)',
                    borderColor: 'rgba(255, 206, 86, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    x: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Employee Phone Numbers'
                        }
                    },
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Total Sales'
                        }
                    }
                }
            }
        });
    });
});

document.addEventListener('DOMContentLoaded', function() {
    fetch('/popular_items_morning/')
    .then(response => response.json())
    .then(data => {
        const ctx = document.getElementById('popularItemsMorningChart').getContext('2d');
        const chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.product_names,
                datasets: [{
                    label: 'Popular Items in the Morning',
                    data: data.quantities,
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
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
    });
});


document.addEventListener('DOMContentLoaded', function() {
    fetch('/order_status_report/')  
    .then(response => response.json())
    .then(data => {
        const ctx = document.getElementById('orderStatusChart').getContext('2d');
        const chart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: ['Accepted', 'Refused', 'Waiting'],
                datasets: [{
                    data: [data.accepted_count, data.refused_count, data.waiting_count],
                    backgroundColor: [
                        'rgba(75, 192, 192, 0.6)',  
                        'rgba(255, 99, 132, 0.6)', 
                        'rgba(255, 205, 86, 0.6)'   
                    ]
                }]
            },
            options: {
                responsive: true,
                title: {
                    display: true,
                    text: 'Order Status Report for Today'
                }
            }
        });
    });
});

document.getElementById('datePicker').addEventListener('change', function() {
    fetchAndRenderChart(this.value);  
});

document.addEventListener('DOMContentLoaded', function() {
    fetchAndRenderChart();  
});

function fetchAndRenderChart(date) {
    let endpoint = '/top_selling_items/';
    if (date) {
        endpoint += `?date=${date}`;
    }

    fetch(endpoint)
    .then(response => response.json())
    .then(data => {
        const ctx = document.getElementById('topSellingItemsChart').getContext('2d');
    
        if (window.myChart) {
            window.myChart.destroy();
        }

        window.myChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.product_names,
                datasets: [{
                    label: 'Top Selling Items',
                    data: data.quantities,
                    backgroundColor: 'rgba(153, 102, 255, 0.2)',
                    borderColor: 'rgba(153, 102, 255, 1)',
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
    });
}

document.addEventListener('DOMContentLoaded', function() {
    fetch('/total_sales/')
    .then(response => response.json())
    .then(data => {
        const ctx = document.getElementById('totalSalesChart').getContext('2d');
        const chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Total Sales'],
                datasets: [{
                    label: 'Sales Amount',
                    data: [data.total_sales],
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
    });
});

document.addEventListener('DOMContentLoaded', function() {
    fetch('/monthly_sales/')
    .then(response => response.json())
    .then(data => {
        const ctx = document.getElementById('monthlySalesChart').getContext('2d');
        const chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.months,  
                datasets: [{
                    label: 'Monthly Sales',
                    data: data.monthly_sales,
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
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
    });
});


document.addEventListener('DOMContentLoaded', function() {
    fetch('/daily_sales/')
    .then(response => response.json())
    .then(data => {
        const ctx = document.getElementById('dailySalesChart').getContext('2d');
        const chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.days,  
                datasets: [{
                    label: 'Daily Sales',
                    data: data.daily_sales,
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
    });
});


document.addEventListener('DOMContentLoaded', function() {
    fetch('/yearly_sales/')
    .then(response => response.json())
    .then(data => {
        const ctx = document.getElementById('yearlySalesChart').getContext('2d');
        const chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.years,  
                datasets: [{
                    label: 'Yearly Sales',
                    data: data.yearly_sales,
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
    });
});
