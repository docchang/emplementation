var Timezone = $.format.date(new Date(), "tz");

(function ($) {
    $.fn.localTimeFromUTC = function (format) {
        return this.each(function () {

            // get time offset from browser
            var currentDate = new Date();
            var offset = -(currentDate.getTimezoneOffset() / 60);

            // get provided date
            var tagText = $(this).html();
            var givenDate = new Date($.format.date(tagText, format));

            // apply offset
            var hours = givenDate.getHours();
            hours += offset;
            givenDate.setHours(hours);

            // format the date
            var localDateString = $.format.date(givenDate, format);
            $(this).html(localDateString);
        });
    };
})(jQuery);

function StartUp() {
    $('.UTCTimestamp').localTimeFromUTC('MM/dd/yyyy hh:mm:ss a');
}