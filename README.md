# <img src="assets/app_logo.png" alt="Logo" width="44" align="left"> SauveLeSherif Optimizer

✨ Optimiseur simple pour **SauveLeSherif** sur Steam.

## 📥 Téléchargement

➡️ **Télécharger la dernière version :** [SauveLeSherif Optimizer - Dernière release](https://github.com/keynaqua/SauveLeSheriff_Optimizer/releases/download/v1.0/SauveLeSherif_Optimizer.exe)

➡️ **Voir toutes les versions :** [Historique des releases](https://github.com/keynaqua/SauveLeSheriff_Optimizer/releases)

![Capture de l'application](assets/SLS_app_capture.png)

## 📝 Description

**SauveLeSherif Optimizer** permet de modifier rapidement les réglages graphiques du jeu sans ouvrir manuellement le fichier de configuration.

L'application propose :

- 🎚️ des réglages graphiques via une interface claire ;
- ⚡ un bouton **Optimiser** pour appliquer un preset recommandé ;
- ♻️ un bouton **Restaurer** pour remettre les qualités graphiques par défaut ;
- 🟦 un bouton pour ajouter l'option Steam **DirectX 11** (`-dx11`) ;
- 🧹 un bouton pour retirer l'option **DirectX 11** ;
- 🔒 une interface locale, sans compte, sans connexion et sans collecte de données.

Le fichier modifié est celui du jeu, dans le dossier utilisateur Windows :

```text
%LOCALAPPDATA%\SauveLeSherif\Saved\Config\Windows\GameUserSettings.ini
```

## 🛠️ Installation

1. Télécharge la dernière version ici : [SauveLeSherif Optimizer - Download](https://github.com/keynaqua/SauveLeSheriff_Optimizer/releases/download/v1.0/SauveLeSherif_Optimizer.exe).
2. Récupère le fichier :

```text
SauveLeSherif_Optimizer.exe
```

3. Place-le où tu veux, par exemple sur le Bureau ou dans un dossier dédié.
4. Lance l'application.

✅ Aucune installation système n'est nécessaire.  
✅ L'application ne demande pas les droits administrateur.  
🛡️ Si Windows Defender affiche un avertissement, suis la section **Windows Defender / SmartScreen** plus bas.  

## 🚀 Lancement

Double-clique sur :

```text
SauveLeSherif_Optimizer.exe
```

### 🛡️ Si Windows Defender / SmartScreen affiche un warning

Windows peut afficher un écran du type :

![Capture erreur Windows Defender](assets/Erreur_WD_1.png)

**Ce warning apparaît parce que l'application n'est pas signée avec un certificat reconnu par Microsoft. Windows ne peut donc pas vérifier l'éditeur, même si l'application est locale et ne demande pas les droits administrateur. Une auto-signature ne retirerait pas cet avertissement pour les autres utilisateurs.**  

### ✅ Comment passer le warning Windows

**Étape 1 - Clique sur "Informations complémentaires"**

![Étape 1 - Informations complémentaires](assets/Erreur_WD_1_2.png)

**Étape 2 - Vérifie le nom de l'application**

![Étape 2 - Vérification du nom](assets/Erreur_WD_2.png)

**Étape 3 - Clique sur "Exécuter quand même"**

![Étape 3 - Exécuter quand même](assets/Erreur_WD_2_2.png)

## 🎉 Bravo ! Le programme devrait maintenant se lancer.

### 🎮 Option DirectX 11

Pour ajouter ou retirer l'option Steam `-dx11`, ferme Steam avant d'utiliser les boutons DirectX dans l'application.

L'application modifie uniquement les options de lancement Steam du jeu. Si Steam est ouvert, l'application refuse l'action pour éviter que Steam réécrive le fichier derrière.

## ♻️ Reset des paramètres

Pour remettre les réglages graphiques par défaut :

1. Ouvre **SauveLeSherif Optimizer**.
2. Clique sur **Restaurer**.
3. Relance le jeu.

Le reset remet les qualités graphiques à leur valeur par défaut dans l'application.

Pour retirer DirectX 11 :

1. Ferme Steam.
2. Ouvre **SauveLeSherif Optimizer**.
3. Clique sur **Retirer DirectX11**.
4. Relance Steam.

## 🙌 Crédits

- Application : **SauveLeSherif Optimizer**
- Auteur : **Keyn 🫧 (@aquakeyn on Discord)**  
- Jeu : [Sauve Le Shérif](https://store.steampowered.com/app/4760110/)
- Page de téléchargement : [Releases page](https://github.com/keynaqua/SauveLeSheriff_Optimizer/releases)
- Distribution : [GitHub](https://github.com/keynaqua/SauveLeSheriff_Optimizer)

Ce projet est un outil communautaire non officiel.
