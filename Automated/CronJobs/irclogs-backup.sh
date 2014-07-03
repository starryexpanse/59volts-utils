#!/bin/bash

oldpwd="$(pwd)"
cd /var/backups/
mkdir -p db/irclogs
cd $_

source "$oldpwd"/Credentials/irclogs-backup.creds.sh

OWNER=root
GROUP=staff

PREFIX="irclogs-"

datetime="$(date +%Y%m%d)"
cleanOld="python /usr/bin/59volts-utils/Scripts/cleanOld.py"

ab_loc="$PREFIX""$datetime"
mysqldump IrcLogs ab_logs -u"$DB_USER" -p"$DB_PASS" > "$ab_loc".sql
tar cvzf "$ab_loc".tgz "$ab_loc".sql

if [[ $? = 0 ]]; then
    unlink "$ab_loc".sql
    chown "$OWNER":"$GROUP" "$ab_loc".tgz
else
    echo 'Tar failed! (exit code '"$?"'). Out of disk space?'
    chown "$OWNER":"$GROUP" "$ab_loc".sql
fi

stem="$(pwd)/$PREFIX"
$cleanOld "${stem}*.sql"
$cleanOld "${stem}*.tgz"
