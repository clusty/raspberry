<?php
// Connecting, selecting database
$dbconn = pg_connect( "host=slackbox dbname=sensor user=pi password='raspberry'" );
// Performing SQL query
$query  = //'SELECT * FROM light';
    "SELECT DATE_TRUNC('hour', timestamp) AS timestamp, AVG(value) AS value FROM light WHERE timestamp > NOW()-INTERVAL '24 hours' GROUP by DATE_TRUNC('hour',timestamp) ORDER BY timestamp";
$result = pg_query( $query ) or die( 'Query failed: ' . pg_last_error() );
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

