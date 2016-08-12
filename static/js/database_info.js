$(function () {
    var info_types = new Array();
    info_types[0] = "relation";
    info_types[1] = "graph";

    for (i = 0;i < info_types.length; i++)
    {
        $('#database_' + info_types[i]).collapse('hide');

        $('#label_' + info_types[i] + '_panel button#add_' + info_types[i] + '_label').on('click', '', info_types[i], addLabel);
    }
});

function addLabel(event)
{
    var info_type = event.data;
    var table_name = $('input#' + info_type + '_input').val();

    if (table_name.length == 0)
    {
        if ($('#' + info_type + '_message').length == 0)
        {
            $('#label_' + info_type + '_panel hr#' + info_type + '_sep_line').after('<div id="' + info_type + '_message" class="alert alert-danger alert-dismissible" role="alert"><button type="button" class="close" data-dismiss="alert"> &times;</span></button><strong>Warning!</strong> Empty input! </div>');
        }
    }
    else
    {
        $('#' + info_type + '_message').remove(); 

        $('#label_' + info_type + '_panel hr#' + info_type + '_sep_line').before('<button type="button" class="btn btn-default btn-xs" > ' + table_name + ' <a onclick="removeLabel(this);"> <span class="glyphicon glyphicon-remove-sign"></span></a>');
    }
}

function removeLabel(label) 
{
    label.parentNode.remove();
    return false;
}

function addDatabaseInfoTab()
{
    //add one new tab
    $('#query_add a[role="button"]').click();
    //focus on the new tab
    var tab_id_str = $('ul#query_tab li:eq(-2)').attr('id');
    var tab_index = tab_id_str.slice(5);
    return tab_index;
}

function relationCoreInfo()
{
    var expand_relation_core = ($('#relation_core_info').attr('class') == 'collapsed');
    if (expand_relation_core)
    {
        var tab_index = addDatabaseInfoTab();

        //clear query input textarea and buttion
        $('#query_form' + tab_index).html('<div class="alert alert-info text-center" role="alert"> <strong> Relation Core Information </strong> </div>');

        //query tab name
        $('#query_tab_name' + tab_index).html("Relation...");

        //add loading progress
        addLoadingAnimation(tab_index);

        var args = {'tab_index': tab_index};
        $.ajax({url: '/get_relation_core_info', data: $.param(args), dataType: 'json', type: 'POST',
            success: querySuccess, error: queryError
        });
    }
}

function graphViewInfo()
{
    var expand_graph_core = ($('#graph_view_info').attr('class') == 'collapsed');
    if (expand_graph_core)
    {
        var tab_index = addDatabaseInfoTab();

        //clear query input textarea and buttion
        $('#query_form' + tab_index).html('<div class="alert alert-info text-center" role="alert"> <strong> Graphical View Information </strong> </div>');

        //query tab name
        $('#query_tab_name' + tab_index).html("Graphical...");

        //add loading progress
        addLoadingAnimation(tab_index);

        var args = {'tab_index': tab_index};
        $.ajax({url: '/get_graphical_view_info', data: $.param(args), dataType: 'json', type: 'POST',
            success: querySuccess, error: queryError
        });
    }
}
