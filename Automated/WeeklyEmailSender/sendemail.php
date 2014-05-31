<?php

// require('include/random_catchphrase.php');


// $suffix = "";
// 
// $cap = getCatchphrase();
// if ($cap) {
// 
// }


$mesg = <<<MESSG
It's time for our weekly check-in! Everyone, post what you've done this week!

- MagBot
MESSG;

$supersecret = trim(file_get_contents(dirname(__FILE__) . '/include/emailaddr.conf'));

$additional_headers = 'Content-type: text/plain; charset=utf-8' . "\r\n"
. 'From: MagBot <no-reply@starryexpanse.com>'
. "Reply-To: Starry Expanse Group <$supersecret>";

mail($supersecret, 'Weekly Check-in Email Thread', $mesg, $additional_headers);

