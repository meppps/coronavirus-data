
// JS for interactive plots

// === Predefined functions === //
function findIndex(country){
    for(i=0;i<list.length;i++){
        if(country === list[i]){
            return i;
        }
    }
};

function parseNum(num){
    if(num){

        if(num.includes('+')){
            num = num.replace('+','');
        };
        if(num.includes(',')){
            num = num.replace(',','');
        };
        return Number(num)
    }
};

// ===================== //
// === Initial plot === //
// ===================== //

var totalCases = obj['totalCases'];
var newCases = obj['newCases'];
var totalRecovered = obj['recovered'];
var totalDeaths = obj['deaths'];
// var newDeaths = parseInt(obj['NewDeaths']);
var activeCases = obj['activeCases'];
var tests = obj['tests'];
var selectedLocation = document.getElementById('location');
var selectedMetric = document.getElementById('selectedMetric');




var set = [
    {
        // title: country,
        x: ['Total Cases', 'Active Cases','New Cases','Recovered','Deaths'],
        y: [totalCases[0] ,activeCases[0], newCases[0], totalRecovered[0], totalDeaths[0]],
        type: 'bar',
        marker:{
        color: ['#856c8b', '#ff7f50', '#ffeb99', '#a7e9af', '#f67280']
        }
    }
];




Plotly.newPlot('myDiv',set)



// Create list of countries
var countries = obj['name'];
var length = countries.length;
var list = [];
for(i=0;i<length;i++){

    var option = document.createElement('option');
    option.text = countries[i];
    option.value = countries[i];
    var select = document.getElementById('countrySelect');
    select.appendChild(option);
    list.push(countries[i]);

};
selectedLocation.innerText = document.getElementById('countrySelect').value;






// ==== Update Plot === //
document.getElementById('countrySelect').addEventListener('change',()=>{

    // Get values
    var country = document.getElementById('countrySelect').value;
    var index = findIndex(country);
    var totalCases = obj['totalCases'][index];
    var newCases = obj['newCases'][index];
    var totalRecovered = obj['recovered'][index];
    var totalDeaths = obj['deaths'][index];
    var newDeaths = parseInt(obj['deaths'][index]);
    var activeCases = obj['activeCases'][index];
    var selectedTests = obj['tests'][index];


    // Plot
    var set = [
    {
        x: ['Total Cases', 'Active Cases','New Cases','Recovered','Deaths'],
        y: [totalCases ,activeCases, newCases, totalRecovered, totalDeaths],
        type: 'bar',
        marker:{
    color: ['#856c8b', '#ff7f50', '#ffeb99', '#a7e9af', '#f67280']
    }}
    ];

    Plotly.newPlot('myDiv', set);

    selectedLocation.innerText = document.getElementById('countrySelect').value;


});

          
    
// ===================== //
// Country Comparison //
// ===================== //


function initComp(){

    // Define selectors
    var compr1 = document.getElementById('compr1');
    var compr2 = document.getElementById('compr2');
    var metricSelector = document.getElementById('metric');
    var metrics = ['Total Cases','Active Cases','New Cases','Recovered','Deaths','Tests','Population'];


    function getMetric(m){
        return m === 'Total Cases' ? 'totalCases':
        m === 'Active Cases' ? 'activeCases':
        m === 'New Cases' ? 'newCases':
        m === 'Recovered' ? 'recovered':
        m === 'Deaths' ? 'deaths':
        m === 'Tests' ? 'tests':
        m === 'Population' ? 'population':
        'None';
    };


    // Metric selector
    metrics.forEach((met)=>{
        var option = document.createElement('option');
        option.value = met;
        option.text = met;
        metricSelector.appendChild(option);
    });

    // Country selector
    function initSelector(selector){
        list.forEach((country)=>{
        var option = document.createElement('option');

        option.text = country;
        option.value = country;
        selector.appendChild(option)
        });
    }; 

    // Initial plot
    initSelector(compr1);
    initSelector(compr2);
    initSelector(compr3);
    initSelector(compr4);


    var total1 = obj['totalCases'][0];
    var total2 = obj['totalCases'][1];
    var total3 = obj['totalCases'][2];
    var total4 = obj['totalCases'][3];


    var comp = [
        {
            x:[total1,total2,total3,total4],
            y:[list[0],list[1],list[2],list[3]],
            orientation: 'h',
            type:'bar',
            marker:{
                color: ['orange','lightblue','lightgreen','lightred']
            }
        }
    ];

    Plotly.newPlot('compare', comp);
    selectedMetric.innerText = metricSelector.value;


// ===================== //
// Dynamic functionality //
// ===================== //

var selectorList = [compr1,compr2,compr3,compr4,metricSelector];
var selection = 0;

    selectorList.forEach((selector)=>{
        if(selector != metricSelector){
            selector.selectedIndex = selection += 1;
    };

        // Update
        addEventListener('change',()=>{
            
            // Compare by metric
            var metric = document.getElementById('metric').value;

            // Country
            var country1 = compr1.value;
            var country2 = compr2.value;
            var country3 = compr3.value;
            var country4 = compr4.value;

            // Index
            var index1 = findIndex(country1);
            var index2 = findIndex(country2);
            var index3 = findIndex(country3);
            var index4 = findIndex(country4);

            // Get figure
            var total1 = obj[getMetric(metric)][index1];
            var total2 = obj[getMetric(metric)][index2];
            var total3 = obj[getMetric(metric)][index3];
            var total4 = obj[getMetric(metric)][index4];
            
            // Plot
            var comp = [
                {
                    x:[total1,total2,total3,total4],
                    y:[country1,country2,country3,country4],
                    orientation:'h',
                    type:'bar',
                    marker:{
                        color: ['green','blue','red','orange']
                    }
                }
            ];
        
            Plotly.newPlot('compare',comp);
            selectedMetric.innerText = metricSelector.value;
        })
    });


};
initComp();



// ==== Plot on map ==== // 
for(i=0;i<list.length;i++){

    var con = list[i];
    var coords = obj['coords'][i];
    var total = obj['totalCases'][i];
    var active = obj['activeCases'][i];
    var loc = obj['name'][i];
    var rec = obj['recovered'][i];
    var pop = obj['population'][i];
    var test = obj['tests'][i];
    var fatal = obj['deaths'][i];
    var newCase = obj['newCases'][i];

    if(loc == 'CAR'){
        continue
    };


    var text = `<h2>${loc}<h2>
                <h4>Population: ${pop}<h4>
                <h4>Total Cases: ${total}<h4>
                <h4>Active Cases: ${active}<h4>
                <h4>New Cases: ${newCase}</h4>
                <h4>Tests: ${test}</h4>
                <h4>Recovered: ${rec}</h4>
                <h4>Fatal: ${fatal}</h4>`;

    L.circle(coords, {
    fillOpacity: 0.75,
    color: 'white',
    fillColor: 'grey',
    radius: 200000
    }).bindPopup(text).addTo(mymap);



    // console.log(coords)

}