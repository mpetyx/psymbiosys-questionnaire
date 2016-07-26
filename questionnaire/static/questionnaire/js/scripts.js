/**
 * Created by DarkA_000 on 7/21/2016.
 */
function drawChart(container, url, qsPart) {

        $(container).addClass('opac');

        $.ajax({
            type: "get",
            cache: false,
            url: url,
            dataType: "json",
            error: function (xhr, status, error) {
                console.log('Something went bad');
            },
            success: function (data) {
                $(container).removeClass('opac').empty();
                var svg = dimple.newSvg(container, "90%", "100%");
                var myChart = new dimple.chart(svg, data);
                myChart.setBounds(10, 30, "100%", 400);

                if ((qsPart == undefined) || (qsPart != 3)) {
                    myChart.addCategoryAxis("x", ["Question", "Answer"]);
                    myChart.addMeasureAxis("y", "Responses");
                    myChart.addSeries("Answer", dimple.plot.bar);
                    myChart.addLegend(20, 0, "100%", 50, "left");
                }
                else {
                    myChart.addMeasureAxis("p", "Responses");
                    myChart.addSeries("Answer", dimple.plot.pie);
                    myChart.addLegend("80%", 0, "20%", 300, "left");
                }
                myChart.draw();
            }
        })
    }

function drawStats(container, url) {
    var $statsContainer = $(container);
    $statsContainer.addClass('opac');

    $.ajax({
         type: "get",
         cache: false,
         url: url,
         dataType: "json",
         error: function (xhr, status, error) {
             console.log('Something went bad');
         },
         success: function (data) {
            
             $('#number-of-responses').html(data['#_of_responses']);
             $('#number-of-unique-responses').html(data['#_of_unique_responses']);
             
             $('#number-of-workers').html(data['#_of_workers']);
             $('#number-of-managers').html(data['#_of_managers']);
             $('#number-of-visitors').html(data['#_of_visitors']);
             
             $statsContainer.removeClass('opac').empty();
             $.each(data['percentages'], function(i, stat) {
                 var $container = $('<div class="col-xs-12 main-stat"></div>');
                 $container.append('<div class="col-xs-9">' + ((stat['Answer'] != '') ? stat['Answer'] : '(No Answer)') + '</div>');
                 $container.append('<div class="col-xs-3">' + stat['Percentage'] + '% </div>');
                 $statsContainer.append($container)
             })
         }
     })
}

function updateBrandValueTable (container, url) {
    $.ajax({
         type: "get",
         cache: false,
         url: url,
         error: function (xhr, status, error) {
             console.log('Something went bad');
         },
         success: function (data) {
             $(container).html(data)
         }
    });

    $.ajax({
        type: "get",
        cache: false,
        url: url.replace('charts', 'stats'),
        dataType: "json",
        error: function (xhr, status, error) {
            console.log('Something went bad');
        },
        success: function (data) {

            $('#number-of-responses').html(data['#_of_responses']);
            $('#number-of-unique-responses').html(data['#_of_unique_responses']);

            $('#number-of-workers').html(data['#_of_workers']);
            $('#number-of-managers').html(data['#_of_managers']);
            $('#number-of-visitors').html(data['#_of_visitors']);
        }
    })
}

$(document).ready(function() {
    // select & checkbox initialization
    $('select').chosen();
    // $('input[type="checkbox"]').iCheck({checkboxClass: 'icheckbox_flat-aero'})

    // table show
    $('select#table-choice').on('change', function () {
        var $tables = $('table'),
            $selectedIdx = $(this).find('option:selected').index();

        $tables.addClass('hidden');
        $tables.eq($selectedIdx).removeClass('hidden');
    });


    $('select#table-type-filter').on('change', function() {
        var val = $(this).find('option:selected').data('val').toUpperCase(),
            $table = $('table:not(.hidden)');
        
        $table
            .find('tr')
            .removeClass('hidden-type')
            .find('td.subject-type')
            .filter(function(){
                return $(this).text() != val
            })
            .closest('tr')
            .addClass('hidden-type');
    });
    
    $('select#chart-choice, select#chart-subject-type-filter, select#chart-campaign-filter, input#chart-unique-answers-filter').on('change',
        function() {
            var urlParamString = '?',
                $option = $('select#chart-choice').find('option:selected'),
                chartChoice = $option.index() + 1;

            if ($option.text() == '') {
                return;
            }

            $.each($('select#chart-subject-type-filter, select#chart-campaign-filter, input#chart-unique-answers-filter'), function(i, sel) {
                if ($(sel).is('select')) {

                    var $option = $(sel).find('option:selected'),
                        varname = $option.data('varname'),
                        val = $option.val();
                }
                else {
                    var varname = $(sel).data('varname'),
                        val = $(sel).prop('checked');
                }

                if ((val) && (varname != undefined)) {
                    if (urlParamString.length != 1) {
                        urlParamString += '&';
                    }

                    urlParamString += varname + '=' + val;
                }
            });

            var endpointURL = chartChoice + '/' + urlParamString;
            drawChart('#chartContainer', '/analytics/workers-sentiment-charts/' + endpointURL, chartChoice);
            drawStats('#statsContainer', '/analytics/workers-sentiment-stats/' + endpointURL)
    });

    $('select#brand-table-campaign-filter, select#brand-table-type-filter, input#brand-table-unique-answers-filter').on('change',
        function() {
            var urlParamString = '?';

            $.each($('select#brand-table-campaign-filter, select#brand-table-type-filter, input#brand-table-unique-answers-filter'), function(i, sel) {
                if ($(sel).is('select')) {

                    var $option = $(sel).find('option:selected'),
                        varname = $option.data('varname'),
                        val = $option.val();
                }
                else {
                    var varname = $(sel).data('varname'),
                        val = $(sel).prop('checked');
                }

                if ((val) && (varname != undefined)) {
                    if (urlParamString.length != 1) {
                        urlParamString += '&';
                    }

                    urlParamString += varname + '=' + val;
                }
            });
            console.log(urlParamString)
            var endpointURL = '/analytics/brand-value-charts/'+ urlParamString;
            updateBrandValueTable('#brand-value-table-container', endpointURL);
            drawStats()
    });
    
    $('select#table-campaign-filter').on('change', function() {
        var val = $(this).find('option:selected').data('val').toUpperCase(),
            $table = $('table:not(.hidden)');
        
        $table
            .find('tr')
            .removeClass('hidden-campaign')
            .find('td.campaign-name')
            .filter(function(){
                return $(this).text() != val
            })
            .closest('tr')
            .addClass('hidden-campaign');
    });

    $('body.analytics-page h4 .toggle-section').on('click', function() {
        $(this)
            .closest('h4')
            .toggleClass('collapsed')
            .find('i')
            .toggleClass('fa-chevron-up fa-chevron-down')
    });

    if ($('body').hasClass('brand-value')) {
        updateBrandValueTable('#brand-value-table-container', '/analytics/brand-value-charts/');
    }
    else {
        // Chart Initialization
        drawChart('#chartContainer', '/analytics/workers-sentiment-charts/1/');
        drawStats('#statsContainer', '/analytics/workers-sentiment-stats/1/');
    }
});

