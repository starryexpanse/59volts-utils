#!/bin/bash

# Usage:
# checkupstatus DOMAIN PORT N SERVICE_NAME EMAILADDR [EMAILADDR]...
#
# Poor man's uptime monitoring
# We send an email if after N checks, the specified 
# domain name is unreachable

function main {
    local domain="$1"
    local port="$2"
    local n="$3"
    local service="$4"
    local emails=${@:5}

    netcat -w 10 -z "$domain" "$port"
    local status=$?

    local datadir="/var/checkupstatus"
    local file="$datadir/$domain:$port"

    if [[ ! -f "$file" ]]; then
        echo 0 > "$file"
    fi

    local saved_num="$(cat "$file" | sed 's/[^0-9]//g')"
    local new_saved_num=saved_num


    if [[ $status -eq 0  ]]; then
        # Host is up!
        echo 0 > "$file"
    else
        # Host seems to be down...
        new_saved_num=$(($saved_num+1))
        echo "$new_saved_num" > "$file"

        if [[ $new_saved_num -ge $n ]]; then
            for email in $emails; do
                php -r '$domain=$argv[1];$email=$argv[2];$port=$argv[3];$service=$argv[4];mail($email, "$domain is down", "Service \"$service\" seems to be down; I could not reach $domain on port $port.\n\nSorry :(\n\n-checkupstatus script");' "$domain" "$email" "$port" "$service"
            done
        fi

    fi
}

main $@
