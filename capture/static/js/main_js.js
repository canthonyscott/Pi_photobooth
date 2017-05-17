/**
 * Created by anthony on 5/16/17.
 */

// Place everything in document ready function, ids wont exist until DOM is fully loaded
$(document).ready(function () {
    console.log("Ready!");


    // Execute when Take a Photo button pressed
    $('#cap-btn').click(function () {
        console.log("Capture btn clicked!");

        var countdown = 5;
        $('#cap-btn').text(countdown);
        setInterval(function () {
            countdown--;
            if (countdown > 0){
                $('#cap-btn').text(countdown);
            }
            else if (countdown == 0){
                //POST REQUEST TO SERVER

                $.post('', function (data) {
                    console.log(data);
                    display_photo('');
                    reset_button();
                });


                $('#cap-btn').text('Smile!')
            }
        }, 1000);

    });


    function reset_button(){
        $('#cap-btn').text('Take a Photo!');
    }

    function display_photo(addr) {
        console.log("addr rec: ", addr);
        // set modal src to an image and display it for a few seconds
            $('#modalPhoto').attr('src', addr);
            $('#myModal').modal('toggle')
        var countdown = 5;
        setInterval(function () {
            countdown--;
            // hide modal after 5 seconds
            if (countdown == 0){
                $('#myModal').modal('hide')

            }
        }, 1000);
    }


});

