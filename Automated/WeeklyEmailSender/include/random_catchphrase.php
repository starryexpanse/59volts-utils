<?php

$creds = include('config.php');

function getResults($start) {
    global $creds;
    $url = "https://www.googleapis.com/customsearch/v1?"
            . 'key=' . urlencode($creds['key'])
            . '&cx=' . urlencode($creds['cx'])
            . '&userIp=' . urlencode($creds['ip'])
            . '&alt=json'
            . '&q=' . urlencode('"as * of mine * used to * say" OR "as I always * say"')
            . "&start=$start"
            ;

    $out = shell_exec('curl -4 ' . escapeshellarg($url) . ' 2>/dev/null');

    $out = json_decode($out);

    return $out;
};

function random_catchphrase() {
    // This could throw a lot of errors,
    // but it's wrapped in a try/catch so whatever :P
    $initial = getResults(1);
    $initial = $initial->queries->request;
    $initial = $initial[0];
    $initial = $initial->totalResults;
    $numResults = (int)$initial;
    $page = rand(0, min(10, floor($numResults/10)));
    $randStart = $page*10+1;
    $results = getResults($randStart);
    var_dump($results);
    $results = $results->items;
    if (!count($results)) {
        return null;
    }
    else {
        return $results[rand(0, count($results)-1)]->snippet;
    }
}

function getCatchphrase() {
    $catchphrase = null;
    for ($i = 0; $i < 20; $i++) {
        echo 'iter';
        try {
            $catchphrase = random_catchphrase();
        }
        catch (Exception $e) {
            echo 'fail';
        }
        if (!is_null($catchphrase)) {
            preg_match('/(?:(?:as.+of\W+mine.+used\W+to.+say)|(?:as\W+I\W+always.+say))\W+(\w.+!)/i', $catchphrase, $matches);
            if (count($matches)) {
                var_dump($matches);
                return $matches[count($matches)];
            }
            else {
                var_dump($catchphrase);
            }
        }
    }
    return $catchphrase;
}
