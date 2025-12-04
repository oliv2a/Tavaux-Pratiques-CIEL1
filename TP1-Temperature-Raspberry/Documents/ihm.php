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

$resultat = mysqli_query($bdd, 'SELECT * FROM mesures ORDER BY id DESC LIMIT 1');
$mesures = mysqli_fetch_assoc($resultat);

list($date, $time) = explode(" ", $mesures['date']);
list($year, $month, $day) = explode("-", $date);
list($hour, $min, $sec) = explode(":", $time);
?>



<!doctype html>

<link rel="stylesheet" href="style_ihm.css" />
<META HTTP-EQUIV="Refresh" CONTENT="10">

<html lang="fr">
<head>
	<meta charset="utf-8">
	<title>IHM - BTS SN1 2022</title>
</head>

<body>

<DIV id="A">
Projet de BTS SN1 2022 <br>
Lycée Laetitia Bonaparte AJACCIO
</DIV>

<DIV id="B">
Le <?php echo $date = "$day/$month/$year"; ?> à <?php echo $date = "$hour h $min"; ?>
</DIV>

<DIV id="C">
Temp. : <?php echo $mesures['temperature'];?>°C / Hum. : <?php echo $mesures['humidite'];?> %
</DIV>

<DIV id="D">
Vent : <?php echo $mesures['vent'];?>km/h / Direction 
</DIV>

<DIV id="E">
Qualité de l'air
</DIV>

</body>
</html>
