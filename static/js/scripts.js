const socket = io();

socket.on('parking_status', function(data) {
    console.log('Received parking status update: ', data);
    var spotsStatus = data.parking_spots_status;
    for (var spotId in spotsStatus) {
        if (spotsStatus.hasOwnProperty(spotId)) {
            var spotElement = document.getElementById('spot-' + spotId);
            if (spotElement) {
                if (spotsStatus[spotId]) {
                    spotElement.classList.remove('occupied');
                    spotElement.classList.add('available');
                } else {
                    spotElement.classList.remove('available');
                    spotElement.classList.add('occupied');
                }
            }
        }
    }
});
