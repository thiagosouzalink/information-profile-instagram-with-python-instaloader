"""
Módulo que disponibiliza ações de obter informações de perfil, lista de
seguidores e lista de contas que está seguindo de um usuário da rede
social Instagram.

Module that provides actions to obtain profile information, list of
followers and list of accounts that are being followed by a user of
Instagram social network.
"""
import instaloader
from instaloader.exceptions import (BadCredentialsException,
                                    InvalidArgumentException,
                                    TwoFactorAuthRequiredException)


def login(instagram, username, password):
    """ Realiza o login de um usuário no Instagram.
        Logs a user into Instagram.

    Args:
        instagram (instaloader.Instaloader): Instância de Instaloader.
                                             Instaloader instance.
        username (str): Nome de usário da conta no Instagram.
                        Instagram account username.
        password (str): Senha da conta no Instagram.
                        Instagram account password.

    Returns:
        instaloader.Profile : Se houver exito na realização do login,
                              caso contrário retorna None.
                              If the login is successful, otherwise it
                              returns None.
    """
    try:
        instagram.login(username, password)
    except InvalidArgumentException:
        print(f"Usuário {username} não existe.")
        return None
    except BadCredentialsException:
        print("\nCredencial inválida.")
        return None
    # Caso haja autenticação de dois fatores do usuário.
    # If there is two-factor authentication of the user.
    except TwoFactorAuthRequiredException:
        code = int(input("Informe o código de autenticação de dois fatores: "))
        try:
            instagram.two_factor_login(code)
        except BadCredentialsException:
            print("\nCódigo de dois fatores inválido.")
            return None
        else:
            profile = instaloader.Profile.from_username(instagram.context,
                                                        username)
            return profile
    else:
        profile = instaloader.Profile.from_username(instagram.context,
                                                    username)
        return profile


def process_information(profile):
    """Processa informações relacionadas ao usuário.
       Processes user-related information.

    Args:
        profile (instaloader.Profile): Instância Profile que armazena
        informações do perfil do usuário.
                                       Profile instance that stores user
        profile information.
    """
    followers_list = [(f.username, f.full_name)
                      for f in profile.get_followers()]
    following_list = [(f.username, f.full_name)
                      for f in profile.get_followees()]

    print_information(profile,
                      followers_list=followers_list,
                      following_list=following_list)


def get_not_followers_back(profile):
    """Obtém lista de usuários que não seguem a conta em questão.
       Gets list of users who do not follow the account in question.

    Args:
        profile (instaloader.Profile): Instância Profile que armazena
        informações do perfil do usuário.
                                       Profile instance that stores user
        profile information.
    """
    followers_list = [(f.username, f.full_name)
                      for f in profile.get_followers()]
    following_list = [(f.username, f.full_name)
                      for f in profile.get_followees()]

    no_followers_back = list(
        set(following_list).difference(set(followers_list))
    )

    print_information(profile, no_followers_back=no_followers_back)


def print_information(profile, followers_list=[],
                      following_list=[], no_followers_back=[]):
    """Exibe as informções solicitadas do usuário.
       Displays the requested information from the user.

    Args:
        profile (instaloader.Profile): Instância Profile que armazena
            informações do perfil do usuário.
                                       Profile instance that stores user
            profile information.
        followers_list (list, optional): Lista de seguidores da conta de
            usuário em questão. Valor default [].
                                         List of followers for the user
            account in question. Defaults to [].
        following_list (list, optional): Lista de usuários que a conta
            de usuário em questão está seguindo. Valor default [].
                                         List of users the user account
            in question is following. Defaults to [].
        no_followers_back (list, optional): Lista de usuários que não
            seguem a conta em questão de volta. Valor default [].
                                            List of users who do not
            follow the account in question back. Defaults to [].
    """
    print("\n########## INFORMAÇÕES DO USUÁRIO ##########\n")
    print(f"Username: {profile.username}")
    print(f"Nome: {profile.full_name}")
    print(f'Seguidores: {profile.followers}')
    print(f'Seguindo: {profile.followees}')
    print("\n############################################")

    if followers_list and following_list:
        highest_username_followers = max(followers_list,
                                         key=lambda f: len(f[0]))
        highest_username_following = max(following_list,
                                         key=lambda f: len(f[0]))
        print("\n\n########### Lista de Seguidores ###########\n")
        for f in followers_list:
            print(
                f"Username: {f[0].ljust(len(highest_username_followers[0])+5)}"
                f"Nome: {f[1]}"
            )
        print("############################################")

        print("\n\n########### Lista de Seguindo ###########\n")
        for f in following_list:
            print(
                f"Username: {f[0].ljust(len(highest_username_followers[0])+5)}"
                f"Nome: {f[1]}"
            )
        print("\n############################################")

    if no_followers_back:
        highest_username_following = max(no_followers_back,
                                         key=lambda f: len(f[0]))
        print("\n\n########## Lista que não seguem você de volta ##########\n")
        for f in no_followers_back:
            print(
                f"Username: {f[0].ljust(len(highest_username_following[0])+5)}"
                f"Nome: {f[1]}"
            )
        print(f"\nTotal: {len(no_followers_back)}")
        print("\n############################################\n")
