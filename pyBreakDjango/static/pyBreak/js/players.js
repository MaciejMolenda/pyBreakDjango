$(document).ready(function() {
    $('.js-example-basic-single').select2({
        placeholder: "Search for your Player",
        allowClear: true
    });
});

$(function() {
    $('.footable').footable();
});

$(function () {
    $('[data-toggle="tooltip"]').tooltip()
})

let primaryTab = document.getElementById("primarytab");
let primaryPld = primaryTab.rows[1];
let primaryWon = primaryTab.rows[2];
let primaryLost = primaryTab.rows[3];
let primaryPerc = primaryTab.rows[4];
let primaryPldTd = primaryPld.getElementsByTagName("td");
let primaryWonTd = primaryWon.getElementsByTagName("td");
let primaryLostTd = primaryLost.getElementsByTagName("td");
let primaryPercTd = primaryPerc.getElementsByTagName("td");

let compareDescDiv = document.getElementById("comparedescdiv");
let compareDesc = document.getElementById("comparedesc").getElementsByTagName("thead")[0].rows[0].getElementsByTagName("th");

let compareTabDiv = document.getElementById("comparetabdiv");
let compareTab = document.getElementById("comparetab");
let comparePld = compareTab.rows[1];
let compareWon = compareTab.rows[2];
let compareLost = compareTab.rows[3];
let comparePerc = compareTab.rows[4];
let comparePldTd = comparePld.getElementsByTagName("td");
let compareWonTd = compareWon.getElementsByTagName("td");
let compareLostTd = compareLost.getElementsByTagName("td");
let comparePercTd = comparePerc.getElementsByTagName("td");

function changeTableRow(rowToChange, dataToPut) {

    for (let i = 0; i < rowToChange.length; i++) {
            rowToChange[i].textContent = String(dataToPut[i]);
    }
};

function fillTableData(lost_array, perc_array, data_array) {

    for (let i = 0; i < data_array[0].length; i++) {
        lost_array.push(data_array[0][i] - data_array[1][i]);
    };

    for (let i = 0; i < data_array[0].length; i++) {
        if(data_array[0][i] != 0) {
            perc_array.push((data_array[1][i] / data_array[0][i] * 100).toFixed(1));
        }
        else {
            perc_array.push('-');
        }
    };
};            

let player_perc = [];
for (let i = 0; i < primaryPldTd.length; i++) {
    if(primaryPldTd[i].textContent != '0') {
        player_perc.push((primaryWonTd[i].textContent / primaryPldTd[i].textContent * 100).toFixed(1));
    }
    else {
        player_perc.push('-');
    }
};

changeTableRow(primaryPercTd, player_perc);

var servaccChart = document.getElementById('servaccChart').getContext('2d');
var serviceAccuracy = new Chart(servaccChart, {
type: 'horizontalBar',
data: {
    labels: ['First serve accuracy', 'First serve % pts', 'Second serve % pts', 'Breakpoints saved ratio %'],
    datasets: [{
        backgroundColor: ['#706fd3', '#ef5777', '#ff5e57', '#0be881'],
        hoverBackgroundColor: ['#474787', '#f53b57', '#ff3f34', '#05c46b'],
        label: playerName,
        data: [playerFirstSrvAcc, playerFirstSrvPts, playerSecSrvPts, playerBpsSaved]}],
},
options: {
    scales: {
        xAxes: [{
            ticks: {
                min: 0,
                beginAtZero: true,
                reverse: true
                },
            }]
        },
    legend: {
        display: false
        }
    }
});

var rettbChart = document.getElementById('rettbChart').getContext('2d');
var returnTbs = new Chart(rettbChart, {
type: 'horizontalBar',
data: {
    labels: ['Tiebreak wins ratio %', 'Return 1st serve % pts', 'Return 2nd serve % pts', 'Breakpoints converted ratio %'],
    datasets: [{
        backgroundColor: ['rgba(153,204,255,1)', '#ffc048', 'rgba(255,204,0,1)', '#c44569'],
        hoverBackgroundColor: ['rgba(153,153,255,1)', '#ffa801', 'rgba(255,153,0,1)', 'purple'],
        label: playerName,
        data: [playerTbWonPerc, playerFirstRetPts, playerSecRetPts, playerBpsConv]}],
},
options: {
    scales: {
        xAxes: [{
            ticks: {
                min: 0
                }
            }]
        },
    legend: {
        display: false
        }
    }
});


var numbersPolar = new Chart(document.getElementById("numbersPolar").getContext("2d"))
var numericStats = new Chart(numbersPolar, {
type: 'polarArea',
data: {
    labels: ['Aces', 'Double Faults', 'BPs to save', 'BPs created'],
    datasets: [{
        label: 'Numeric stats',
        backgroundColor: ["#27ae60", "#c0392b", "#f39c12", "#6d214f"],
        data: [playerAces, playerDFs, playerBPdef, playerBPcre],
    }]
},
options: {
    responsive: true,
    maintainAspectRatio: false,
    layout: {
        padding: {
            left: 0,
            right: 0,
            top: 0,
            bottom: 0
            }
        },
    },
});

var spiderChart = new Chart(document.getElementById("spider").getContext("2d"))
var skills = new Chart(spiderChart, {
type: 'radar',
data: {
    labels: ['1st Srv Acc %','1st Srv %','2nd Srv %', 'BPs save %','Srv Games %',
    'Ret 1st %','Ret 2nd %', 'BPs convert %', 'Ret Games %','Tiebreak %'],
    datasets: [{
        label: playerName,
        backgroundColor: "rgba(3, 88, 106, 0.2)",
        borderColor: "rgba(3, 88, 106, 0.80)",
        pointBackgroundColor: "rgba(3, 88, 106 ,0.6)",
        pointBorderColor: "rgba(3, 88, 106 ,0.6)",
        pointHoverBackgroundColor: "rgba(3, 88, 106, 0.8)",
        pointHoverBorderColor: "rgba(220, 220, 220, 1)",
        pointRadius: 4,
        pointHoverRadius: 8,
        borderRadius: 15,
        lineWidth: 8,
        borderCapStyle: 'round',
        data: [playerFirstSrvAcc, playerFirstSrvPts, playerSecSrvPts, playerBpsSaved, playerSrvGames, playerFirstRetPts,
                    playerSecRetPts, playerBpsConv, playerRetGames, playerTbWonPerc],
    }]
},
options: {
    responsive: true,
    maintainAspectRatio: false,
    layout: {
        padding: {
            left: 0,
            right: 0,
            top: 0,
            bottom: 0
        }
    },
    legend: { display: true },
    tooltips: {
        callbacks: {
            label: function(tooltipItem, data) {
            return data.datasets[tooltipItem.datasetIndex].label + ": " + tooltipItem.yLabel;
            }
        }
    },

    scale: {
        ticks: {
            max: 100, min: 0, stepSize: 20
        },
        gridLines: {
            color: '#666666',
            lineWidth: 0.6,
        },

        angleLines: {
            display: false
            }
        }
    },
});

