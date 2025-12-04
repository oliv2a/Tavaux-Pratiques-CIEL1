<?php
$servername = "localhost";
$username = "root";
$password = "raspberry";
$BDD="WAI";

if($bdd = mysqli_connect($servername, $username, $password, $BDD))
{
	 echo 'Exemle d extraction des valeurs d une table';  // Si la connexion a réussi, rien ne se passe.
}
else // Mais si elle rate…
{
	echo 'Erreur'; // On affiche un message d'erreur.
}

$resultat = mysqli_query($bdd, 'SELECT * FROM mesures');
$mesures = mysqli_fetch_assoc($resultat);

// exemple d affichage de valeur
echo "<br>";
echo $mesures['id'];
echo "<br>";
echo $mesures['heure']; 
echo "<br>";
echo $mesures['temperature'];
?>