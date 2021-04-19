/**
 * Created by anthony on 5/16/17.
 */

// Place everything in document ready function, ids wont exist until DOM is fully loaded
$(document).ready(function () {
    console.log("Ready!");


    // Execute when Take a Photo button pressed
    $('#cap-btn').click(function () {
        console.log("Capture btn clicked!");
        $('#cap-btn').attr("disabled", true);

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
                    // console.log(data);
                    if (data > 0){
                        notify_error(data);
                    }
                    else {
                        display_photo(data);
                    }
                });


                $('#cap-btn').text('Smile!')
            }
        }, 1000);

    });


    function reset_button(){
        $('#cap-btn').removeAttr("disabled");
        $('#cap-btn').text('Take a Photo!');
    }

    function display_photo(addr) {
        console.log("addr rec: ", addr);
        $('#cap-btn').text("Please Wait....");
        // set modal src to an image and display it for a few seconds
            $('#modalPhoto').attr('src', addr);
            $('#myModal').modal('toggle');
        var countdown = 8;
        setInterval(function () {
            countdown--;
            // hide modal after 5 seconds
            if (countdown == 0){
                $('#myModal').modal('hide');
                reset_button();

            }
        }, 1000);
    }
    
    function notify_error(code) {
        $('#cap-btn').addClass('btn-danger');
        if (code == 1){
            $('#cap-btn').text("Too close, back up");
        }
        else if (code == 2){
            $('#cap-btn').text("Camera error");
        }
        var countdown = 6
        setInterval(function () {
            countdown--;
            if (countdown == 0){
               $('#cap-btn').removeClass('btn-danger');
               reset_button();
            }

        }, 1000);
    }


});

