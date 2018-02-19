# Pizik

Transformez votre RaspBerry Pi en instrument de musique libre !

Le projet est encore en phase de babillage.

Installez les librairies OSC pour permettre à Python d'envoyer des messages OSC à Sonic-Pi qui se chargera de produire du son.

Pour l'instant, le seul programme fonctionnel est le simple_piano, que l'on trouve dans modules.
Effectuez les branchement comme indiqué dans le script simple_piano.py (pour chacun des numéros de boutons, reliez la pin du RaspBerry Pi à une patte du bouton, l'autre patte à la terre).
Lancez SonicPi, ouvrez le fichier simple_piano.txt, mettez le en route avec alt - R.
Via le terminal ou un IDE comme Geany, lancez le script simple_piano.py.

Vous avez un petit clavier huit touches, paramétrable à l'aide de Sonic Pi.