document.addEventListener('alpine:init', () => {
    Alpine.data('typing', () => ({
        words: [],
        handled: [],
        spaces: {},

        currentWord: '',
        currentType: '', // Le mot en cours de frappe
        hasStarted: false,
        hasFinished: false,
        isLoading: false,
        durationInSecond: 30,
        remainingTime: 30,
        timeInS: 0,
        finalScore: 0,


        getWords() {
            this.isLoading = true;
            fetch('/api/words/')
                .then(response => response.json())
                .then(data => {
                    this.words = data
                    this.currentWord = this.words.shift()
                    this.isLoading = false;
                })
        },

        sendScore() {
            this.isLoading = true;
            fetch('/api/score/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    score: this.finalScore
                })
            })
            .then(response => this.isLoading = false)
        },

        validateWord() {
            if (this.currentWord === this.currentType) {
                this.handled.push({
                    word: this.currentType,
                    success: true
                })

            } else {
                this.handled.push({
                    word: this.currentWord,
                    success: false
                })

            }

            word = this.words.shift()
            this.currentWord = word
            this.currentType = ''

            if (this.words.length === 0) {
                this.handleFinish()
            }


        },

        handleTyping(event) {
            // A chaque fois qu'une touche est pressée, on met à jour le mot en cours
            this.spaces[this.timeInS] = this.spaces[this.timeInS] ? this.spaces[this.timeInS] + 1 : 1
            if (!this.hasStarted) {
                this.hasStarted = true
                this.startTimer();
            }

            this.currentType = event.target.value
            if (this.currentWord === this.currentType || event.data === ' ') {
                this.validateWord()
            }


        },

        startTimer() {
            this.remainingTime = this.durationInSecond;
            const interval = setInterval(() => {
                this.remainingTime--;
                this.timeInS++;
                if (this.remainingTime <= 0) {
                    clearInterval(interval);
                    this.handleFinish();
                }
            }, 1000);
        },

        calculateScore() {
            // Calculer le score du joueur
            foundWords = this.handled.filter(h => h.success).length
            this.finalScore = (foundWords * 60) / this.durationInSecond
        },

        handleFinish() {
            // Sera appelé lorsque la partie sera terminée
            console.log('Partie terminée');
            this.hasFinished = true;
            this.calculateScore();
            this.sendScore();
            this.ensureChartContainerExists();
            console.log(this.spaces);
        },

        ensureChartContainerExists() {
            const checkExist = setInterval(() => {
                if (document.querySelector("#chart")) {
                    clearInterval(checkExist);
                    this.renderChart();
                }
            }, 100); // Vérifiez toutes les 100ms si l'élément existe
        },

        renderChart() {
            // Préparer les données pour le graphique
            const seriesData = [];
            for (let i = 0; i <= this.durationInSecond; i++) {
                seriesData.push(this.spaces[i] || 0);
            }

            var options = {
                series: [{
                    name: "Vitesse de frappe",
                    data: seriesData
                }],
                chart: {
                    type: 'area',
                    height: 350,
                    zoom: {
                        enabled: false
                    }
                },
                dataLabels: {
                    enabled: false
                },
                stroke: {
                    curve: 'smooth'
                },
                title: {
                    text: 'Vitesse de frappe',
                    align: 'left'
                },
                xaxis: {
                    categories: [...Array(this.durationInSecond + 1).keys()],
                    title: {
                        text: 'Temps (seconde)'
                    }
                },
                yaxis: {
                    title: {
                        text: 'Nb de charactères tapés'
                    }
                }
            };

            var chart = new ApexCharts(document.querySelector("#chart"), options);
            chart.render();
        },

        init() {
            this.getWords()
        }
    }))
})