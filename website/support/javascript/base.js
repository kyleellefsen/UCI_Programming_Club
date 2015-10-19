$(init);
function init() {
    $( ".tabs" ).tabs();
    $('.toptab').tabs({ active: 1 });
    
    var now = new Date();
    var start = new Date("2015-09-20 GMT-0700"); // September 20th
    var diff = now - start;
    var oneDay = 1000 * 60 * 60 * 24;
    var day = Math.floor(diff / oneDay);
    var week = Math.floor(day/7);
    if (week>0){
        $('#weeks').find("li.ui-state-active").removeClass('ui-state-active');
        $('#weeks').tabs({ active: week-1 });
    }
}