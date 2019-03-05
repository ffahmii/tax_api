FROM mysql:5.7

ENV MYSQL_DATABASE=test_shopee

COPY ./init.sql /docker-entrypoint-initdb.d/init.sql

EXPOSE 3306
CMD ["mysqld"]
