FROM mysql:5.7

ENV MYSQL_DATABASE=testing123

COPY ./init.sql /docker-entrypoint-initdb.d/init.sql

EXPOSE 3306
CMD ["mysqld"]
