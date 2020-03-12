# Introduction

Afin de répondre à certaines demandes en interne j'avais développé ce plugin QGis pour traiter les XML des DT/DICT.

Le développement a été abandonnée durant plusieurs années, mais a repris grâce à l'intérêt porté par de nombreuses sollicitations et le travail fournit par la FDEA.

C'est à ce jour la seule solution opensource existante sur le marché.

N'hésitez pas à nous contacter par [mail](mailto:infos@oslandia.com?subject=[DICT]%20Demande%20pour%20le%20plugin) si vous souhaitez faire évoluer ce plugin.

Vous trouverez plus d'informations sur notre [page dédiée](https://oslandia.com/en/offre-qgis/plugin-de-reponse-aux-dict).

# Utilisation

L'outil est composé de deux bouttons : un pour traiter un XML (à gauche) <img src="icon.png"  width="32" height="32"> et un pour configurer le plugin (à droite) <img src="config.png"  width="32" height="32">.

## Configuration
La configuration permet à l’utilisateur de ne pas avoir à répéter la saisie des informations et indiquer où et comment doivent sortir les PDF.

![configuration1](images/configuration.png)

![configuration2](images/configuration2.png)

## Traitement de la DT/DICT

Le XML reçu est à ouvrir via la boîte de dialogue suivante :

![chargement du xml](images/chargement_xml.png)

Vous serez ensuite guidé par un assistant qui reprend la logique du formulaire PDF. Des contrôles sont en place pour éviter les erreurs de saisie.

![assistant, onglet "Informations et coordonnées"](images/wizard1.png)
![assistant, onglet "Réponse à la DICT"](images/wizard2.png)
![assistant, onglet "Sécurité et signature"](images/wizard3.png)

Le plugin doit s'utiliser sur un projet ouvert comprenant vos réseaux et les composeurs d'impression qui seront utilisés pour la sortie des plans.
Après avoir rempli le formulaire, vous devez sélectionner le composeur pour l'impression PDF. Vous pouvez noter une emprise de chantier indiquant l'emprise de la demande.

![Sélection du composeur et emprise du chantier](images/selection_composeur.png)

Une fois le traitement effectué vous pouvez récupérer le formulaire pdf et les plans. Ils seront fusionnés si vous avez configuré cette option.

