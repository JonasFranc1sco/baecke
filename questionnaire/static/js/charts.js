document.addEventListener('DOMContentLoaded', function () {
    const data = window.chartData;
    
    if (!data) return;

    const labelsSexFormat = data.labelsSexRaw.map(label => {
        if (label === 'ML') return 'Masculino';
        if (label === 'FM') return 'Feminino';
        return 'Outro / Não informado';
    });

    const ctxMedia = document.getElementById('mediaChart');
    if (ctxMedia) {
        new Chart(ctxMedia.getContext('2d'), {
            type: 'bar',
            data: {
                labels: ['Escore Médio Geral'],
                datasets: [{
                    label: 'Média de todos os participantes',
                    data: [data.mediaTotal],
                    backgroundColor: 'rgba(15, 81, 50, 0.85)', // Primária #0f5132
                    borderColor: '#0f5132',
                    borderWidth: 1.5,
                    borderRadius: 10,
                    maxBarThickness: 70
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 15,
                        grid: {
                            color: 'rgba(226, 232, 240, 0.6)'
                        },
                        ticks: {
                            font: {
                                family: 'Inter',
                                size: 12
                            }
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        },
                        ticks: {
                            font: {
                                family: 'Inter',
                                size: 12
                            }
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: '#0f172a',
                        titleFont: { family: 'Inter' },
                        bodyFont: { family: 'Inter' },
                        padding: 10,
                        cornerRadius: 8
                    }
                }
            }
        });
    }

    const ctxSex = document.getElementById('genderChart');
    if (ctxSex) {
        new Chart(ctxSex.getContext('2d'), {
            type: 'doughnut',
            data: {
                labels: labelsSexFormat,
                datasets: [{
                    data: data.valuesSex,
                    backgroundColor: [
                        'rgba(15, 81, 50, 0.85)',   // Verde escuro
                        'rgba(5, 150, 105, 0.85)',  // Esmeralda
                        'rgba(148, 163, 184, 0.85)' // Slate neutro
                    ],
                    borderWidth: 2,
                    borderColor: '#ffffff',
                    hoverOffset: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                cutout: '70%',
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 16,
                            font: {
                                family: 'Inter',
                                size: 13
                            },
                            usePointStyle: true
                        }
                    },
                    tooltip: {
                        backgroundColor: '#0f172a',
                        titleFont: { family: 'Inter' },
                        bodyFont: { family: 'Inter' },
                        padding: 10,
                        cornerRadius: 8
                    }
                }
            }
        });
    }
});