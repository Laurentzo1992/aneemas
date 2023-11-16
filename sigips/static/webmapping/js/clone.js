
// gestion du boutton de panel

function toggleLeftPane() {
    if (window.mobileAndTabletcheck()) {
        menu_width = 250; //Reduce menu width for portable devices
        $("#slide_menu").css('width', '250px');
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




// initialisation de la carte

$(document).ready(function () {

    if (window.mobileAndTabletcheck()) {
        menu_width = 250; //Reduce menu width for portable devices
        $("#slide_menu").css('width', '250px');
    }
    map = (new L.map('map', { maxZoom: 100, zoomControl: false }));


    map.setView([12.3569, -1.5352], 6); //Coordinates and zoom level
    //
    // Create base layers objects
    var osm = new L.TileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18
        , attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    });

    (new L.Control.Zoom({ position: 'topright' })).addTo(map);

    map.addLayer(osm);
    
    markersCanvas = new L.MarkersCanvas();
    markersCanvas.addTo(map);

    //Scale control
    scaleControl = L.control.scale({ metric: true, imperial: false, position: 'bottomright' });
    scaleControl.addTo(map);
    //Zoom to fit control
    var ctlZoomToFit = L.control();

    ctlZoomToFit.onAdd = function (map) {
        this._div = L.DomUtil.create('div', 'zoomtofit leaflet-bar'); // create a div with a class "info"
        this._div.title = "Centrer la carte sur Ouagadougou";

        this._div.onclick = function () {
            map.setView([12.3569, -1.5352], 9); //center in Ouagadougou
        };
        L.DomEvent.on(this._div, 'click', function (ev) {
            L.DomEvent.stopPropagation(ev);
        });
        return this._div;
    };
    ctlZoomToFit.addTo(map);

    //Zoom box control

    var ctlZoomBox = L.control.zoomBox({
        modal: false,  // If false (default), it deactivates after each use.
        // If true, zoomBox control stays active until you click on the control to deactivate.
        position: "topright",
        // className: "customClass"  // Class to use to provide icon instead of Font Awesome
        title: "Zoom vers une région spécifique" // a custom title
    });
    map.addControl(ctlZoomBox);

    // Make an AJAX request to fetch data
    $.ajax({
        url: "http://127.0.0.1:8000/api/infrastructures/",
        type: "GET",
        dataType: "json",
        success: function(response) {
            const results = response.results;
            console.log(results);
    
            // Vérifiez si le tableau de résultats est défini et n'est pas vide
            if (results && results.length > 0) {
                results.forEach(data => {
                    // Assurez-vous que les coordonnées sont définies et sont des nombres
                    const latitude = parseFloat(data.latitude);
                    const longitude = parseFloat(data.longitude);
    
                    // Vérifiez si les coordonnées sont valides
                    if (!isNaN(latitude) && !isNaN(longitude)) {
                        // Utilisez le contenu de votre marqueur ici (vous pouvez personnaliser cela)
                        const markerContent = `<b>${data.nom_site}</b><br>${data.obs_geo}`;
    
                        // Ajoutez le marqueur à la carte avec le contenu spécifié
                        L.marker([latitude, longitude]).addTo(map).bindPopup(markerContent);
                    } else {
                        console.warn("Coordonnées non valides pour :", data);
                    }
                });
            } else {
                console.warn("Aucune donnée à afficher.");
            }
        },
        error: function(error) {
            console.error('Erreur lors de la récupération des données:', error);
        }
    });
    

});



