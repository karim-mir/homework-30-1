FROM nginx:latest

COPY nginx.conf /etc/nginx/nginx.conf

COPY html/ /user/share/nginx/html/

EXPOSE 80