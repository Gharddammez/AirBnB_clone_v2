# File: 101-setup_web_static.pp

# Ensure the necessary directories are created
file { '/data':
  ensure => 'directory',
}

file { '/data/web_static':
  ensure => 'directory',
}

# Create the necessary subdirectories
file { ['/data/web_static/releases', '/data/web_static/shared']:
  ensure => 'directory',
}

# Create a symbolic link for 'current'
file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test',
}

# Create an index.html file
file { '/data/web_static/releases/test/index.html':
  ensure  => 'file',
  content => '<html>\n  <head>\n  </head>\n  <body>\n    Holberton School\n  </body>\n</html>',
}

# Configure permissions
file { '/data':
  owner => 'ubuntu',
  group => 'ubuntu',
}

file { '/data/web_static':
  owner => 'root',
  group => 'root',
}

file { '/data/web_static/releases':
  owner => 'root',
  group => 'root',
}

file { '/data/web_static/shared':
  owner => 'root',
  group => 'root',
}

file { '/data/web_static/current':
  owner => 'root',
  group => 'root',
}

file { '/data/web_static/releases/test':
  owner => 'root',
  group => 'root',
}

# Notify the user when the setup is complete
notify { 'Web static setup complete':
  message => 'Web static setup complete',
}
