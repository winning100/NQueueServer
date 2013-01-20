<html>
<head>
  <title>NQueue | Manage All Businesses</title>
  <meta http-equiv="Content-Type" content="text/html;charset=UTF-8"/>
  <meta name="keywords" content="python web application" />
  <meta name="description" content="NQueue Management" />
  <script src="http://code.jquery.com/jquery-1.8.3.js"></script>
  <script src="http://code.jquery.com/ui/1.9.2/jquery-ui.js"></script>
  <link href="${request.static_url('innovation:static/bootstrap/css/bootstrap.min.css')}" rel="stylesheet" media="screen">
  <link href="${request.static_url('innovation:static/multi_select/css/multi-select.css')}" media="screen" rel="stylesheet" type="text/css">
</head>
<body>
  <center>
    <%include file="header.mako"/>
    
    <select id='options' multiple='multiple' name='options[]'>
      %for value in b_list:
        <option value="${value['_id']}">${value['name']}</option>
      %endfor  
    </select>
    <script src="${request.static_url('innovation:static/multi_select/js/jquery.multi-select.js')}" type="text/javascript"></script>

    <form id='add_to_queue' action=#>
      ID / Name : <input type="text" id="new_name"><br>
      Password : <input type="text" id="new_password"><br>
      <input type="submit" value="Submit" id="add_button" class="btn">
      <label class="error" for="client_id_manual" id="name_error">You need to input a name!</label><br>
    </form>

  </center>
  <script>
  $('#options').multiSelect();
  $('.error').hide();  

  $(document).ready(function(){
    $("#add_button").click(function(){
      var c_id = $("#new_name").val();
      var password = $("#new_password").val();
      var options= $('#options').find(":selected").val();
      if (c_id == "") {
        $("label#name_error").show();
        $("#name_error").focus();
        return false;
      }
      $.ajax({
        type:"POST",
        url: "${request.route_url('add_employee')}",
        data:{ b_name : options, name : c_id, p_word : password }, 
        success:function(result){
          $('.error').hide();  
          console.log("Successful");
        }
        });
    });
  });
  </script>
</body>
</html>

