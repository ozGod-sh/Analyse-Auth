# -*- coding: utf-8 -*-
# Auteur: ozGod

import argparse
import jwt
import json
import sys

def display_banner():
    """Affiche une bannière stylisée pour l'outil."""
    VERSION = "1.0.0"
    AUTHOR = "ozGod"
    banner = f"""
╔══════════════════════════════════════════════════════════╗
║                                                              ║
║  🔐 Analyse-Auth (JWT) v{VERSION}                            ║
║                                                              ║
║  Analyseur de tokens JWT et de failles d'authentification.  ║
║  Créé par {AUTHOR}                                           ║
║                                                              ║
╚══════════════════════════════════════════════════════════╝
"""
    print(banner)

def decode_jwt(token):
    """Décode et affiche le contenu d'un token JWT sans vérifier la signature."""
    try:
        header = jwt.get_unverified_header(token)
        payload = jwt.decode(token, options={"verify_signature": False})
        print("[*] En-tête (Header):")
        print(json.dumps(header, indent=2))
        print("\n[*] Charge utile (Payload):")
        print(json.dumps(payload, indent=2))
        return header, payload
    except jwt.DecodeError as e:
        print(f"[!] Erreur de décodage JWT : {e}", file=sys.stderr)
        return None, None

def check_alg_none(token):
    """Vérifie si le token est vulnérable à l'attaque alg:none."""
    header, _ = decode_jwt(token)
    if header and header.get('alg').lower() == 'none':
        print("\n[!] VULNÉRABILITÉ TROUVÉE: L'algorithme est 'none'. Le token peut être accepté sans signature.")
    else:
        print("\n[*] L'algorithme n'est pas 'none'.")

def verify_signature(token, secret):
    """Vérifie la signature du token avec un secret donné."""
    try:
        header = jwt.get_unverified_header(token)
        alg = header.get('alg')
        jwt.decode(token, secret, algorithms=[alg])
        print(f"\n[+] La signature est VALIDE avec le secret : '{secret}'")
        return True
    except (jwt.InvalidSignatureError, jwt.DecodeError):
        print(f"\n[-] La signature est INVALIDE avec le secret : '{secret}'")
        return False

def brute_force_secret(token, wordlist):
    """Tente de trouver le secret en utilisant une wordlist."""
    print("\n[*] Démarrage du brute-force du secret...")
    try:
        with open(wordlist, 'r', encoding='utf-8') as f:
            secrets = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[!] Erreur: Le fichier wordlist '{wordlist}' est introuvable.", file=sys.stderr)
        return

    header = jwt.get_unverified_header(token)
    alg = header.get('alg')

    for secret in secrets:
        try:
            jwt.decode(token, secret, algorithms=[alg])
            print(f"\n[+] SUCCÈS ! Le secret est : '{secret}'")
            return
        except (jwt.InvalidSignatureError, jwt.DecodeError):
            continue
    
    print("\n[-] Echec. Aucun secret valide n'a été trouvé dans la wordlist.")

def main():
    display_banner()
    parser = argparse.ArgumentParser(
        description="Analyse les tokens JWT, vérifie les signatures et cherche des vulnérabilités.",
        epilog=f"Créé par ozGod."
    )
    parser.add_argument("token", help="Le token JWT à analyser.")
    parser.add_argument("-s", "--secret", help="Le secret pour vérifier la signature.")
    parser.add_argument("-w", "--wordlist", help="Le chemin vers la wordlist pour brute-forcer le secret.")

    args = parser.parse_args()

    print(f"[*] Analyse du token...")
    header, _ = decode_jwt(args.token)

    if not header:
        sys.exit(1)

    check_alg_none(args.token)

    if args.secret:
        verify_signature(args.token, args.secret)
    elif args.wordlist:
        brute_force_secret(args.token, args.wordlist)
    else:
        print("\n[*] Pour vérifier la signature, fournissez un secret (--secret) ou une wordlist (--wordlist).")

if __name__ == "__main__":
    main()
