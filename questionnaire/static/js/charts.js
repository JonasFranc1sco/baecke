document.addEventListener('DOMContentLoaded', function () {
    const data = window.chartData;
    
    if (!data) return;


    const labelsSexFormat = data.labelsSexRaw.map(label => {
        if (label === 'ML') return 'Masculino';
        if (label === 'FM') return 'Feminino';
        return 'Outro/Não informado';
    });

    const ctxMedia = document.getElementById('mediaChart');
    if (ctxMedia) {
        new Chart(ctxMedia.getContext('2d'), {
            type: 'bar',
            data: {
                labels: ['Escore Médio Geral'],
                datasets: [{
                    label: 'Média de todos os usuários',
                    data: [data.mediaTotal],
                    backgroundColor: 'rgba(79, 70, 229, 0.7)', // Cor primária (Indigo)
                    borderColor: 'rgba(79, 70, 229, 1)',
                    borderWidth: 1,
                    borderRadius: 8
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 15 // Ajuste esse valor dependendo do máximo possível no score de Baecke
                    }
                },
                plugins: {
                    legend: {
                        display: false // Oculta a legenda já que é só uma barra
                    }
                }
            }
        });
    }

    // 4. Renderização do Gráfico de Distribuição por Gênero (Rosca/Doughnut)
    const ctxSex = document.getElementById('genderChart');
    if (ctxSex) {
        new Chart(ctxSex.getContext('2d'), {
            type: 'doughnut',
            data: {
                labels: labelsSexFormat,
                datasets: [{
                    data: data.valuesSex,
                    backgroundColor: [
                        'rgba(54, 162, 235, 0.8)', // Azul para Masculino
                        'rgba(255, 99, 132, 0.8)'  // Rosa para Feminino
                    ],
                    borderWidth: 0,
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: true,
                cutout: '65%',
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 20,
                            font: {
                                size: 14
                            }
                        }
                    }
                }
            }
        });
    }
});