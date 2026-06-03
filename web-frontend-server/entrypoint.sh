#!/bin/sh
INSTANCE=${SERVER_INSTANCE:-1}

if [ "$INSTANCE" = "2" ]; then
  COLOR="background:#10b981"
else
  COLOR="background:#3b82f6"
fi

# Match <body ...> với bất kỳ attributes nào
sed -i "s|<body|<body><div style='background:red;color:white;text-align:center;padding:10px;'>INSTANCE ${INSTANCE}</div>|" /usr/share/nginx/html/index1.html
nginx -g "daemon off;"