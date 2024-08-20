$(document).ready(function() {
    var ctx = $('#temperatureChart')[0].getContext('2d');
    var temperatureChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],  // Les labels des axes X (ex: heures, jours, etc.)
            datasets: [{
                label: 'Température',
                data: [],   // Les données de température
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                fill: true
            }]
        },
        options: {
            scales: {
                x: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Heure'
                    }
                },
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Température (°C)'
                    }
                }
            }
        }
    });

    function fetchData() {
        $.ajax({
            url: "{% url 'get_data' %}",  // Assure-toi que cette URL est correcte
            method: 'GET',
            success: function(data) {
               
                // Ajoute les nouvelles données
                var now = new Date();
                var time = now.getHours() + ":" + now.getMinutes() + ":" + now.getSeconds();
                
                temperatureChart.data.labels.push(time);
                temperatureChart.data.datasets[0].data.push(data.temperature);

                // Limite le nombre de points pour ne pas surcharger le graphique
                if (temperatureChart.data.labels.length > 10) {
                    temperatureChart.data.labels.shift();
                    temperatureChart.data.datasets[0].data.shift();
                }
                $('#temperature').text(data.temperature + '°C');//lecture temperature
                $('#humidity').text(data.humidity + '%');//lecture humidité
                temperatureChart.update();
            },
            error: function() {
                console.log('Erreur lors de la récupération des données');
            }
        });
    }

    // Appel initial pour obtenir les données immédiatement
    fetchData();

    // Appel périodique pour mettre à jour les données
    setInterval(fetchData, 2000); // Met à jour toutes les 5 secondes
});