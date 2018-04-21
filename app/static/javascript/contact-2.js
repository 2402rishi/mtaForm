$(function () {

    // init the validator
    // validator files are included in the download package
    // otherwise download from http://1000hz.github.io/bootstrap-validator

    $('#contact-form').validator();


    // when the form is submitted
    $('#contact-form').on('submit', function (e) {
        console.log("Im a done");
        // if the validator does not prevent form submit
        if (!e.isDefaultPrevented()) {
            var url = "http://localhost:5000/send";

            // POST values in the background the the script URL
            return true;
        }
    })
});