var oddsChart = new Chart(document.getElementById("oddsChart").getContext("2d"))
var odds = new Chart(oddsChart, {
    type: 'bar',
    data: {
    labels: ["Surety", "Favorite", "Slight favorite", "Contender", "Outsider", "Underdog"],
    datasets: [
        {
        backgroundColor: ["#44B91C", "#8e5ea2","#3cba9f","#e8c3b9","#c45850", '#7f8c8d'],
        data: [],
        }
    ]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
        yAxes: [{
            ticks: {
                max: 100,
                min: 0,
                stepSize: 20
                }
            }]
        },
        legend: { display: false },
    }
});

let btnOvrMain = document.querySelector('#btn-ovr');
let btnOvrOvr = document.querySelector('#btn-ovr-ovr');
let btnOvrYear = document.querySelector('#btn-ovr-year');
let btnOvrCur = document.querySelector('#btn-ovr-cur');
let btnHardMain = document.querySelector('#btn-hard');
let btnHardOvr = document.querySelector('#btn-hard-ovr');
let btnHardYear = document.querySelector('#btn-hard-year');
let btnHardCur = document.querySelector('#btn-hard-cur');
let btnClayMain = document.querySelector('#btn-clay');
let btnClayOvr = document.querySelector('#btn-clay-ovr');
let btnClayYear = document.querySelector('#btn-clay-year');
let btnClayCur = document.querySelector('#btn-clay-cur');

let comparePlayerVar = '';
let currentScenario = ovr ;

odds.data.datasets[0] = {
label: playerName,
backgroundColor: ["#44B91C", "#8e5ea2","#3cba9f","#e8c3b9","#c45850", '#7f8c8d'],
data: [suretyPerc, favPerc, sliFavPerc, contPerc, outPerc, undPerc]};
odds.update();

allPlayers = [];
ovr.forEach(function(man) {
        allPlayers.push(String(man.pk));
    });

function fixDecimal(source, index) {
    let obj = source[index]['fields'];
    for (let property in obj) {
        if ((obj[property] != null) & (typeof(obj[property]) == 'number') & (Number.isInteger(obj[property]) == false)) {
            obj[property] = obj[property].toFixed(1);
        };
    };
};

