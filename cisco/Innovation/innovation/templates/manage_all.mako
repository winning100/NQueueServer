<html>
<head>
  <title>NQueue | Manage All Businesses</title>
  <meta http-equiv="Content-Type" content="text/html;charset=UTF-8"/>
  <meta name="keywords" content="python web application" />
  <meta name="description" content="NQueue Management" />
  <script src="http://code.jquery.com/jquery-1.8.3.js"></script>
  <script src="http://code.jquery.com/ui/1.9.2/jquery-ui.js"></script>
  <link href="${request.static_url('innovation:static/bootstrap/css/bootstrap.min.css')}" rel="stylesheet" media="screen">
</head>
<body>
  <center>
    <%include file="header.mako"/>
    %for value in b_list:
      ${value['name']} | <a href="${request.route_url('manage',b_id=value['_id']) }">Manage Queue</a>
      %if value['owner'] == 'true':
        | <a href="${request.route_url('manage_employees')}"> Manage Employees</a>
      %endif
      <br>
    %endfor  
  </center>
</body>
</html>

