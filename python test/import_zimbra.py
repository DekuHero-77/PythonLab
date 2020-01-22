#!/usr/bin/python
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; GPLv3
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# To obtain a copy of the GNU General Public License, write to the Free  Software Foundation,
# Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA
#
#--------------------------------------------------------------------------------------------------
# Notes:
# This script automatically creates zimbra accounts from active directory, the  actrive directory account must have
# the employeeType=STUDENT attributed set. If accounts are in the 'banned' active directory group then the
# account will automatically be locked when the script is run, and unlocked if they are no longer in the AD
# banned group
#--------------------------------------------------------------------------------------------------
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
#--------------------------------------------------------------------------------------------------
import ldap, string, os, time, sys 
#output the list of all accounts from zmprov gaa (get all accounts)
f = os.popen(pathtozmprov +' -l gaa')
zmprovgaa= []
zmprovgaa = f.readlines() 
l=ldap.initialize("ldap://"+ldapserver+":"+port)
l.simple_bind_s(ldapbind,ldappassword) #bind to the ldap  server using name/password
try:
    res = l.search_s(banned,
    ldap.SCOPE_SUBTREE)
    member = []
    for (dn, vals) in res:
      try:
        member = vals['member']
      except:
        print "no users"

    for userdn in member:
	resUser = l.search_s(userdn,
        ldap.SCOPE_SUBTREE, "(&(ObjectCategory=user) )",  ['sAMAccountName','givenName','sn','memberOf', 'userAccountControl', 'name'])
	#userAccountControl  512 = normal , 514 = disabled account
        for (dn, vals) in resUser:
          accountname = vals['sAMAccountName'][0].lower()
          try:
            sirname = vals['sn'][0].lower()
          except:
            sirname = vals['sAMAccountName'][0].lower()
          try:
            givenname = vals['givenName'][0]
          except:
            givenname = vals['sAMAccountName'][0].lower()
          try:
            groups = vals['memberOf']
          except:
            groups = 'none'
          try:
            status = vals['userAccountControl'][0]
          except:
            status = '514'
          initial = givenname[:1].upper()
          sirname = sirname.replace(' ', '')
          sirname = sirname.replace('\\', '')
          sirname = sirname.replace('-', '')
          sirname = sirname.capitalize()
          name = initial + "." + sirname
          accountname = accountname + "@" + emaildomain
          password = "  \'\' "
          sys.stdout.flush()
	  
	  validuserAccountControl = ['512', '66048']
          # if the account doesn't exist in the output of zmprov gaa create the  account
          if accountname +"\n" not in zmprovgaa:
            if status in validuserAccountControl:
              print  accountname," exists in active directory but not in zimbra, the   account is being created\n"
              time.sleep(1)
              os.system(pathtozmprov +' ca %s %s displayName "%s" givenName "%s" sn "%s"' %  (accountname,password,vals['name'][0], vals['givenName'][0],  vals['sn'][0]))
          else:
            zmprovga = os.popen(pathtozmprov + ' ga %s' % (accountname))
            ga= []
            ga = zmprovga.readlines()
            locked = "zimbraAccountStatus: locked\n"
            if status not in validuserAccountControl:
              if locked not in ga: #if account not locked then lock it
                print accountname, " The email  account has been locked "
                #os.system(pathtozmprov + ' ma %s zimbraAccountStatus locked' % (accountname))
                time.sleep(1)
            else:
              if locked in ga: #if account not locked then lock it
                print accountname, " The email  account has been unlocked "
                #os.system(pathtozmprov + ' ma %s zimbraAccountStatus active' % (accountname))
                time.sleep(1)



except ldap.LDAPError, error_message:
  print error_message
l.unbind_s()