function visualizePlayer(element, scenario, tekst, backcolor) {
    element.addEventListener("click", function (e) {
        document.getElementById('scenario-info').textContent = tekst;
        document.getElementById('scenario-header').style.backgroundColor = backcolor;
        document.getElementById('scenario-info').style.backgroundColor = backcolor;
        currentScenario = scenario;
        let playersList = [];
        scenario.forEach(function(man) {
            playersList.push(String(man.pk));
        });

        let playerIndex = playersList.indexOf(playerID);

        if(playerIndex > -1) {

            fixDecimal(scenario, playerIndex);

            var primaryPlayerData = [
                [scenario[playerIndex].fields['Matches_played'], scenario[playerIndex].fields['Tiebreak_played'], 
                scenario[playerIndex].fields['Surety_played'], scenario[playerIndex].fields['Favorite_played'],
                scenario[playerIndex].fields['Slightfav_played'], scenario[playerIndex].fields['Slightunder_played'], 
                scenario[playerIndex].fields['Under_played'], scenario[playerIndex].fields['Underdog_played']],

                [scenario[playerIndex].fields['Matches_won'], scenario[playerIndex].fields['Tiebreak_won'], 
                scenario[playerIndex].fields['Surety_won'], scenario[playerIndex].fields['Favorite_won'],
                scenario[playerIndex].fields['Slightfav_won'], scenario[playerIndex].fields['Slightunder_won'], 
                scenario[playerIndex].fields['Under_won'], scenario[playerIndex].fields['Underdog_won']]
            ];

            let primaryLostArr = [];
            let primaryPercArr = [];

            fillTableData(primaryLostArr, primaryPercArr, primaryPlayerData);
            
            changeTableRow(primaryPldTd, primaryPlayerData[0]);
            changeTableRow(primaryWonTd, primaryPlayerData[1]);
            changeTableRow(primaryLostTd, primaryLostArr);
            changeTableRow(primaryPercTd, primaryPercArr);

            serviceAccuracy.data.datasets[0].data = [scenario[playerIndex].fields['First_serve_accuracy'], scenario[playerIndex].fields['First_serve_points'],
                scenario[playerIndex].fields['Second_serve_points'], scenario[playerIndex].fields['Breakpoints_saved_ratio']];
            serviceAccuracy.update();

            returnTbs.data.datasets[0].data = [scenario[playerIndex].fields['Tiebreak_won_perc'], scenario[playerIndex].fields['Return_1st_serve_points'],
                scenario[playerIndex].fields['Return_2nd_serve_points'], scenario[playerIndex].fields['Breakpoints_converted_ratio']];
            returnTbs.update();
            
            skills.data.datasets[0].data = [scenario[playerIndex].fields['First_serve_accuracy'], scenario[playerIndex].fields['First_serve_points'], scenario[playerIndex].fields['Second_serve_points'],
            scenario[playerIndex].fields['Breakpoints_saved_ratio'], scenario[playerIndex].fields['Service_games_won_ratio'], scenario[playerIndex].fields['Return_1st_serve_points'],
            scenario[playerIndex].fields['Return_2nd_serve_points'], scenario[playerIndex].fields['Breakpoints_converted_ratio'], scenario[playerIndex].fields['Return_games_won_ratio'], 
            scenario[playerIndex].fields['Tiebreak_won_perc']];
            skills.update();

            if(numericStats.data.datasets[0].data.length <= 4) {
                numericStats.data.datasets[0].data = [scenario[playerIndex].fields['Aces_AVG'], scenario[playerIndex].fields['DoubleFaults_AVG'],
                scenario[playerIndex].fields['Breakpoints_to_defend_per_set'], scenario[playerIndex].fields['Breakpoints_created_per_set']];
                numericStats.update();
                }

            else {
                numericStatsArray = numericStats.data.datasets[0].data[0] = String(scenario[playerIndex].fields['Aces_AVG']);
                numericStatsArray = numericStats.data.datasets[0].data[2] = String(scenario[playerIndex].fields['DoubleFaults_AVG']);
                numericStatsArray = numericStats.data.datasets[0].data[4] = String(scenario[playerIndex].fields['Breakpoints_to_defend_per_set']);
                numericStatsArray = numericStats.data.datasets[0].data[6] = String(scenario[playerIndex].fields['Breakpoints_created_per_set']);
                numericStats.update();
                }

            odds.data.datasets.pop();
            odds.data.datasets[0] = {
                label: scenario[playerIndex].fields['Name'],
                backgroundColor: ["#44B91C", "#8e5ea2","#3cba9f","#e8c3b9","#c45850", '#7f8c8d'],
                data: [
                (scenario[playerIndex].fields['Surety_won'] / scenario[playerIndex].fields['Surety_played'] * 100).toFixed(1),
                (scenario[playerIndex].fields['Favorite_won'] / scenario[playerIndex].fields['Favorite_played'] * 100).toFixed(1),
                (scenario[playerIndex].fields['Slightfav_won'] / scenario[playerIndex].fields['Slightfav_played'] * 100).toFixed(1),
                (scenario[playerIndex].fields['Slightunder_won'] / scenario[playerIndex].fields['Slightunder_played'] * 100).toFixed(1),
                (scenario[playerIndex].fields['Under_won'] / scenario[playerIndex].fields['Under_played'] * 100).toFixed(1),
                (scenario[playerIndex].fields['Underdog_won'] / scenario[playerIndex].fields['Underdog_played'] * 100).toFixed(1)]};

            odds.update();
            }

        else {

            changeTableRow(primaryPldTd, new Array(8).fill('0'));
            changeTableRow(primaryWonTd, new Array(8).fill('0'));
            changeTableRow(primaryLostTd, new Array(8).fill('0'));
            changeTableRow(primaryPercTd, new Array(8).fill('-'));

            serviceAccuracy.data.datasets[0].data = new Array(4).fill(null);
            serviceAccuracy.update();

            returnTbs.data.datasets[0].data = new Array(4).fill(null);
            returnTbs.update();

            skills.data.datasets[0].data = new Array(10).fill(null);
            skills.update();


            if(numericStats.data.datasets[0].data.length <= 4) {
                numericStats.data.datasets[0].data = new Array(4).fill(null);
                numericStats.update();
                }

            else {
                numericStats.data.datasets[0].data[0] = null;
                numericStats.data.datasets[0].data[2] = null;
                numericStats.data.datasets[0].data[4] = null;
                numericStats.data.datasets[0].data[6] = null;
                numericStats.update();
                };
            
            odds.data.datasets.pop();
            odds.data.datasets[0] = {
                label: playerName,
                backgroundColor: ["#44B91C", "#8e5ea2","#3cba9f","#e8c3b9","#c45850", '#7f8c8d'],
                data: []};

            odds.update();

            };

        if(comparePlayerVar != '') {
            comparePlayerIndex = playersList.indexOf(comparePlayerVar);
            if(comparePlayerIndex > -1) {
                // console.log(currentScenario[comparePlayerIndex].fields['Name']);
                // console.log(currentScenario[comparePlayerIndex].fields['Rank']);
                fixDecimal(currentScenario, comparePlayerIndex);
                
                var comparePlayerData = [
                        [currentScenario[comparePlayerIndex].fields['Matches_played'], currentScenario[comparePlayerIndex].fields['Tiebreak_played'], 
                        currentScenario[comparePlayerIndex].fields['Surety_played'], currentScenario[comparePlayerIndex].fields['Favorite_played'],
                        currentScenario[comparePlayerIndex].fields['Slightfav_played'], currentScenario[comparePlayerIndex].fields['Slightunder_played'], 
                        currentScenario[comparePlayerIndex].fields['Under_played'], currentScenario[comparePlayerIndex].fields['Underdog_played']],

                        [currentScenario[comparePlayerIndex].fields['Matches_won'], currentScenario[comparePlayerIndex].fields['Tiebreak_won'], 
                        currentScenario[comparePlayerIndex].fields['Surety_won'], currentScenario[comparePlayerIndex].fields['Favorite_won'],
                        currentScenario[comparePlayerIndex].fields['Slightfav_won'], currentScenario[comparePlayerIndex].fields['Slightunder_won'], 
                        currentScenario[comparePlayerIndex].fields['Under_won'], currentScenario[comparePlayerIndex].fields['Underdog_won']]
                    ];

                let compareLostArr = [];
                let comparePercArr = [];

                fillTableData(compareLostArr, comparePercArr, comparePlayerData);
                
                changeTableRow(comparePldTd, comparePlayerData[0]);
                changeTableRow(compareWonTd, comparePlayerData[1]);
                changeTableRow(compareLostTd, compareLostArr);
                changeTableRow(comparePercTd, comparePercArr);

                // console.log('ten drugi: ', comparePlayerVar);

                serviceAccuracy.data.datasets[1].data = [scenario[comparePlayerIndex].fields['First_serve_accuracy'], scenario[comparePlayerIndex].fields['First_serve_points'],
                scenario[comparePlayerIndex].fields['Second_serve_points'], scenario[comparePlayerIndex].fields['Breakpoints_saved_ratio']];
                serviceAccuracy.update();

                returnTbs.data.datasets[1].data = [scenario[comparePlayerIndex].fields['Tiebreak_won_perc'], scenario[comparePlayerIndex].fields['Return_1st_serve_points'],
                scenario[comparePlayerIndex].fields['Return_2nd_serve_points'], scenario[comparePlayerIndex].fields['Breakpoints_converted_ratio']];
                returnTbs.update();
                
                if(numericStats.data.datasets[0].data.length <= 4) {
                    numericStats.data.datasets[0].data.splice(1, 0, String(scenario[comparePlayerIndex].fields['Aces_AVG']));
                    numericStats.data.labels.splice(1, 0, 'Aces - rival');
                    numericStats.data.datasets[0].backgroundColor.splice(1, 0, 'green');
                    numericStats.data.datasets[0].data.splice(3, 0, String(scenario[comparePlayerIndex].fields['DoubleFaults_AVG']));
                    numericStats.data.labels.splice(3, 0, 'DFs - rival');
                    numericStats.data.datasets[0].backgroundColor.splice(3, 0, 'red');
                    numericStats.data.datasets[0].data.splice(5, 0, String(scenario[comparePlayerIndex].fields['Breakpoints_to_defend_per_set']));
                    numericStats.data.labels.splice(5, 0, 'BPs to save - rival');
                    numericStats.data.datasets[0].backgroundColor.splice(5, 0, 'yellow');
                    numericStats.data.datasets[0].data.splice(7, 0, String(scenario[comparePlayerIndex].fields['Breakpoints_created_per_set']));
                    numericStats.data.labels.splice(7, 0, 'BPs created - rival');
                    numericStats.data.datasets[0].backgroundColor.splice(7, 0, 'purple');
                    numericStats.update();
                }

                else {
                    numericStats.data.datasets[0].data[1] = String(scenario[comparePlayerIndex].fields['Aces_AVG']);
                    numericStats.data.datasets[0].data[3] = String(scenario[comparePlayerIndex].fields['DoubleFaults_AVG']);
                    numericStats.data.datasets[0].data[5] = String(scenario[comparePlayerIndex].fields['Breakpoints_to_defend_per_set']);
                    numericStats.data.datasets[0].data[7] = String(scenario[comparePlayerIndex].fields['Breakpoints_created_per_set']);
                    numericStats.data.labels[1] = 'Aces - rival';
                    numericStats.data.datasets[0].backgroundColor[1] = 'green';
                    numericStats.data.labels[3] = 'DFs - rival';
                    numericStats.data.datasets[0].backgroundColor[3] = 'red';
                    numericStats.data.labels[5] = 'BPs to save - rival';
                    numericStats.data.datasets[0].backgroundColor[5] = 'yellow';
                    numericStats.data.labels[7] = 'BPs created - rival';
                    numericStats.data.datasets[0].backgroundColor[7] = 'purple';
                    numericStats.update();
                };

                skills.data.datasets[1] = {
                    label: scenario[comparePlayerIndex].fields['Name'],
                    backgroundColor: "rgba(255,51,102,0.2)",
                    borderColor: "rgba(255,51,102,0.85)",
                    pointColor: "rgba(255,51,102,0.85)",

                    pointRadius: 4,
                    pointHoverRadius: 8,
                    borderRadius: 15,
                    lineWidth: 8,
                    borderCapStyle: 'round',
                    data: [scenario[comparePlayerIndex].fields['First_serve_accuracy'], scenario[comparePlayerIndex].fields['First_serve_points'], scenario[comparePlayerIndex].fields['Second_serve_points'],
                    scenario[comparePlayerIndex].fields['Breakpoints_saved_ratio'], scenario[comparePlayerIndex].fields['Service_games_won_ratio'], scenario[comparePlayerIndex].fields['Return_1st_serve_points'],
                    scenario[comparePlayerIndex].fields['Return_2nd_serve_points'], scenario[comparePlayerIndex].fields['Breakpoints_converted_ratio'], scenario[comparePlayerIndex].fields['Return_games_won_ratio'], 
                    scenario[comparePlayerIndex].fields['Tiebreak_won_perc']]
                };
                skills.update();

                odds.data.datasets[1] = {
                    backgroundColor: ["#b8e994", "#e056fd","#74b9ff","#f8c291","#e74c3c", '#95a5a6'],
                    label: scenario[comparePlayerIndex].fields['Name'],
                    data: [
                    (scenario[comparePlayerIndex].fields['Surety_won'] / scenario[comparePlayerIndex].fields['Surety_played'] * 100).toFixed(1),
                    (scenario[comparePlayerIndex].fields['Favorite_won'] / scenario[comparePlayerIndex].fields['Favorite_played'] * 100).toFixed(1),
                    (scenario[comparePlayerIndex].fields['Slightfav_won'] / scenario[comparePlayerIndex].fields['Slightfav_played'] * 100).toFixed(1),
                    (scenario[comparePlayerIndex].fields['Slightunder_won'] / scenario[comparePlayerIndex].fields['Slightunder_played'] * 100).toFixed(1),
                    (scenario[comparePlayerIndex].fields['Under_won'] / scenario[comparePlayerIndex].fields['Under_played'] * 100).toFixed(1),
                    (scenario[comparePlayerIndex].fields['Underdog_won'] / scenario[comparePlayerIndex].fields['Underdog_played'] * 100).toFixed(1)]};

                odds.update();                        
            }

            else {

                changeTableRow(comparePldTd, new Array(8).fill('0'));
                changeTableRow(compareWonTd, new Array(8).fill('0'));
                changeTableRow(compareLostTd, new Array(8).fill('0'));
                changeTableRow(comparePercTd, new Array(8).fill('-'));

                serviceAccuracy.data.datasets[1].data = new Array(4).fill(null);
                serviceAccuracy.update();

                returnTbs.data.datasets[1].data = new Array(4).fill(null);
                returnTbs.update();

                if(numericStats.data.datasets[0].data.length <= 4) {
                    numericStats.data.datasets[0].data.splice(1, 0, null);
                    numericStats.data.datasets[0].data.splice(3, 0, null);
                    numericStats.data.datasets[0].data.splice(5, 0, null);
                    numericStats.data.datasets[0].data.splice(7, 0, null);
                    numericStats.data.labels.splice(1, 0, 'Aces - rival');
                    numericStats.data.datasets[0].backgroundColor.splice(1, 0, 'green');
                    numericStats.data.labels.splice(3, 0, 'DFs - rival');
                    numericStats.data.datasets[0].backgroundColor.splice(3, 0, 'red');
                    numericStats.data.labels.splice(5, 0, 'BPs to save - rival');
                    numericStats.data.datasets[0].backgroundColor.splice(5, 0, 'yellow');
                    numericStats.data.labels.splice(7, 0, 'BPs created - rival');
                    numericStats.data.datasets[0].backgroundColor.splice(7, 0, 'purple');
                    numericStats.update();
                }

                else {
                    numericStats.data.datasets[0].data[1] = null;
                    numericStats.data.datasets[0].data[3] = null;
                    numericStats.data.datasets[0].data[5] = null;
                    numericStats.data.datasets[0].data[7] = null;
                    numericStats.data.labels[1] = 'Aces - rival';
                    numericStats.data.datasets[0].backgroundColor[1] = 'green';
                    numericStats.data.labels[3] = 'DFs - rival';
                    numericStats.data.datasets[0].backgroundColor[3] = 'red';
                    numericStats.data.labels[5] = 'BPs to save - rival';
                    numericStats.data.datasets[0].backgroundColor[5] = 'yellow';
                    numericStats.data.labels[7] = 'BPs created - rival';
                    numericStats.data.datasets[0].backgroundColor[7] = 'purple';
                    numericStats.update();
                }

                skills.data.datasets[1] = {
                    label: ovr[allPlayers.indexOf(comparePlayerVar)].fields['Name'],
                    backgroundColor: "rgba(255, 51, 102, 0.2)",
                    borderColor: "rgba(255, 51, 102, 0.85)",
                    pointBackgroundColor: "rgba(255, 51, 102, 0.85)",
                    pointBorderColor: "rgba(255, 51, 102, 0.85)",
                    pointHoverBackgroundColor: "rgba(255, 51, 102, 0.8)",
                    pointHoverBorderColor: "rgba(255, 51, 102, 1)",
                    pointRadius: 4,
                    pointHoverRadius: 8,
                    borderRadius: 15,
                    lineWidth: 8,
                    borderCapStyle: 'round',
                    data: [new Array(10).fill(null)]
                };
                skills.update();

                odds.data.datasets[1] = {
                    backgroundColor: ["#b8e994", "#e056fd","#74b9ff","#f8c291","#e74c3c", '#95a5a6'],
                    label: ovr[allPlayers.indexOf(comparePlayerVar)].fields['Name'],
                    data: []};
                odds.update(); 
            }
        }

        });
    };

