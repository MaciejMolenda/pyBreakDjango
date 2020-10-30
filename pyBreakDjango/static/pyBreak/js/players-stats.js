$(document).ready(function() {
    $('.js-example-basic-single').select2({
    placeholder: "Search for your Player",
    allowClear: true
  });
});

$("#selection").on("select2:select", function (e) {
    window.open(e.params.data.id);
});

let oddsDict = {};

for (let i = 0; i < ovr.length; i++) {
      oddsDict[ovr[i].fields.Name] = [
        (ovr[i].fields.Surety_won / ovr[i].fields.Surety_played * 100).toFixed(1),
        (ovr[i].fields.Favorite_won / ovr[i].fields.Favorite_played * 100).toFixed(1),
        (ovr[i].fields.Slightfav_won / ovr[i].fields.Slightfav_played * 100).toFixed(1),
        (ovr[i].fields.Slightunder_won / ovr[i].fields.Slightunder_played * 100).toFixed(1),
        (ovr[i].fields.Under_won / ovr[i].fields.Under_played * 100).toFixed(1),
        (ovr[i].fields.Underdog_won / ovr[i].fields.Underdog_played * 100).toFixed(1),
      ];
    };

let oddsTab = document.getElementById("odds-table").getElementsByTagName("tbody")[0];
let playersTd = oddsTab.getElementsByTagName("tr");

Object.keys(oddsDict).forEach(function(key) {
  for (let i = 0; i < oddsDict[key].length; i++) {
    if (oddsDict[key][i] == 'NaN') {
      oddsDict[key][i] = '-';
    }
  }
});

for (let i = 0; i < playersTd.length; i++) {
    playersTd[i].children[2].textContent = oddsDict[playersTd[i].children[1].textContent][0];
    playersTd[i].children[3].textContent = oddsDict[playersTd[i].children[1].textContent][1];
    playersTd[i].children[4].textContent = oddsDict[playersTd[i].children[1].textContent][2];
    playersTd[i].children[5].textContent = oddsDict[playersTd[i].children[1].textContent][3];
    playersTd[i].children[6].textContent = oddsDict[playersTd[i].children[1].textContent][4];
    playersTd[i].children[7].textContent = oddsDict[playersTd[i].children[1].textContent][5];
  };

function changeButton(element) {
  element.addEventListener("click", function (e) {
    if (this.textContent == 'Open the table') {
      this.textContent = 'Close the table';
      this.style.backgroundColor = '#fela00';
      this.style.background = 'linear-gradient(to bottom, #fe1a00 5%, #ce0100 100%)';
      this.style.border = '1px solid #d83526';
    }
    else {
      this.textContent = 'Open the table';
      this.style.backgroundColor = '#89c403';
      this.style.background = 'linear-gradient(to bottom, #89c403 5%, #77a809 100%)';
      this.style.border = '1px solid #74b807';
    };
  });
};

changeButton(document.getElementById('serve-button'));
changeButton(document.getElementById('return-button'));
changeButton(document.getElementById('odds-button'));