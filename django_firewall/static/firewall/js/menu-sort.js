// Puts the included jQuery into our own namespace
var firewall = {
    "jQuery": jQuery.noConflict(true)
};

firewall.jQuery(document).ready(function() {
	
    // Set this to the name of the column holding the position
    pos_field = 'position';
    
    // Determine the column number of the position field
    pos_col = null;
    
    cols = firewall.jQuery('#result_list tbody tr:first').children()
    
    for (i = 0; i < cols.length; i++) {
        inputs = firewall.jQuery(cols[i]).find('input[name*=' + pos_field + ']')
        
        if (inputs.length > 0) {
            // Found!
            pos_col = i;
            break;
        }
    }
    
    if (pos_col == null) {
        return;
    }
    
    // Some visual enhancements
    header = firewall.jQuery('#result_list thead tr').children()[pos_col]
    firewall.jQuery(header).css('width', '1em')
    firewall.jQuery(header).children('a').text('#')
    
    // Hide position field
    firewall.jQuery('#result_list tbody tr').each(function(index) {
        pos_td = firewall.jQuery(this).children()[pos_col]
        input = firewall.jQuery(pos_td).children('input').first()
        //input.attr('type', 'hidden')
        input.hide()
        
        label = firewall.jQuery('<strong>' + input.attr('value') + '</strong>')
        firewall.jQuery(pos_td).append(label)
    });
    
    // Determine sorted column and order
    sorted = firewall.jQuery('#result_list thead th.sorted')
    sorted_col = firewall.jQuery('#result_list thead th').index(sorted)
    sort_order = sorted.hasClass('descending') ? 'desc' : 'asc';
    
    if (sorted_col != pos_col) {
        // Sorted column is not position column, bail out
        console.info("Sorted column is not %s, bailing out", pos_field);
        return;
    }
    
    firewall.jQuery('#result_list tbody tr').css('cursor', 'move')
    
	var sortLock = function(e, ui) {
	
		var widths = [];
		ui.children().each(function() {
			widths[widths.length] = firewall.jQuery(this).width();
		});
	
		var row = ui.clone();
		var i = 0;
		row.children().each(function() {
			firewall.jQuery(this).width(widths[i]);
			i++;
		});
		
		return row;
	};
    
    // Make tbody > tr sortable
    firewall.jQuery('#result_list tbody').sortable({
        helper: sortLock,
        revert: true,
        axis: 'y',
        items: 'tr',
        cursor: 'move',
        update: function(event, ui) {
            item = ui.item
            items = firewall.jQuery(this).find('tr').get()
            
            if (sort_order == 'desc') {
                // Reverse order
                items.reverse()
            }
            
            firewall.jQuery(items).each(function(index) {
                pos_td = firewall.jQuery(this).children()[pos_col]
                input = firewall.jQuery(pos_td).children('input').first()
                label = firewall.jQuery(pos_td).children('strong').first()
                
                input.attr('value', index)
                label.text(index)
            });
            
            // Update row classes
            firewall.jQuery(this).find('tr').removeClass('row1').removeClass('row2')
            firewall.jQuery(this).find('tr:even').addClass('row1')
            firewall.jQuery(this).find('tr:odd').addClass('row2')
        }
    });
    
});