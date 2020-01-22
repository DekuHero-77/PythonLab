#!/usr/bin/python
# Variables can be changed here:
banned =  "CN=mail_zimbra,OU=Services,OU=Groups,OU=ELLIPSE,DC=ORION,DC=lan"
# an OU for banned users
scope   = 'OU=Users,OU=Paris,OU=ELLIPSE,DC=ORION,DC=lan'
#the search scope
domain = "" # "example.com"
ldapserver="par-ad01.orion.lan"
#ldap server
port="389"
#ldap port (389 default)
emaildomain="ellipsanime.net"
#the email domain
ldapbinddomain="ellipse"
#the domain of the ldap bind account
ldapbind="CN=mail zimbra,OU=SysAccount,OU=Paris,OU=ELLIPSE,DC=ORION,DC=lan"
#the account name of the account to bind to ldap
ldappassword="wVbUs2]JqaaT"
#the ldap password
pathtozmprov="/opt/zimbra/bin/zmprov"
mailinglistname="studio-paris@ellipsanime.net"
#--------------------------------------------------------------------------------------------------
import ldap, string, os, time, sys 
#output the list of all accounts from zmprov gaa (get all accounts)
f = os.popen(pathtozmprov +' -l gaa')
zmprovgaa= []
zmprovgaa = f.readlines() 
l=ldap.initialize("ldap://"+ldapserver+":"+port)
l.simple_bind_s(ldapbind,ldappassword) #bind to the ldap  server using name/password
try:
    res = l.search_s(scope, ldap.SCOPE_SUBTREE, "(&(ObjectCategory=user) )",['sAMAccountName','mail'])
    usermail = []
    for (dn, vals) in res:
      try:
        mail = vals['mail'][0].lower()
      except:
        mail = vals['sAMAccountName'][0].lower() + "@" + emaildomain
      usermail.append(mail)

except ldap.LDAPError, error_message:
  print error_message
l.unbind_s()

f = os.popen(pathtozmprov + ' gdlm ' + mailinglistname + '| grep @ | grep -v "#"')
zmprovmember= []
zmprovmember = f.read().splitlines()

missingintozimbra = list(set(usermail) - set(zmprovmember))
removetozimbra = list(set(zmprovmember) - set(usermail))

f = os.popen(pathtozmprov +' -l gaa')
zmprovgaa= []
zmprovgaa = f.read().splitlines()

for mail in missingintozimbra:
  if mail in zmprovgaa:
    print mail," add to list"
    os.system(pathtozmprov + ' adlm ' + mailinglistname + ' ' + mail)     

for mail in removetozimbra:
  if mail in removetozimbra:
    print mail," remove to list "
    os.system(pathtozmprov + ' rdlm ' + mailinglistname + ' ' + mail)     
     
  
