/**
 * Created by DarkA_000 on 7/21/2016.
 */

var _RADAR_CHART_MAPPINGS = {
    PLEASURE: 'Psychological level of gusto while working in the room, being 1 the minimum pleasure and 5 the maximum pleasure.',
    ACTIVATION: 'Psychological level of willingness to work due to working room and ambiance, being 1 the minimum level of activation and 5 the maximum level of activation.',
    CONTROL: 'Psychological perception of dominance of the situation while working in the room, being 1 the miminum level of perceived control and 5 the maximum level of perceived control. ',
    MODIFICATION: 'Psychological need for modifying the working ambiance and room elements, being 1 the maximum need for modification and 5 the minimum need for modification.',
    AVOIDANCE: 'Psychological need for leaving the working room due to displeasure with ambiance and room elements, being 1 the maximum need for avoiding the room and 5 the minimum need for avoidance.'
};

function evaluateKpiSubtitle(Questionnaire, userType) {
    var q = Questionnaire.toUpperCase();
    var ut = userType ? userType.toUpperCase() : 'ALL';


    if (q === 'WORKERS_SENTIMENT') {
        return {
            'ALL': 'a_ALL',
            'WORKER': 'b_WORKERS',
            'MANAGER': 'c_MANAGERS',
            'VISITOR': 'd_VISITORS'
        }[ut];

    } else {
        return {
            'ALL': 'a_ALL EMPLOYEES',
            'WORKER': 'b_WORKERS',
            'MANAGER': 'c_MANAGERS',
            'VISITOR': 'a_VISITORS'
        }[ut];
    }
}


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

                var NumberOfResponses;

                if (qsPart != 4 && qsPart != 5) {
                    var svg = dimple.newSvg(container, "100%", 675);
                    var myChart = new dimple.chart(svg, data);
                    myChart.setBounds(50, 75, 485, 550);

                    if ((qsPart == undefined) || (qsPart != 3)) {
                        myChart.addCategoryAxis("x", "Question");
                        myChart.addMeasureAxis("y", "Responses");
                        var myOtherSeries = myChart.addSeries("Answer", dimple.plot.bar);
                        myOtherSeries.barGap = 0.5;
                        myChart.addLegend(50, 0, "100%", 50, "left");

                        myChart.assignColor("Not suitable for working", "rgba(182, 7, 7, 0.9)", "rgba(182, 7, 7, 0.9)");
                        myChart.assignColor("Suitable for working", "rgba(9, 97, 16, 0.86)", "rgba(9, 97, 16, 0.86)");
                        myChart.assignColor("Neither/nor", "rgb(215, 135, 37)", "rgb(215, 135, 37)");

                        myOtherSeries.getTooltipText = function(e) {
                            NumberOfResponses = 0;
                            data.forEach(function( entry ) {
                                if (entry['Question'] == e.xField[0] ) {
                                   NumberOfResponses += entry['Responses']
                                }
                            });

                            return [
                                'Answer: ' + e.xField[1],
                                'Responses: ' + e.yValue,
                                'Percentage: ' + (e.yValue * 100 / NumberOfResponses).toFixed(2) + '%'
                            ]
                        };
                    }
                    else {
                        myChart.addMeasureAxis("p", "Responses");
                        var mySeries = myChart.addSeries("Answer", dimple.plot.pie);
                        myChart.addLegend("80%", 0, "20%", 300, "left");

                        NumberOfResponses = data.reduce( function(a, b){
                            return a + b['Responses'];
                        }, 0);

                        mySeries.getTooltipText = function(e) {
                            return [
                                'Answer: ' + e.seriesValue,
                                'Responses: ' + e.pValue,
                                'Percentage: ' + (e.pValue * 100 / NumberOfResponses).toFixed(2) + '%'
                            ]
                        };

                        myChart.assignColor("Need some rest", "rgba(182, 7, 7, 0.9)", "rgba(182, 7, 7, 0.9)");
                        myChart.assignColor("Can keep working", "rgba(9, 97, 16, 0.86)", "rgba(9, 97, 16, 0.86)");
                        myChart.assignColor("Neither/nor", "rgb(215, 135, 37)", "rgb(215, 135, 37)");

                        svg.append("text")
                            .attr("x", 295)
                            .attr("y", 625)
                            .attr("text-anchor", "middle")
                            .style("font-size", "12px")
                            .text("Fatigue");

                    }
                    myChart.draw();
                } else {
                    var chart = RadarChart.chart();
                    var svg = d3
                        .select(container)
                        .append('svg')
                        .attr('width', 550)
                        .attr('height', 550);

                    // change config
                    chart.config({
                        levels: 5,
                        maxValue: 5,
                        factorLegend: 1,
                        axisLine: true,
                        axisText: true,
                        w: 545,
                        h: 545

                    });

                    // draw one
                    svg
                        .append('g')
                        .classed('focus', 1)
                        .datum(data)
                        .call(chart);


                    // add fake axis scale
                    $(container).append('<div id="radar-chart-scale"><div>5</div><div>4</div><div>3</div><div>2</div><div>1</div><div>0</div></div>')

                    var $radarLegends = $('.radar-chart .axis text.legend');

                    $radarLegends.each(function(i, legend) {

                        var $legend = $(legend);
                        var text = _RADAR_CHART_MAPPINGS[$legend.text().trim().toUpperCase()];

                        $legend
                            .attr('data-toggle', "tooltip")
                            .attr('title', text)
                            .attr('data-container', 'body')
                            .attr('data-placement', 'bottom');
                    });

                    $radarLegends.tooltip();
                }
            }
        })
    }