function delCompare(del) {
    if (del) {
        del.addEventListener("click", function (e) {
            document.getElementById('del-test').style.display="none";
            comparePlayerVar = '';
            serviceSet = serviceAccuracy.data.datasets;
            returnSet = returnTbs.data.datasets;
            skillsSet = skills.data.datasets;
            oddsSet = odds.data.datasets;
            numericStatsArray = numericStats.data.datasets[0].data
            numericStatsLabels = numericStats.data.labels;
            numericStatsColors = numericStats.data.datasets[0].backgroundColor;

            if (serviceSet.length > 1) {

                compareTabDiv.style.display = "none";
                compareDescDiv.style.display = "none";
                serviceSet.pop();
                serviceAccuracy.update();

                returnSet.pop();
                returnTbs.update();

                skillsSet.pop();
                skills.update();

                oddsSet.pop();
                odds.update();

                numericStatsArray.splice(7, 1);
                numericStatsArray.splice(5, 1);
                numericStatsArray.splice(3, 1);
                numericStatsArray.splice(1, 1);
                numericStatsLabels.splice(7, 1);
                numericStatsLabels.splice(5, 1);
                numericStatsLabels.splice(3, 1);
                numericStatsLabels.splice(1, 1);
                numericStatsColors.splice(7, 1);
                numericStatsColors.splice(5, 1);
                numericStatsColors.splice(3, 1);
                numericStatsColors.splice(1, 1);
                numericStats.update();

            };
        });
    };
};

