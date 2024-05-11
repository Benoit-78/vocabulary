


mysqldump \
    -u [username] \
    -p[password] \
    [database_name] > backup.sql

mariabackup \
    --user=[username] \
    --password=[password] \
    --backup \
    --target-dir=/path/to/backup/directory



mysql \
    -u [username] \
    -p[password] \
    [database_name] < backup.sql

mariabackup \
    --prepare \
    --target-dir=/path/to/backup/directory