<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" xmlns:tal="http://xml.zope.org/namespaces/tal">
<head>
  <title>Administration Area </title>
  <meta http-equiv="Content-Type" content="text/html;charset=UTF-8"/>
  <meta name="keywords" content="python web application" />
  <meta name="description" content="pyramid web application" />
  
</head>

<body>
  <div id="login_form" xmlns="http://www.w3.org/1999/xhtml">
    <form id="login_form" action="${url}" method="post" >
    <h2>Log In</h2>
    <fieldset>
        <input name="_csrf" type="hidden" value="${request.session.get_csrf_token()}">
        <input type="hidden" name="came_from" value="${came_from}"/>
        <label for="login">Username:</label> <input type="text" name="login" value="${login}"/>
        <label for="password">Password:</label> <input type="password" name="password" value="${password}"/>
        <input type="submit" class="login" name="form.submit" value="Log In"/>
    </fieldset>
    </form>
    ${message}
</div>

</body>
</html>
