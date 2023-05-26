{% load static %}
{% load i18n %}
<script>
	

	$(document).ready(function() {
		// Form ============================================================
		$('#id_form').submit(function(){
			// Prevent multiple submits
	        if ($.data(this, 'submitted')) return false;
			
			// Loading Alert
			swal({
                  position: 'top-end',
                  type:'warning',
                  html:'<div><div><h3>{% trans "Store Data"%}</h3></div><div><label>{% trans "Storing data on progress .." %}</label></div></div>',
                  showConfirmButton: false
                });
			swal.showLoading();
			$.data(this, 'submitted', true); // mark form as submitted.
	        return true;
		});
		// End Form ========================================================
			
     });
	
	 //====================================================================
	 // Get City when university changed
	 // Input Params ID University selected
	 // Target $('#id_level')
	 // ====================================================================
	 function university_on_changed(){
		 var pk_university = '{{university.pk}}'; //$('#id_university').val();
		
		 var data = new FormData();
         data.append("csrfmiddlewaretoken", '{{ csrf_token }}');
         data.append("pk_university", pk_university);
         data.append("is_filter", true);
         data.append("obj_name", "level");
        
         $.ajax({
            url: "{% url 'masters:ajax_level_university_on_changed' %}",
            cache: false,
            contentType: false,
            processData: false,
            data: data,
            type: "POST",
            success: function(data) {
            	// Get ID LEVEL
            	var id_level_selected = $('#id_level').val();
            	
            	// Replace Level
	    		$('#id_level').replaceWith(data.level_field);
	    		
	    		// Set if any selected before
	    		$('#id_level').val(id_level_selected);
	    		$("#id_level").select2({ width: '100%' });
            	  
            },
            error: function(data) {
                console.log(data);
            }
        });
	 }
	
	 university_on_changed();
	
	 // select2
	 $("#id_level").select2({ width: '100%' });
	 
</script>