function drawStats(container, url) {
    var $statsContainer = $(container);
    var $dictContainer = $('#dictContainer');
    $statsContainer.addClass('opac');
    $dictContainer.addClass('opac');

    $.ajax({
         type: "get",
         cache: false,
         url: url,
         error: function (xhr, status, error) {
             console.log('Something went bad');
         },
         success: function (data) {

             $statsContainer.removeClass('opac').empty();
             $dictContainer.removeClass('opac').empty();

             if ('#_of_responses' in data) {

                 $('#number-of-responses').html(data['#_of_responses']);
                 $('#number-of-unique-responses').html(data['#_of_unique_responses']);

                 $('#number-of-workers').html(data['#_of_workers'] + ' ( ' + data['%_of_workers'] + '% )');
                 $('#number-of-managers').html(data['#_of_managers'] + ' ( ' + data['%_of_managers'] + '% )');
                 $('#number-of-visitors').html(data['#_of_visitors'] + ' ( ' + data['%_of_visitors'] + '% )');
             }

             $('#section-title').html(data['section_title']);

             if (data['kpi'] != null && data['kpi_title']) {
                 $('.kpi-table').hide();
                 $('#performance-indicators').show();
                 $('.kpi-container').html(data['kpi'].toFixed(2) + '%');
                 $('.kpi-subject-type').text(data['subject_type'].toLowerCase() + 's');
                 
                 var $kpiTable;
                 if (data['part'] == 1 || data['part'] == 2) {
                     $kpiTable = $('#kpi-table-1')
                 } else if (data['part'] == 4 || data['part'] == 5) {
                     $kpiTable = $('#kpi-table-2')
                 }
                 
                 $kpiTable.show();
                 $kpiTable.find('.suggestions').hide();
                 if (data['kpi'] < 50) {
                     $kpiTable.find('.suggestions-below-50').show();
                 } else if (data['kpi'] < 80) {
                     $kpiTable.find('.suggestions-between-50-80').show();
                 } else {
                     $kpiTable.find('.suggestions-above-80').show();
                 }

                 $('.kpi-subtitle').html(
                     evaluateKpiSubtitle(
                         'WORKERS_SENTIMENT',
                         $('select#chart-subject-type-filter option:selected').val()
                     )
                 );

             } else {
                 $('body.worker-sentiment .kpi-table').hide();
                 $('#performance-indicators').hide();
                 $('#kpi-container').html('');
             }

             // update Likert dictionary
             var $container;

             // TODO: un-comment for likert dictionary matching
             // $container = $('<div class="row likert-dict"></div>');
             // for (var i in data['likert_dict']) {
             //     $container.append('<div class="col-xs-6">' + i + '  -  ' + data['likert_dict'][i] + '</div>')
             // }
             // $dictContainer.append($container);

             // TODO: un-comment for likert statistical values
             // $container = $('<div class="row likert-stats"></div>');
             // $container.append('<div class="col-xs-12 title">Likert Statistical Values</div>');
             // for (var i in data['likert_values']) {
             //     $container.append('<div class="col-xs-12">'
             //         + '<div class="col-xs-6">' + i + ':</div>'
             //         + '<div class="col-xs-6">' + data['likert_values'][i] + '</div></div>')
             // }
             // $statsContainer.append($container);

             if (data['percentages']) {
                 $container = $('<div class="row likert-stats"></div>');
                 $container.append('<div class="col-xs-12 title">Aggregated Answers</div>');
                 $.each(data['percentages'], function (i, stat) {

                     $container.append('<div class="col-xs-12">'
                         + '<div class="col-xs-6">' + ((stat['Answer'] != '') ? stat['Answer'] : '(No Answer)') + ':</div>'
                         + '<div class="col-xs-6">' + stat['Percentage'] + '%</div></div>')

                 });
                 $statsContainer.append($container)
             }
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
             var $data = $(data);
             $(container).html($data);

             $('#indicators-container').html(
                 $data.siblings('#kpi-table-4').detach()
             );

             $('.kpi-subtitle').html(
                 evaluateKpiSubtitle(
                     'BRAND_VALUE',
                     $('select#table-type-filter option:selected').val()
                 )
             );
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

            $('#number-of-workers').html(data['#_of_workers'] + ' ( ' + data['%_of_workers'] + '% )');
             $('#number-of-managers').html(data['#_of_managers'] + ' ( ' + data['%_of_managers'] + '% )');
             $('#number-of-visitors').html(data['#_of_visitors'] + ' ( ' + data['%_of_visitors'] + '% )');
        }
    })
}

