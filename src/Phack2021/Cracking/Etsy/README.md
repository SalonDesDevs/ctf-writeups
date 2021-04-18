# Etsy - 128 points

Il n'y a pas besoin de prêter attention à l'indice sur le boss, celui-ci est plus déroutant qu'autre chose.

On se voit fourni deux fichiers qui sont respectivement un /etc/passwd et le /etc/shadow associé d'un système, ainsi qu'une wordlist. Il nous reste à voir si l'on peut cracker un ou des mots de passe parmi ceux-ci. On utilise [john](https://github.com/openwall/john).

`john unshadow passwd shadow > passwords.txt`
    
`john --wordlist=wordlist passwords.txt`

Après un temps conséquent (17min26 sur mon ordinateur) la session se conclut et précise qu'un mot de passe a été trouvé, l'on peut voir celui-ci avec `john --show passwords.txt`, et le flag est `PHACK{mot de passe}`.