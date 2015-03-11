#!/bin/bash

# Usage:
# checkupstatus DOMAIN N EMAILADDR [EMAILADDR]...
#
# Poor man's uptime monitoring
# We send an email if after N checks, the specified 
# domain name is unreachable

function main {
    local domain="$1"
    local n="$2"
    local emails=${@:3}

    local headers="$(curl -s -S --connect-timeout 10 -I -- "http://$domain")"
    local status=$?
    local response="$(echo "$headers" | grep '^HTTP/')"
    local response_family="$(echo "$response" | cut -c 10)"

    local success=0

    local datadir="/var/checkupstatus"
    local file="$datadir/$domain"

    if [[ ! -f "$file" ]]; then
        echo 0 > "$file"
    fi

    local saved_num="$(cat "$file" | sed 's/[^0-9]//g')"
    local new_saved_num=saved_num


    if [[ $status -eq 0 && ($response_family -eq 3 || $response_family -eq 2) ]]; then
        success=1
    fi

    ###

    if [[ $success ]]; then
        echo 0 > "$file"
    else
        new_saved_num=$(($saved_num+1))
        echo "$new_saved_num" > "$file"

        if [[ $new_saved_num -ge $n ]]; then
            for email in $emails; do
                php -r '$domain=$argv[1];$email=$argv[2];mail($email, "$domain is down", "$domain is replying to my HTTP request with:\n\n$argv[3]\n\nSorry :(\n\n-checkupstatus script");' "$domain" "$email" "$headers"
            done
        fi

    fi
}

main $@
