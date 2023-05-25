/* ===========================================================
1. Event return float with .
   /^-?\d+(?:[.,]\d*?)?$/ --> with . or ,
2. 'onkeypress':'return isFloat("n")'
=========================================================== */
function isFloat(n) {
            var floatRegex = /^-?\d+(?:[.]\d*?)?$/;
            if (!floatRegex.test(n))
                return false;
            return true;
        }

/* ===========================================================
1. Event return number
2. 'onkeypress':'return isNumberKey(event)'
=========================================================== */
function isNumberKey(evt)
  {
     var charCode = (evt.which) ? evt.which : event.keyCode
     if (charCode > 31 && (charCode < 48 || charCode > 57))
        return false;

     return true;
  }

/* ===========================================================
1. Event return number
2. 'onkeypress':'return isNumberKey(event)'
=========================================================== */
function isNumberDotKey(evt)
  {
     var charCode = (evt.which) ? evt.which : event.keyCode
     if (charCode > 31 && (charCode < 48 || charCode > 57))
    	
    	 if (charCode == 46){
    		 return true;
    	 }else{
    		 return false;
    	 }

     return true;
  }
          
/* ===========================================================
1. Convert Number to IDR Format
2. $('#component').on("keyup", function () {
              $(this).val(number_to_idr($(this).val()));
    });
=========================================================== */
function number_to_idr(v){
    if (v){
        v = parseInt(v.replace(/,.*|\D/g,''),10)
        var rev     = parseInt(v, 10).toString().split('').reverse().join('');
        var rev2    = '';
        for(var i = 0; i < rev.length; i++){
            rev2  += rev[i];
            if((i + 1) % 3 === 0 && i !== (rev.length - 1)){
                rev2 += '.';
            }
        }
        return rev2.split('').reverse().join('');
    }else{
        return "";
    }
}

/* ===========================================================
1. TOAST Alert django messages
2. INPUT :
	- heading = '{{message.tags}}'
	- text = '{{ message }}' 
	- icon = '{{message.tags}}'
=========================================================== */
function toast_alert(heading, text, icon){
    $.toast({
        heading:heading,
        text:text,
        showHideTransition: 'slide',
        icon:icon
    })
}

/* ===========================================================
1. REDIRECT URL
2. INPUT :
	- url
=========================================================== */
function redirect_url_no_params(url){
	window.location.href=url;
}
function redirect_url_with_params(url){
	window.location.href=url;
}
function redirect_new_window(url){
		window.open(url, "_blank");
	}
	
function redirect_download(url){
    window.location.href = url;
}
//====================================================================
//INFO DATA
//Params, created, modified, userupdated
//====================================================================
function data_info(no,created, modified, user){
	swal(
		{
         title:'# '+no,
         html:
        	 '<div class="row">'+
        	 '<div class="col-md-12 text-left"><small>'+
        	 '<lable>'+created+' WIB</lable><br>'+
         	 '<lable>'+modified+' WIB </lable><br>'+
         	 '</small></div>'+
         	 '</div>'+
         	 '<div class="row">'+
         	 '<div class="col-md-12 text-right"><small>'+
         	 '<lable><b>'+user+'</b></lable>'+
         	 '</small></div>'+
         	 '</div>',
         type:'info'
         }
     )
}
          