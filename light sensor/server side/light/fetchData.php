<?php
// Connecting, selecting database
$dbconn = pg_connect( "host=slackbox dbname=sensor user=pi password='raspberry'" );
// Performing SQL query
$query  = //'SELECT * FROM light';
"SELECT DATE_TRUNC('hour', time) AS time, AVG(value) AS value FROM sensors WHERE (id = $1) GROUP by DATE_TRUNC('hour',time) ORDER BY time LIMIT 100";
$result = pg_query_params( $dbconn, $query, explode(' ',$_POST['id']) ) or die( 'Query failed: ' . pg_last_error() );
$rows = array( );
while ( $line = pg_fetch_array( $result, null, PGSQL_ASSOC ) ) {
    $rows[ ] = $line;
}
print json_encode( $rows );
// Free resultset
pg_free_result( $result );
// Closing connection
pg_close( $dbconn );
?>
 
