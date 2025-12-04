 <?php
$servername = "localhost";
$username = "root";
$password = "raspberry";
$BDD="bts_sn1";

if($bdd = mysqli_connect($servername, $username, $password, $BDD))
{
	 echo 'Connexion OK';  // Si la connexion a réussi, rien ne se passe.
}
else // Mais si elle rate…
{
	echo 'Erreur'; // On affiche un message d'erreur.
}

$resultat = mysqli_query($bdd, 'SELECT * FROM mesures ');
$mesures = mysqli_fetch_assoc($resultat);

list($date, $time) = explode(" ", $mesures['date']);
list($year, $month, $day) = explode("-", $date);
list($hour, $min, $sec) = explode(":", $time);
?>



<!doctype html>


<html lang="fr">
<head>

</head>

<body>

<?php echo $date = "$day/$month/$year"; ?>

<?php echo $mesures['temperature'];?>
<?php echo $mesures['humidite'];?> %

</body>
</html>
