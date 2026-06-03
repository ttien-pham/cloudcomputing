FROM mariadb:11

# Copy file SQL khởi tạo vào entrypoint của MariaDB
COPY init/ /docker-entrypoint-initdb.d/

EXPOSE 3306
