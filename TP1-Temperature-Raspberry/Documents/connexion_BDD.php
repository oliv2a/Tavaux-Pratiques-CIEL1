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
?>
