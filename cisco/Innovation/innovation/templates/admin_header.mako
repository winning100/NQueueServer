<link href="${request.static_url('innovation:static/generic.css')}" rel="stylesheet" media="screen">
<div class="navbar navbar-fixed-top navbar-inverse">
  <div class="navbar-inner">
    <div class="container"
      <span> Business Management </span>
      <a class="link-header" href="${request.route_url('admin_add_business')}">Add Business</a>
      <a class="link-header" href="${request.route_url('admin_edit_business')}">Edit Business</a>
      <a class="link-header" href="${request.route_url('admin_add_user')}">Add User</a>
      <a class="link-header" href="${request.route_url('admin_edit_user')}">Add User</a>
      <a class="link-header" href="${request.route_url('logout')}">Logout</a>
    </div>
  </div>
</div>

