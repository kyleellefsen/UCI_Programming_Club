$(init);
function init() {
    $( ".tabs" ).tabs();
    $('.toptab').tabs({ active: 1 });
    
    var now = new Date();
    var start = new Date(2015, 3, 5); // April 6th start date
    var diff = now - start;
    var oneDay = 1000 * 60 * 60 * 24;
    var day = Math.floor(diff / oneDay);
    var week = Math.floor(day/7);
    $('#weeks').find("li.ui-state-active").removeClass('ui-state-active');
    $('#weeks').tabs({ active: week });
}