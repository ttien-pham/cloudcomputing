FROM nginx:stable
RUN rm -f /etc/nginx/conf.d/default.conf
COPY conf.default /etc/nginx/conf.d/default.conf
COPY html/ /usr/share/nginx/html/
RUN chmod -R 755 /usr/share/nginx/html
EXPOSE 80
RUN cat > /entrypoint.sh << 'EOF'
#!/bin/sh
INSTANCE=${SERVER_INSTANCE:-1}

if [ "$INSTANCE" = "2" ]; then
  COLOR="background:#10b981"
else
  COLOR="background:#3b82f6"
fi

sed -i '/<body/a\
<div style="background:red;color:white;text-align:center;padding:10px;">INSTANCE '"$INSTANCE"'</div>
' /usr/share/nginx/html/index1.html

nginx -g "daemon off;"
EOF
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
