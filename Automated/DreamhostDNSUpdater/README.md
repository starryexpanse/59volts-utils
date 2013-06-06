DreamhostDNSUpdater
===================

Description
-----------

This utility is run every so often, to update Dreamhost about our various servers' IP addresses, as they may change over time.
If a discrepancy between the current IP address and the IP address on the DNS server (Dreamhost's) is detected, we delete the 
inaccurate record and upload a new one.

Uses
----
This script could be used as an effective replacement for dynamic DNS services like DynDNS&reg;. Some call these types of scripts
"DynDNS updaters."
