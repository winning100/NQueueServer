<html>
<head>
  <title>NQueue | ${b_name} Management</title>
  <meta http-equiv="Content-Type" content="text/html;charset=UTF-8"/>
  <meta name="keywords" content="python web application" />
  <meta name="description" content="NQueue Management" />
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js" type="text/javascript"></script>
  <link href="${request.static_url('innovation:static/multi_select/css/multi-select.css')}" media="screen" rel="stylesheet" type="text/css">
</head>
<body>
  <center>
    <%include file="header.mako"/>
    <div class="ms-selectable">
    <select id='Callbacks' multiple='multiple' name='options[]'>
      <option value='1234'>Joe S</option>
      <option value='5678'>Bertha B2</option>
      <option value='sdfg3'>Lisa M</option>
      <option value='gfs_4'>Bart S</option>
      <option value='gfds0'>Steve F</option>
    </select>
    <script src="${request.static_url('innovation:static/multi_select/js/jquery.multi-select.js')}" type="text/javascript"></script>
    </div>

<script>

  function getCD(text) {
    $('html').append('<div id="confirmDialog"><p>' + text + '</p></div>');
    var confirmDialog = $('#confirmDialog');
   confirmDialog .dialog({
        modal: true,
        autoOpen: false,
        title: 'Make a selection',
        width: 300,
        height: 180,
        buttons: {
            'OK': function() {
                $(this).remove();
            },
            'Cancel': function() {
                $(this).remove();
            }
        }
    });

    confirmDialog.dialog('open');
}


  $('#Callbacks').multiSelect({
    afterDeselect: function(value, text){
      //alert("Deselect value: "+value);
      getCD('Please make a selection');
    }
  });
</script>


</center>
</body>
</html>
