<html>
<head>
  <title>NQueue </title>
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
    <%include file="admin_header.mako"/>
    
    Owner Businesses <br>
    <select id='owners' multiple='multiple' name='owners[]'>
      %for value in b_list:
        <option value="${value['_id']}">${value['name']}</option>
      %endfor  
    </select>
    
    Employee Businesses <br>
    <select id='employees' multiple='multiple' name='employees[]'>
      %for value in b_list:
        <option value="${value['_id']}">${value['name']}</option>
      %endfor  
    </select>
    <script src="${request.static_url('innovation:static/multi_select/js/jquery.multi-select.js')}" type="text/javascript"></script>

    <select id='permissions' multiple='multiple' name='permissions[]'>
      <option value="administrators">Super Administrators</option>
      <option value="b_admins">Business Admins</option>
      <option value="b_queuers">Business Queuers</option>
    </select>


    <form id='add_to_queue' action=#>
      ID / Name : <input type="text" id="new_name"><br>
      Password : <input type="text" id="new_password"><br>
      <input type="submit" value="Submit" id="add_button" class="btn">
      <label class="error" for="client_id_manual" id="name_error">You need to input a name!</label><br>
    </form>

  </center>
  <script>
  $('#employees').multiSelect();
  $('#owners').multiSelect();
  $('#permissions').multiSelect();
  $('.error').hide();  

  $(document).ready(function(){
    $("#add_button").click(function(){
      var c_id = $("#new_name").val();
      var password = $("#new_password").val();
      var employee = $('#employees').val();
      var owner = $('#owners').val();
      var permission= [];
      $('#permissions :selected').each(function(i, selected){ 
        permission[i] = $(selected).val(); 
        });


      if (c_id == "") {
        $("label#name_error").show();
        $("#name_error").focus();
        return false;
      }
      $.ajax({
        type:"POST",
        url: "${request.route_url('admin_add_user')}",
        data:{ employees : employee, name : c_id, p_word : password, owners : owner, permissions : permission }, 
        success:function(result){
          $('.error').hide();  
          if (result == 'OK') {
            console.log("Successful");
            alert("User added successfully!");
          }
          if (result == 'NO') {
            console.log("Unsuccessful");
          }
        }
        });
    });
  });
  </script>
</body>
</html>


