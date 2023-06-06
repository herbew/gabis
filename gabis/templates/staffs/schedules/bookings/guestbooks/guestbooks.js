{% load static %}
{% load i18n %}
<script>
	
		//====================================================================
		// Address Upload File
		// Input Params -files
		// Target $('#id_description').summernote
		// ====================================================================
		function description_upload_file(files) {
		    var data = new FormData();
		    data.append("csrfmiddlewaretoken", '{{ csrf_token }}');
		    data.append("files", files);
		    
		    $.ajax({
		        url: "{% url 'trails:summernotes_upload_files' %}",
		        cache: false,
		        contentType: false,
		        processData: false,
		        data: data,
		        type: "POST",
		        success: function(data) {
		        	if(data.status==200){
		        		var url_image = data.url;
		        		console.log(url_image);
		        		console.log(data.path_gs);
		        		// replace image with src-------------------------------
		        		var image = $('<img>').attr('src', url_image).addClass("img-fluid");
		        		$('#id_description').summernote("insertNode", image[0]);
		        		
		        	}else if (data.status==201){
		        		// Error File limitation
		        		swal(
			                '{% trans "Error Upload File" %}',
							data.content,
			                   'error'
			              );
		        	}
		            
		        },
		        error: function(data) {
		            console.log(data);
		        }
		    });
		}
		
		// ====================================================================
		// Description Upload File
		// Input Params -target.src
		// ====================================================================
		function description_delete_file(target) {
		    var data = new FormData();
		    data.append("csrfmiddlewaretoken", '{{ csrf_token }}');
		    data.append("url", target);
		    
		    $.ajax({
		        url: "{% url 'trails:summernotes_delete_files' %}",
		        cache: false,
		        contentType: false,
		        processData: false,
		        data: data,
		        type: "POST",
		        success: function(data) {
		        	if(data.status==200){
		        		swal(
				             '{% trans "Delete File" %}',
							  data.content,
				              'success'
				              );
		        		
		        	}else if (data.status==201){
		        		// Error File limitation
		        		swal(
			                '{% trans "Error Delete File" %}',
							data.content,
			                'error'
			              );
		        	}
		            
		        },
		        error: function(data) {
		            console.log(data);
		        }
		    });
		}


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
			
		// Description =====================================================
		$('#id_description').summernote({
            height : 300,
            
            // Image -------------------------------------------------------
	        callbacks:{
	              onImageUpload:function(files){
		            	description_upload_file(files[0]);
		            },
		          onMediaDelete : function(target) {
		                description_delete_file(target[0].src);
		            }
	        },
	        
	        
	        // Popup -------------------------------------------------------  
            popover: {
                  image: [
                    ['image', ['resizeFull', 'resizeHalf', 'resizeQuarter', 'resizeNone']],
                    ['float', ['floatLeft', 'floatRight', 'floatNone']],
                    ['remove', ['removeMedia']]
                  ],
                  link: [
                    ['link', ['linkDialogShow', 'unlink']]
                  ],
                  table: [
                    ['add', ['addRowDown', 'addRowUp', 'addColLeft', 'addColRight']],
                    ['delete', ['deleteRow', 'deleteCol', 'deleteTable']],
                  ],
                  air: [
                    ['color', ['color']],
                    ['font', ['bold', 'underline', 'clear']],
                    ['para', ['ul', 'paragraph']],
                    ['table', ['table']],
                    ['insert', ['link', 'picture']]
                    
                      ]
                    },
                    
            // Popup -------------------------------------------------------        
            toolbar: [
                ['style', ['style']],
                ['font', ['bold', 'underline', 'clear', 'strikethrough', 'superscript', 'subscript']],
                ['fontname', ['fontname']],
                ['color', ['color']],
                ['para', ['ul', 'ol', 'paragraph']],
                ['table', ['table']],
                ['insert', ['link', 'picture', 'video']],
                ['view', ['fullscreen', 'codeview', 'help']],
              ],
              
        	placeholder: '{% trans "Description of Document ..." %}',  
            
		});
        // End Description =================================================
		
     });
	
	$("#id_typed").select2({ width: '100%' });
	 
</script>