#!/bin/bash

oldpwd="$(pwd)"
cd /var/backups/
mkdir -p blog-content/
cd $_

source "$oldpwd"/Credentials/blog-content-backup.creds.sh

OWNER=root
GROUP=staff

PREFIX="blog-content-"

datetime="$(date +%Y%m%d)"
cleanOld="python /usr/bin/59volts-utils/Scripts/cleanOld.py"

ab_loc="$PREFIX""$datetime"
mkdir "$ab_loc"

rsync -evarcP starryexpanse.com:~web/com/starryexpanse/starryexpanse.com/public "$ab_loc"

rsyncCode=$?

if [[ $rsyncCode = 0 ]]; then
    tar cvzf "$ab_loc".tgz "$ab_loc"
    chown "$OWNER":"$GROUP" "$ab_loc".tgz
else
    echo 'Rsync failed! (exit code '"$rsyncCode"'). Out of disk space?'
    chown "$OWNER":"$GROUP" "$ab_loc"
fi

stem="$(pwd)/$PREFIX"
$cleanOld "${stem}*.tgz"
