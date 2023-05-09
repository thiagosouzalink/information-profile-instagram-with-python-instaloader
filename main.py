"""
Projeto que exibe informações de perfil, lista de seguidores e lista de
contas que está seguindo de um usuário da rede social Instagram.

Project that displays profile information, list of followers and list of
accounts that are following of a social network user Instagram.
"""
from getpass import getpass

import instaloader


from profile_information import (login,
                                 process_information)


if __name__ == "__main__":
    instagram = instaloader.Instaloader()

    username = input("Informe seu username: ").strip()
    password = getpass("Informe sua senha: ")

    profile = login(instagram, username, password)

    if not profile:
        print("\nVerifique as informações da conta e tente novamente.\n")

    else:
        print(f"\nProcessando informações do usuário {username}...")
        process_information(profile, get_not_followers_back=True)