function refreshTable() {
    var val = $('#table-type-filter').find('option:selected').data('val').toUpperCase(),
        $table = $('table.analytics-table');

    if ( val ) {
        $table
            .find('tr')
            .removeClass('hidden-type')
            .find('td.subject-type')
            .filter(function () {
                return $(this).text() != val
            })
            .closest('tr')
            .addClass('hidden-type');
    } else {
        $table
            .find('tr')
            .removeClass('hidden-type')
    }

    // Campaign related changes
    var $option = $('#table-campaign-filter').find('option:selected');
    val = $option.data('val').toUpperCase();

    var $mirror = $option.closest('.select-container').find('.selection-mirror');
    if ($mirror.length) {
        $mirror.text($option.text());
    }

    if (val) {

        $table
            .find('tr')
            .removeClass('hidden-campaign')
            .find('td.campaign-name')
            .filter(function () {
                return $(this).text().toUpperCase() != val
            })
            .closest('tr')
            .addClass('hidden-campaign');

        if (!$table
                .find('tbody tr:not(.hidden-campaign)')
                .length
        ) {

            if (!$table.find('.table-placeholder').length) {
                $table
                    .find('tbody')
                    .append('<tr class="table-placeholder"></tr>')
                    .find('.table-placeholder')
                    .append('<h5 class="text-center">No results were found</h5>')
            }
        } else {
            $table
                .find('.table-placeholder')
                .remove()
        }
    } else {
        $table
            .find('tr')
            .removeClass('hidden-campaign')
    }

    // choose which table to show
    var $tableChoiceSelector = $('select#table-choice');

    if (!$tableChoiceSelector.length) {
        return;
    }

    var $selectedIdx = $tableChoiceSelector.find('option:selected').index();

    $table.addClass('hidden');
    $table.eq($selectedIdx).removeClass('hidden');
}

