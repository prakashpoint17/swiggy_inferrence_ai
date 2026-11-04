-- Create a dedicated read-only MySQL user

CREATE USER 'swiggy_ai'@'localhost'
IDENTIFIED BY 'root';

GRANT SELECT, SHOW VIEW
ON swiggydb_new.*
TO 'swiggy_ai'@'localhost';

FLUSH PRIVILEGES;

