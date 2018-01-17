<?php
$db = mysqli_connect("193.93.253.25","codespo","45Pvilfd","codespo_metinstitutt") or die('Feil ved oppkobling til server. ERROR: 109');

$datepick = $_POST['date'];
        $ascdesc = $_POST['ascdesc'];
        $limitby = $_POST['limitby'];

        $query = "SELECT * FROM data_main_min ORDER BY ID DESC LIMIT 60";
        
       
        mysqli_query($db, $query) or die('FEILMELDING: Feil i inntasting');

        $result = mysqli_query($db, $query);

        while ($row = mysqli_fetch_array($result)) {
         $arrTime[] = $row['TIMESTAMP'];
         $arrLabels[] = $row['CELSIUS'];
        }
        $arrCollection = array(array('label' => "°C" ,'data' => array_reverse($arrLabels)));
        $arrReturn = array('labels' => array_reverse($arrTime), 'datasets' => $arrCollection);
        print (json_encode($arrReturn, JSON_NUMERIC_CHECK));
        mysqli_close($db);

?>