$(document).ready(function() {
    // select & checkbox initialization
    $('select').chosen();

    if(window.location.href.indexOf('workers-sentiment') > -1) {
        drawChart('#chartContainer', '/analytics/workers-sentiment-charts/1/');
        drawStats('#statsContainer', '/analytics/workers-sentiment-stats/1/');
    }

    if(window.location.href.indexOf('brand-value') > -1) {
        updateBrandValueTable('#brand-value-table-container', '/analytics/brand-value-charts/');
    }
    
    $('select.ws-filter, input#chart-unique-answers-filter').on('change',
        function() {
            var that = this,
                selectedVariable = $(this).find('option:selected').data('varname'),
                urlParamString = '?';


            $('select > option[data-varname=' + selectedVariable + '][value=' + this.value + ']')
                .closest('select')
                .not(this)
                .each(function(i, sel) {
                    sel.value = that.value;
                    $(sel).trigger("chosen:updated");

            });

            $.each($('select.ws-filter, input#chart-unique-answers-filter'), function(i, sel) {
                if ($(sel).is('select')) {

                    var $option = $(sel).find('option:selected'),
                        varname = $option.data('varname'),
                        val = $option.val();

                    var $mirror = $(sel).closest('.select-container').find('.selection-mirror');
                    if ($mirror.length) {
                        $mirror.text($option.text());
                    }
                }
                else {
                    var varname = $(sel).data('varname'),
                        val = $(sel).prop('checked');
                }

                if ((val) && (varname != undefined) && urlParamString.indexOf(varname) < 0) {
                    if (urlParamString.length != 1) {
                        urlParamString += '&';
                    }

                    urlParamString += varname + '=' + val;
                }
            });

            var $option = $('select#chart-choice').find('option:selected'),
                chartChoice = $option.index() + 1;

            var endpointURL = chartChoice + '/' + urlParamString;
            drawChart('#chartContainer', '/analytics/workers-sentiment-charts/' + endpointURL, chartChoice);
            drawStats('#statsContainer', '/analytics/workers-sentiment-stats/' + endpointURL);
            refreshTable();
    });

    $('select.bv-filter, input#brand-table-unique-answers-filter').on('change',
        function() {
            var urlParamString = '?';
            var selectedVariable = $(this).find('option:selected').data('varname');

            var that = this;
            $('select > option[data-varname=' + selectedVariable + '][value=' + this.value + ']')
                .closest('select')
                .not(this)
                .each(function(i, sel) {
                    sel.value = that.value;
                    $(sel).trigger("chosen:updated");

            });

            $.each($('select.bv-filter, input#brand-table-unique-answers-filter'), function(i, sel) {
                if ($(sel).is('select')) {

                    var $option = $(sel).find('option:selected'),
                        varname = $option.data('varname'),
                        val = $option.val();

                    var $mirror = $(sel).closest('.select-container').find('.selection-mirror');
                    if ($mirror.length) {
                        $mirror.text($option.text());
                    }
                }
                else {
                    var varname = $(sel).data('varname'),
                        val = $(sel).prop('checked');
                }

                if ((val) && (varname != undefined) && urlParamString.indexOf(varname) < 0) {
                    if (urlParamString.length != 1) {
                        urlParamString += '&';
                    }

                    urlParamString += varname + '=' + val;
                }
            });

            var endpointURL = '/analytics/brand-value-charts/'+ urlParamString;
            updateBrandValueTable('#brand-value-table-container', endpointURL);
            refreshTable();
    });

    $('body.analytics-page h4 .toggle-section').on('click', function() {
        $(this)
            .closest('h4')
            .toggleClass('collapsed')
            .find('i')
            .toggleClass('fa-chevron-up fa-chevron-down')
    });
});



$('body').on('click', '#workers-sentiment-detailed-results--excel', function(e) {
    var val = $('#table-campaign-filter').find('option:selected').data('pk');
    window.location.href = '/analytics/workers-sentiment-export?campaign=' + (val ? val : '');
});

$('body').on('click', '#brand-values-detailed-results--excel', function(e) {
    var val = $('#table-campaign-filter').find('option:selected').data('pk');
    window.location.href = '/analytics/brand-values-export?campaign=' + (val ? val : '');
});