delCompare(document.querySelector('#del-test'));

let selectRecognition = {};

for (let i = 0; i < ovr.length; i++) {
    selectRecognition['#' + ovr[i]['fields']['Rank'] + ' ' + ovr[i]['fields']['Name']] = [ovr[i]['pk'], ovr[i]['fields']['Name']];
};

$('.js-example-basic-single').on('select2:select', function (e) {
    let selectValue = e.params.data['text'];
});

function comparePlayer() {
    $('.js-example-basic-single').on('select2:select', function (e) {
        document.getElementById('del-test').style.display = 'block';
        let selectValue = e.params.data['text'];

        serviceSet = serviceAccuracy.data.datasets;
        returnSet = returnTbs.data.datasets;
        skillsSet = skills.data.datasets;
        numericStatsArray = numericStats.data.datasets[0].data
        numericStatsLabels = numericStats.data.labels;
        numericStatsColors = numericStats.data.datasets[0].backgroundColor;

        let compareName = selectRecognition[selectValue][0];
        comparePlayerVar = compareName;
        let playersList = [];
        currentScenario.forEach(function(man) {
            playersList.push(String(man.pk));
        });

        let comparePlayerIndex = playersList.indexOf(compareName);

        if(comparePlayerIndex > -1) {

            fixDecimal(currentScenario, comparePlayerIndex);

            var comparePlayerData = [
                [currentScenario[comparePlayerIndex].fields['Matches_played'], currentScenario[comparePlayerIndex].fields['Tiebreak_played'], 
                currentScenario[comparePlayerIndex].fields['Surety_played'], currentScenario[comparePlayerIndex].fields['Favorite_played'],
                currentScenario[comparePlayerIndex].fields['Slightfav_played'], currentScenario[comparePlayerIndex].fields['Slightunder_played'], 
                currentScenario[comparePlayerIndex].fields['Under_played'], currentScenario[comparePlayerIndex].fields['Underdog_played']],

                [currentScenario[comparePlayerIndex].fields['Matches_won'], currentScenario[comparePlayerIndex].fields['Tiebreak_won'], 
                currentScenario[comparePlayerIndex].fields['Surety_won'], currentScenario[comparePlayerIndex].fields['Favorite_won'],
                currentScenario[comparePlayerIndex].fields['Slightfav_won'], currentScenario[comparePlayerIndex].fields['Slightunder_won'], 
                currentScenario[comparePlayerIndex].fields['Under_won'], currentScenario[comparePlayerIndex].fields['Underdog_won']]
            ];

            let compareLostArr = [];
            let comparePercArr = [];

            fillTableData(compareLostArr, comparePercArr, comparePlayerData);
            
            changeTableRow(comparePldTd, comparePlayerData[0]);
            changeTableRow(compareWonTd, comparePlayerData[1]);
            changeTableRow(compareLostTd, compareLostArr);
            changeTableRow(comparePercTd, comparePercArr);

            compareDesc[0].textContent = currentScenario[comparePlayerIndex].fields['Name'];
            compareDesc[1].textContent = "Rank: " + String(currentScenario[comparePlayerIndex].fields['Rank']);

            compareTabDiv.style.display = "inline";
            compareDescDiv.style.display = "inline";

            if (serviceSet.length == 1) {

                serviceSet.push({
                    backgroundColor: ['#778ca3', '#f8a5c2', '#ea8685', '#7EC66C'],
                    hoverBackgroundColor: ['#4b6584', '#f78fb3', '#e66767', '#6DA75E'],
                    label: currentScenario[comparePlayerIndex].fields['Name'],
                    data: [currentScenario[comparePlayerIndex].fields['First_serve_accuracy'], currentScenario[comparePlayerIndex].fields['First_serve_points'],
                    currentScenario[comparePlayerIndex].fields['Second_serve_points'], currentScenario[comparePlayerIndex].fields['Breakpoints_saved_ratio']]});
                serviceAccuracy.update();

                returnSet.push({
                    backgroundColor: ['#596275', '#e77f67', '#e15f41', '#a55eea'],
                    hoverBackgroundColor: ['#303952', '#cf6a87', '#c44569', '#8854d0'],
                    label: currentScenario[comparePlayerIndex].fields['Name'],
                    data: [currentScenario[comparePlayerIndex].fields['Tiebreak_won_perc'], currentScenario[comparePlayerIndex].fields['Return_1st_serve_points'],
                    currentScenario[comparePlayerIndex].fields['Return_2nd_serve_points'], currentScenario[comparePlayerIndex].fields['Breakpoints_converted_ratio']]});
                returnTbs.update();

                numericStatsArray.splice(1, 0, String(currentScenario[comparePlayerIndex].fields['Aces_AVG']));
                numericStatsArray.splice(3, 0, String(currentScenario[comparePlayerIndex].fields['DoubleFaults_AVG']));
                numericStatsArray.splice(5, 0, String(currentScenario[comparePlayerIndex].fields['Breakpoints_to_defend_per_set']));
                numericStatsArray.splice(7, 0, String(currentScenario[comparePlayerIndex].fields['Breakpoints_created_per_set']));
                numericStatsLabels.splice(1, 0, 'Aces - rival');
                numericStatsColors.splice(1, 0, 'green');
                numericStatsLabels.splice(3, 0, 'DFs - rival');
                numericStatsColors.splice(3, 0, 'red');
                numericStatsLabels.splice(5, 0, 'BPs to save - rival');
                numericStatsColors.splice(5, 0, 'yellow');
                numericStatsLabels.splice(7, 0, 'BPs created - rival');
                numericStatsColors.splice(7, 0, 'purple');
                numericStats.update();

                skillsSet.push({
                    label: currentScenario[comparePlayerIndex].fields['Name'],
                    backgroundColor: "rgba(255, 51, 102, 0.2)",
                    borderColor: "rgba(255, 51, 102, 0.85)",
                    pointBackgroundColor: "rgba(255, 51, 102, 0.85)",
                    pointBorderColor: "rgba(255, 51, 102, 0.85)",
                    pointHoverBackgroundColor: "rgba(255, 51, 102, 0.8)",
                    pointHoverBorderColor: "rgba(255, 51, 102, 1)",
                    pointRadius: 4,
                    pointHoverRadius: 8,
                    borderRadius: 15,
                    lineWidth: 8,
                    borderCapStyle: 'round',
                    data: [currentScenario[comparePlayerIndex].fields['First_serve_accuracy'], currentScenario[comparePlayerIndex].fields['First_serve_points'], currentScenario[comparePlayerIndex].fields['Second_serve_points'],
                    currentScenario[comparePlayerIndex].fields['Breakpoints_saved_ratio'], currentScenario[comparePlayerIndex].fields['Service_games_won_ratio'], currentScenario[comparePlayerIndex].fields['Return_1st_serve_points'],
                    currentScenario[comparePlayerIndex].fields['Return_2nd_serve_points'], currentScenario[comparePlayerIndex].fields['Breakpoints_converted_ratio'], currentScenario[comparePlayerIndex].fields['Return_games_won_ratio'], 
                    currentScenario[comparePlayerIndex].fields['Tiebreak_won_perc']]
                });
                skills.update();
                
                odds.data.datasets.push({
                backgroundColor: ["#b8e994", "#e056fd","#74b9ff","#f8c291","#e74c3c", '#95a5a6'],
                label: currentScenario[comparePlayerIndex].fields['Name'],
                data: [
                (currentScenario[comparePlayerIndex].fields['Surety_won'] / currentScenario[comparePlayerIndex].fields['Surety_played'] * 100).toFixed(1),
                (currentScenario[comparePlayerIndex].fields['Favorite_won'] / currentScenario[comparePlayerIndex].fields['Favorite_played'] * 100).toFixed(1),
                (currentScenario[comparePlayerIndex].fields['Slightfav_won'] / currentScenario[comparePlayerIndex].fields['Slightfav_played'] * 100).toFixed(1),
                (currentScenario[comparePlayerIndex].fields['Slightunder_won'] / currentScenario[comparePlayerIndex].fields['Slightunder_played'] * 100).toFixed(1),
                (currentScenario[comparePlayerIndex].fields['Under_won'] / currentScenario[comparePlayerIndex].fields['Under_played'] * 100).toFixed(1),
                (currentScenario[comparePlayerIndex].fields['Underdog_won'] / currentScenario[comparePlayerIndex].fields['Underdog_played'] * 100).toFixed(1)]});

                odds.update();

            }

            else if (serviceSet.length > 1) {

                serviceSet.pop();
                serviceSet.push({
                    backgroundColor: ['#596275', '#e77f67', '#e15f41', '#8ABE7D'],
                    hoverBackgroundColor: ['#303952', '#cf6a87', '#c44569', '#74A069'],
                    label: currentScenario[comparePlayerIndex].fields['Name'],
                    data: [currentScenario[comparePlayerIndex].fields['First_serve_accuracy'], currentScenario[comparePlayerIndex].fields['First_serve_points'],
                    currentScenario[comparePlayerIndex].fields['Second_serve_points'], currentScenario[comparePlayerIndex].fields['Breakpoints_saved_ratio']]});
                serviceAccuracy.update();
                };

                returnSet.pop();
                returnSet.push({
                    backgroundColor: ['#596275', '#e77f67', '#e15f41', '#a55eea'],
                    hoverBackgroundColor: ['#303952', '#cf6a87', '#c44569', '#8854d0'],
                    label: currentScenario[comparePlayerIndex].fields['Name'],
                    data: [currentScenario[comparePlayerIndex].fields['Tiebreak_won_perc'], currentScenario[comparePlayerIndex].fields['Return_1st_serve_points'],
                    currentScenario[comparePlayerIndex].fields['Return_2nd_serve_points'], currentScenario[comparePlayerIndex].fields['Breakpoints_converted_ratio']]});
                returnTbs.update();

                numericStatsArray[1] = String(currentScenario[comparePlayerIndex].fields['Aces_AVG']);
                numericStatsArray[3] = String(currentScenario[comparePlayerIndex].fields['DoubleFaults_AVG']);
                numericStatsArray[5] = String(currentScenario[comparePlayerIndex].fields['Breakpoints_to_defend_per_set']);
                numericStatsArray[7] = String(currentScenario[comparePlayerIndex].fields['Breakpoints_created_per_set']);
                numericStatsLabels[1] = 'Aces - rival';
                numericStatsColors[1] = 'green';
                numericStatsLabels[3] = 'DFs - rival';
                numericStatsColors[3] = 'red';
                numericStatsLabels[5] = 'BPs to save - rival';
                numericStatsColors[5] = 'yellow';
                numericStatsLabels[7] = 'BPs created - rival';
                numericStatsColors[7] = 'purple';
                numericStats.update();

                skillsSet.pop();
                skillsSet.push({
                    label: currentScenario[comparePlayerIndex].fields['Name'],
                    backgroundColor: "rgba(255, 51, 102, 0.2)",
                    borderColor: "rgba(255, 51, 102, 0.85)",
                    pointBackgroundColor: "rgba(255, 51, 102, 0.85)",
                    pointBorderColor: "rgba(255, 51, 102, 0.85)",
                    pointHoverBackgroundColor: "rgba(255, 51, 102, 0.8)",
                    pointHoverBorderColor: "rgba(255, 51, 102, 1)",
                    pointRadius: 4,
                    pointHoverRadius: 8,
                    borderRadius: 15,
                    lineWidth: 8,
                    borderCapStyle: 'round',
                    data: [currentScenario[comparePlayerIndex].fields['First_serve_accuracy'], currentScenario[comparePlayerIndex].fields['First_serve_points'], currentScenario[comparePlayerIndex].fields['Second_serve_points'],
                    currentScenario[comparePlayerIndex].fields['Breakpoints_saved_ratio'], currentScenario[comparePlayerIndex].fields['Service_games_won_ratio'], currentScenario[comparePlayerIndex].fields['Return_1st_serve_points'],
                    currentScenario[comparePlayerIndex].fields['Return_2nd_serve_points'], currentScenario[comparePlayerIndex].fields['Breakpoints_converted_ratio'], currentScenario[comparePlayerIndex].fields['Return_games_won_ratio'], 
                    currentScenario[comparePlayerIndex].fields['Tiebreak_won_perc']]
                });
                skills.update();

                odds.data.datasets[1] = {
                backgroundColor: ["#b8e994", "#e056fd","#74b9ff","#f8c291","#e74c3c", '#95a5a6'],
                label: currentScenario[comparePlayerIndex].fields['Name'],
                data: [
                (currentScenario[comparePlayerIndex].fields['Surety_won'] / currentScenario[comparePlayerIndex].fields['Surety_played'] * 100).toFixed(1),
                (currentScenario[comparePlayerIndex].fields['Favorite_won'] / currentScenario[comparePlayerIndex].fields['Favorite_played'] * 100).toFixed(1),
                (currentScenario[comparePlayerIndex].fields['Slightfav_won'] / currentScenario[comparePlayerIndex].fields['Slightfav_played'] * 100).toFixed(1),
                (currentScenario[comparePlayerIndex].fields['Slightunder_won'] / currentScenario[comparePlayerIndex].fields['Slightunder_played'] * 100).toFixed(1),
                (currentScenario[comparePlayerIndex].fields['Under_won'] / currentScenario[comparePlayerIndex].fields['Under_played'] * 100).toFixed(1),
                (currentScenario[comparePlayerIndex].fields['Underdog_won'] / currentScenario[comparePlayerIndex].fields['Underdog_played'] * 100).toFixed(1)]};

                odds.update();
            }

        else {

            changeTableRow(comparePldTd, new Array(8).fill('0'));
            changeTableRow(compareWonTd, new Array(8).fill('0'));
            changeTableRow(compareLostTd, new Array(8).fill('0'));
            changeTableRow(comparePercTd, new Array(8).fill('-'));

            compareDesc[0].textContent = ovr[allPlayers.indexOf(comparePlayerVar)].fields['Name'];
            compareDesc[1].textContent = "Rank: " + String(ovr[allPlayers.indexOf(comparePlayerVar)].fields['Rank']);

            compareTabDiv.style.display = "inline";
            compareDescDiv.style.display = "inline";

            if (serviceSet.length == 1) {

                serviceSet.push({
                    label: selectRecognition[selectValue][1],
                    data: [new Array(4).fill(null)]});
                serviceAccuracy.update();

                returnSet.push({
                    label: selectRecognition[selectValue][1],
                    data: [new Array(4).fill(null)]});
                returnTbs.update();

                numericStatsArray.splice(1, 0, null);
                numericStatsArray.splice(3, 0, null);
                numericStatsArray.splice(5, 0, null);
                numericStatsArray.splice(7, 0, null);
                numericStatsLabels.splice(1, 0, 'Aces - rival');
                numericStatsColors.splice(1, 0, 'green');
                numericStatsLabels.splice(3, 0, 'DFs - rival');
                numericStatsColors.splice(3, 0, 'red');
                numericStatsLabels.splice(5, 0, 'BPs to save - rival');
                numericStatsColors.splice(5, 0, 'yellow');
                numericStatsLabels.splice(7, 0, 'BPs created - rival');
                numericStatsColors.splice(7, 0, 'purple');
                numericStats.update();

                skillsSet.push({
                    label: ovr[allPlayers.indexOf(comparePlayerVar)].fields['Name'],
                    backgroundColor: "rgba(255, 51, 102, 0.2)",
                    borderColor: "rgba(255, 51, 102, 0.85)",
                    pointBackgroundColor: "rgba(255, 51, 102, 0.85)",
                    pointBorderColor: "rgba(255, 51, 102, 0.85)",
                    pointHoverBackgroundColor: "rgba(255, 51, 102, 0.8)",
                    pointHoverBorderColor: "rgba(255, 51, 102, 1)",
                    pointRadius: 4,
                    pointHoverRadius: 8,
                    borderRadius: 15,
                    lineWidth: 8,
                    borderCapStyle: 'round',
                    data: [new Array(10).fill(null)]});
                skills.update();

                odds.data.datasets.push({
                    backgroundColor: ["#b8e994", "#e056fd","#74b9ff","#f8c291","#e74c3c", '#95a5a6'],
                    label: ovr[allPlayers.indexOf(comparePlayerVar)].fields['Name'],
                    data: [new Array(6).fill(null)]});
                odds.update();
                
            }

            else if (serviceSet.length > 1) {

                serviceSet.pop();
                serviceSet.push({
                    backgroundColor: ['#778ca3', '#f8a5c2', '#ea8685', '#7EC66C'],
                    hoverBackgroundColor: ['#4b6584', '#f78fb3', '#e66767', '#6DA75E'],
                    label: selectRecognition[selectValue][1],
                    data: [new Array(4).fill(null)]});
                serviceAccuracy.update();

                returnSet.pop();
                returnSet.push({
                    backgroundColor: ['#596275', '#e77f67', '#e15f41', '#a55eea'],
                    hoverBackgroundColor: ['#303952', '#cf6a87', '#c44569', '#8854d0'],
                    label: selectRecognition[selectValue][1],
                    data: [new Array(4).fill(null)]});
                returnTbs.update();

                numericStatsArray[1] = null;
                numericStatsArray[3] = null;
                numericStatsArray[5] = null;
                numericStatsArray[7] = null;
                numericStatsLabels[1] = 'Aces - rival';
                numericStatsColors[1] = 'green';
                numericStatsLabels[3] = 'DFs - rival';
                numericStatsColors[3] = 'red';
                numericStatsLabels[5] = 'BPs to save - rival';
                numericStatsColors[5] = 'yellow';
                numericStatsLabels[7] = 'BPs created - rival';
                numericStatsColors[7] = 'purple';
                numericStats.update();

                skillsSet.pop();
                skillsSet.push({
                    label: ovr[allPlayers.indexOf(comparePlayerVar)].fields['Name'],
                    backgroundColor: "rgba(255, 51, 102, 0.2)",
                    borderColor: "rgba(255, 51, 102, 0.85)",
                    pointBackgroundColor: "rgba(255, 51, 102, 0.85)",
                    pointBorderColor: "rgba(255, 51, 102, 0.85)",
                    pointHoverBackgroundColor: "rgba(255, 51, 102, 0.8)",
                    pointHoverBorderColor: "rgba(255, 51, 102, 1)",
                    pointRadius: 4,
                    pointHoverRadius: 8,
                    borderRadius: 15,
                    lineWidth: 8,
                    borderCapStyle: 'round',
                    data: [new Array(10).fill(null)]});
                skills.update();

                odds.data.datasets[1] = {
                    backgroundColor: ["#b8e994", "#e056fd","#74b9ff","#f8c291","#e74c3c", '#95a5a6'],
                    label: ovr[allPlayers.indexOf(comparePlayerVar)].fields['Name'],
                    data: [new Array(6).fill(null)]};
                odds.update();

                };
            };                        
        });
    };

visualizePlayer(btnOvrMain, ovr, 'All surfaces, overall', '#df2e2b');
visualizePlayer(btnOvrOvr, ovr, 'All surfaces, overall', '#df2e2b');
visualizePlayer(btnOvrYear, ovryear, 'All surfaces, 2020 year', '#df2e2b');
visualizePlayer(btnOvrCur, ovrcur, 'All surfaces, after lockdown', '#df2e2b');
visualizePlayer(btnHardMain, hard, 'Hard courts, overall', '#3d94f6');
visualizePlayer(btnHardOvr, hard, 'Hard courts, overall', '#3d94f6');
visualizePlayer(btnHardYear, hardyear, 'Hard courts, 2020 year', '#3d94f6');
visualizePlayer(btnHardCur, hardcur, 'Hard courts, after lockdown', '#3d94f6');
visualizePlayer(btnClayMain, clay, 'Clay courts, overall', '#f4b811');
visualizePlayer(btnClayOvr, clay, 'Clay courts, overall', '#f4b811');
visualizePlayer(btnClayYear, clayyear, 'Clay courts, 2020 year', '#f4b811');
visualizePlayer(btnClayCur, claycur, 'Clay courts, after lockdown', '#f4b811');
         
comparePlayer(); 

