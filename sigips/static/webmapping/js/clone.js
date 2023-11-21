
MAPBOX_ACCESS_TOKEN = 'sk.eyJ1IjoibGF1cmVuem8xOTkyIiwiYSI6ImNscDZzOTNqNzF3dmgya3FvMjBjYzE1bTIifQ._Ux605Y4ItBDBVN5QkogQw'

const MENU_WIDTH = 250;
const DEFAULT_MAP_VIEW = [12.3569, -1.5352];
const API_URL = "api/sites/";

var selectedTypes = [];

var markersCanvas; 


$(document).ready(function () {
    const isMobile = window.mobileAndTabletcheck();

    if (isMobile) {
        setMenuWidth(MENU_WIDTH);
    }

    //creation de la carte
    const map = initializeMap();
    markersCanvas = new L.LayerGroup();
    markersCanvas.addTo(map);

    const osm = createTileLayer();
    osm.addTo(map);
    
    //Ajoutez l'événement de zoom à votre carte lors de l'initialisation
    map.on('zoomend', handleZoomEvent);
    ////////////////////////////////////////////////////////////////////////////////////
    const satelliteLayer = L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 200,
        id: 'mapbox/satellite-streets-v12',
        accessToken: MAPBOX_ACCESS_TOKEN
    });

    const satelliteLayer2 = L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 200,
        id: 'mapbox/streets-v12',
        accessToken: MAPBOX_ACCESS_TOKEN
    });


    const humanitarianLayer = L.tileLayer('https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.openstreetmap.fr/">OpenStreetMap France</a>'
    });

    const baseMaps = {
        "OpenStreetMap": osm,
        "Satellite": satelliteLayer,
        "Satellite opt 2":satelliteLayer2,
        "Humanitarian": humanitarianLayer
    };

    L.control.layers(baseMaps).addTo(map);
    L.control.zoom({ position: 'topright' }).addTo(map);
    
    /////////////////////////////////////////////////////////////////////////////////////////////////////

    const scaleControl = L.control.scale({ metric: true, imperial: false, position: 'bottomright' });
    scaleControl.addTo(map);

    const ctlZoomToFit = createZoomToFitControl(map);
    ctlZoomToFit.addTo(map);

    const ctlZoomBox = L.control.zoomBox({
        modal: false,
        position: "topright",
        title: "Zoom vers une région spécifique"
    });
    map.addControl(ctlZoomBox);

    // Faire une requête ajax pour récupérer les données
    loadSites();

    loadTypes();

    
    // Gérer les changements dans les filtres de type
    $('#typeFilters').on('change', 'input[type="checkbox"]', function () {
        updateMapMarkers();
    });

});

// Fonction pour charger les types
function loadTypes() {
    $.ajax({
        url: '/api/types/',
        type: 'GET',
        success: function (data) {
            const types = data.results;
            let checkboxHTML = '';
            for (const type of types) {
                checkboxHTML += `<div class="form-check">
                  <input class="form-check-input" type="checkbox" value="${type.id}" id="type-${type.id}">
                  <label class="form-check-label" for="type-${type.id}">${type.libelle}</label>
                </div>`;
            }
            $('#typeFilters').append(checkboxHTML);
        },
        error: function (error) {
            console.error('Error fetching data:', error);
        }
    });
}

// Fonction pour charger les sites
function loadSites() {
    $.ajax({
        url: API_URL + `?selectedTypes=${selectedTypes.join(',')}`,
        type: "GET",
        dataType: "json",
        success: function (data) {
            displayMarkers(data.results);
        },
        error: function (error) {
            console.error('Error fetching data:', error);
        }
    });
}

// Fonction pour mettre à jour les marqueurs sur la carte en fonction des filtres de type
function updateMapMarkers() {
    selectedTypes = Array.from(document.querySelectorAll('input[type="checkbox"]:checked')).map(checkbox => checkbox.value);
   
    $.ajax({
        url: API_URL + `?type_site=${selectedTypes.join(',')}`,
        type: "GET",
        dataType: "json",
        data: { selectedTypes: selectedTypes },
        success: function (data) {
            markersCanvas.clearLayers();
            displayMarkers(data.results);
        },
        error: function (error) {
            console.error('Error fetching data:', error);
        }
    });
}


// Fonction pour afficher les marqueurs sur la carte
function displayMarkers(results) {
    results.forEach(result => {
        const latitude = parseFloat(result.latitude);
        const longitude = parseFloat(result.longitude);

        if (!isNaN(latitude) && !isNaN(longitude) || selectedTypes.includes(result.typesite)) {
            
            const customIcon = L.icon({
                iconUrl: "static/webmapping/img/cicrlce-green.png",
                iconSize: [15, 15],
                iconAnchor: [10, 5],
            });

            const markerContent = `
                <br><b>Commune : </b>${result.commune}
                <br><b>Village : </b>${result.village}
                <br><b>Type de site : </b>${result.typesite}
                <br><b>Status : </b>${result.statut ? result.statut_id : 'N/A'}
                <br> <b>Nom du site : </b>${result.nom_site}
                <br><b>Observation géologique du site : </b>${result.obs_geo}
                <br> <b>Étendu : </b>${result.etendu}`;

            L.marker([latitude, longitude], { icon: customIcon, siteName: result.nom_site }).addTo(markersCanvas).bindPopup(markerContent);
        } else {
            console.warn("Invalid coordinates or type not selected for:", result);
        }
    });
}





function setMenuWidth(width) {
    $("#slide_menu").css('width', `${width}px`);
}

function initializeMap() {
    return L.map('map', { maxZoom: 200, zoomControl: false }).setView(DEFAULT_MAP_VIEW, 6);
}

function createTileLayer() {
    return new L.TileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    });
}

function createZoomToFitControl(map) {
    const ctlZoomToFit = L.control();

    ctlZoomToFit.onAdd = function (map) {
        this._div = L.DomUtil.create('div', 'zoomtofit leaflet-bar');
        this._div.title = "Centrer la carte sur Ouagadougou";

        this._div.onclick = function () {
            map.setView(DEFAULT_MAP_VIEW, 9); // Center in Ouagadougou
        };

        L.DomEvent.on(this._div, 'click', function (ev) {
            L.DomEvent.stopPropagation(ev);
        });

        return this._div;
    };

    return ctlZoomToFit;
}



function toggleLeftPane() {
    const isMobile = window.mobileAndTabletcheck();

    if (isMobile) {
        setMenuWidth(MENU_WIDTH);
    }

    $('#slide_menu').toggleClass('slide_menu_visible');
    $('#slide_button').toggleClass('slide_button_visible');
    $('#legend').toggleClass('legend_visible');
    $('#slide_button .fas').toggleClass('fa-rotate-180');
}

window.mobileAndTabletcheck = function () {
    var check = false;
    (function (a) { if (/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce|xda|xiino|android|ipad|playbook|silk/i.test(a) || /1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(a.substr(0, 4))) check = true; })(navigator.userAgent || navigator.vendor || window.opera);
    return check;
};




function handleZoomEvent(e) {
    const currentZoom = e.target.getZoom();
    const zoomThreshold = 12;

    if (currentZoom >= zoomThreshold) {
        showSiteNames();
    } else {
        hideSiteNames();
    }
}



function showSiteNames() {
    markersCanvas.eachLayer(layer => {
        layer.bindTooltip(layer.options.siteName, { permanent: true, className: 'site-label' }).openTooltip();
    });
}

function hideSiteNames() {
    markersCanvas.eachLayer(layer => {
        layer.closeTooltip();
    });
}

