$(document).ready(function(){
    var endpoint = 'visitor-data'
    var endpointtwo = 'user-data'
    var visitorpermonth = []
    var visitormonthnumber = []
    var visitorperyear =[]
    var visitoryearnuber =[]
    var userpermonth =[]
    var usermonthnumber =[]
    var usersperyear =[]
    var usersyearnumber =[]
    $.ajax({
        method: "GET",
        url: endpoint,
        success: function(visitor_stats){
            visitorpermonth = visitor_stats.visitorNumberMonthly
            visitormonthnumber = visitor_stats.visitorMonthNumber
            visitorperyear = visitor_stats.visitorNumberYearly
            visitoryearnuber = visitor_stats.vistorYearNumber

            console.log(visitorpermonth)
            console.log( visitormonthnumber)

            console.log(visitorperyear)
            console.log(visitoryearnuber)


            const visitorM = document.getElementById('visitorMonthly').getContext('2d');
            const visitorMonthly = new Chart(visitorM, {
            type: 'bar',
            data: {
                labels: visitormonthnumber,
                datasets: [{
                    label: 'Monthly Visitors',
                    data: visitorpermonth,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(153, 102, 255, 0.2)',
                        'rgba(255, 159, 64, 0.2)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)'
                    ],
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

            const visitorY = document.getElementById('visitorYearly').getContext('2d');
            const visitorYearly = new Chart(visitorY, {
            type: 'bar',
            data: {
                labels: visitoryearnuber,
                datasets: [{
                    label: 'Yearly Visitors',
                    data:  visitorperyear,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(153, 102, 255, 0.2)',
                        'rgba(255, 159, 64, 0.2)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)'
                    ],
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

        },
        error: function(error_visitor_stats){
            console.log("error")
            console.log(error_visitor_stats)
        }
    })
// ********************** Users Section **********************************//
    $.ajax({
        method: "GET",
        url: endpointtwo,
        success: function(user_stats){
            userpermonth = user_stats.userspermonth
            usermonthnumber = user_stats.usersmonthnumber
            usersperyear = user_stats.usersperyear
            usersyearnumber = user_stats.usersyearnumber

            console.log(userpermonth)
            console.log(usermonthnumber)

            console.log(usersperyear)
            console.log(usersyearnumber)


            const userM = document.getElementById('usersMonthly').getContext('2d');
            const usersMonthly = new Chart(userM, {
            type: 'bar',
            data: {
                labels: usermonthnumber,
                datasets: [{
                    label: 'Monthly Users',
                    data: userpermonth,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(153, 102, 255, 0.2)',
                        'rgba(255, 159, 64, 0.2)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)'
                    ],
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

            const userY = document.getElementById('usersYearly').getContext('2d');
            const usersYearly = new Chart(userY, {
            type: 'bar',
            data: {
                labels: usersyearnumber,
                datasets: [{
                    label: 'Yearly User',
                    data:  usersperyear,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(153, 102, 255, 0.2)',
                        'rgba(255, 159, 64, 0.2)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)'
                    ],
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

        },
        error: function(error_visitor_stats){
            console.log("error")
            console.log(error_visitor_stats)
        }
    })


});