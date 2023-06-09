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
	 // Get Paroki when Keuskupan changed
	 // Input Params ID Keuskupan selected
	 // Target $('#id_paroki')
	 // ====================================================================
	 function paroki_on_changed(){
		 var pk_keuskupan = $('#id_keuskupan').val();
		
		 var data = new FormData();
         data.append("csrfmiddlewaretoken", '{{ csrf_token }}');
         data.append("pk_keuskupan", pk_keuskupan);
         data.append("is_filter", false);
         data.append("obj_name", "paroki");
        
         $.ajax({
            url: "{% url 'masters:ajax_post_paroki_change' %}",
            cache: false,
            contentType: false,
            processData: false,
            data: data,
            type: "POST",
            success: function(data) {
            	// Get ID LEVEL
            	var id_paroki_selected = $('#id_paroki').val();
            	
            	// Replace Level
	    		$('#id_paroki').replaceWith(data.paroki_field);
	    		
	    		// Set if any selected before
	    		$('#id_paroki').val(id_paroki_selected);
	    		$("#id_paroki").select2({ width: '100%' });
            	  
            },
            error: function(data) {
                console.log(data);
            }
        });
	 }
	
	 paroki_on_changed();
	 
	 //====================================================================
	 // Get Wilayah when Paroki changed
	 // Input Params ID Paroki selected
	 // Target $('#id_wilayah')
	 // ====================================================================
	 function wilayah_on_changed(){
		 var pk_paroki = $('#id_paroki').val();
		
		 var data = new FormData();
         data.append("csrfmiddlewaretoken", '{{ csrf_token }}');
         data.append("pk_paroki", pk_paroki);
         data.append("is_filter", false);
         data.append("obj_name", "wilayah");
        
         $.ajax({
            url: "{% url 'masters:ajax_post_wilayah_change' %}",
            cache: false,
            contentType: false,
            processData: false,
            data: data,
            type: "POST",
            success: function(data) {
            	// Get ID LEVEL
            	var id_wilayah_selected = $('#id_wilayah').val();
            	
            	// Replace Level
	    		$('#id_wilayah').replaceWith(data.wilayah_field);
	    		
	    		// Set if any selected before
	    		$('#id_wilayah').val(id_wilayah_selected);
	    		$("#id_wilayah").select2({ width: '100%' });
            	  
            },
            error: function(data) {
                console.log(data);
            }
        });
	 }
	
	 wilayah_on_changed();
	 
	 //====================================================================
	 // Get Lingkungan when Wilayah changed
	 // Input Params ID Wilayah selected
	 // Target $('#id_lingkungan')
	 // ====================================================================
	 function lingkungan_on_changed(){
		 var pk_wilayah = $('#id_wilayah').val();
		
		 var data = new FormData();
         data.append("csrfmiddlewaretoken", '{{ csrf_token }}');
         data.append("pk_wilayah", pk_wilayah);
         data.append("is_filter", false);
         data.append("obj_name", "lingkungan");
        
         $.ajax({
            url: "{% url 'masters:ajax_post_lingkungan_change' %}",
            cache: false,
            contentType: false,
            processData: false,
            data: data,
            type: "POST",
            success: function(data) {
            	// Get ID LEVEL
            	var id_lingkungan_selected = $('#id_lingkungan').val();
            	
            	// Replace Level
	    		$('#id_lingkungan').replaceWith(data.lingkungan_field);
	    		
	    		// Set if any selected before
	    		$('#id_lingkungan').val(id_lingkungan_selected);
	    		$("#id_lingkungan").select2({ width: '100%' });
            	  
            },
            error: function(data) {
                console.log(data);
            }
        });
	 }
	
	 lingkungan_on_changed();
	
	 // select2
	 $("#id_keuskupan").select2({ width: '100%' });
	 $("#id_paroki").select2({ width: '100%' });
	 $("#id_wilayah").select2({ width: '100%' });
	 $("#id_lingkungan").select2({ width: '100%' });
	 $("#id_gender").select2({ width: '100%' });
	 
</script>