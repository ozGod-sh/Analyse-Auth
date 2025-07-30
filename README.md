# 🔐 Analyse-Auth - Analyseur de Tokens JWT

**Créé par ozGod-sh**

## Description

Analyse-Auth est un outil de cybersécurité spécialisé dans l'analyse et l'audit des tokens JWT (JSON Web Tokens). Il permet de décoder, vérifier et tester la sécurité des implémentations JWT en détectant les vulnérabilités courantes.

## Fonctionnalités

### 🔍 Analyse Complète des JWT
- **Décodage automatique** : Extrait et affiche le header et payload sans vérification de signature
- **Analyse de vulnérabilités** : Détecte l'attaque "alg:none" 
- **Vérification de signature** : Teste la validité avec un secret fourni
- **Brute-force de secrets** : Utilise une wordlist pour découvrir les secrets faibles

### 🛡️ Détection de Vulnérabilités
- **Algorithme "none"** : Identifie les tokens acceptés sans signature
- **Secrets faibles** : Teste contre une liste de mots de passe courants
- **Format JSON lisible** : Affichage structuré des données décodées

## Installation

### Prérequis
- Python 3.6+
- pip (gestionnaire de paquets Python)

### Installation des dépendances
```bash
cd Analyse-Auth
pip install -r requirements.txt
```

### Dépendances
- `PyJWT` : Bibliothèque pour manipuler les tokens JWT
- `cryptography` : Support cryptographique pour les algorithmes de signature

## Utilisation

### Syntaxe de base
```bash
python analyse_auth.py <TOKEN_JWT> [OPTIONS]
```

### Options disponibles
- `-s, --secret SECRET` : Vérifie la signature avec un secret spécifique
- `-w, --wordlist FICHIER` : Brute-force le secret avec une wordlist
- `-h, --help` : Affiche l'aide

### Exemples d'utilisation

#### 1. Analyse basique d'un token
```bash
python analyse_auth.py eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

#### 2. Vérification avec un secret connu
```bash
python analyse_auth.py <TOKEN> --secret "mon_secret_jwt"
```

#### 3. Brute-force du secret
```bash
python analyse_auth.py <TOKEN> --wordlist wordlist.txt
```

## Structure des fichiers

```
Analyse-Auth/
├── analyse_auth.py      # Script principal
├── requirements.txt     # Dépendances Python
├── wordlist.txt        # Liste de secrets courants
└── README.md           # Cette documentation
```

## Logique de fonctionnement

### 1. Décodage JWT
L'outil utilise `jwt.get_unverified_header()` et `jwt.decode()` avec `verify_signature=False` pour extraire les informations sans validation.

### 2. Détection "alg:none"
Vérifie si l'algorithme dans le header est défini sur "none", ce qui permet d'accepter des tokens sans signature.

### 3. Vérification de signature
Utilise l'algorithme spécifié dans le header pour valider la signature avec le secret fourni.

### 4. Brute-force
Teste séquentiellement chaque secret de la wordlist jusqu'à trouver une correspondance valide.

## Wordlist incluse

Le fichier `wordlist.txt` contient des secrets couramment utilisés :
- secret
- 123456
- password
- admin
- root
- changeme
- secretkey
- jwt
- json
- token
- auth
- key

## Cas d'usage

### Pour les pentesters
- Audit de sécurité des applications web utilisant JWT
- Test de robustesse des secrets de signature
- Identification de configurations dangereuses

### Pour les développeurs
- Validation de l'implémentation JWT
- Test de la force des secrets utilisés
- Vérification des bonnes pratiques de sécurité

## Limitations

- Ne supporte que les algorithmes symétriques pour le brute-force
- La wordlist fournie est basique (peut être étendue)
- Pas de support pour les clés RSA/ECDSA dans le brute-force

## Sécurité et éthique

⚠️ **Utilisation responsable uniquement**
- Utilisez cet outil uniquement sur vos propres applications
- Obtenez une autorisation écrite avant tout test de pénétration
- Respectez les lois locales sur la cybersécurité

## Licence

MIT License - Voir le fichier LICENSE pour plus de détails.

---

**Analyse-Auth v1.0.0** | Créé par ozGod-sh