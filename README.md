## Purpose

This is a very basic script that extracts urls from blocklists and converts them to HOSTS syntax used by Pi-Hole.

Some AdGuard lists contain whitelisted domains marked with the prefix "@@" 
(e.g.  `@@¦¦example.com^`)    
These whitelisted domains are ignored.

## How to use

Add the link to a blocklist (in AdGuard syntax) to the *AdGuard_blocklists.csv* and specify a name for the list in the second row.
Then, execute the script.
Running the script will take some time, depending on blocklist sizes and will create the folder *blocklists_converted*.

**The Original repositories are credited in the respective blocklist.**
