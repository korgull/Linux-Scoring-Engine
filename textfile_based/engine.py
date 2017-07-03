#!/usr/bin/python2
# Author is Moses Arocha


import os
import pwd
import re
import socket
import subprocess
import sys

#!/usr/bin/python2

import subprocess as n
import pygame
import time


n.call(['notify-send', 'foo', 'bar'])
pygame.init()
pygame.mixer.music.load("/home/moses/Music/smb_stage_clear.mp3")
pygame.mixer.music.play()
time.sleep(10)



score = 0
points = []


def program_check(program):
   pro = subprocess.Popen("dpkg -l | grep " +program, shell=True, stdout=subprocess.PIPE)
   display = pro.stdout.read()
   pro.stdout.close()
   pro.wait()
   if display:
       return True
   else:
       return False


def waf_check():
   global score
   if os.path.isfile("/etc/modsecurity/modsecurity.conf-recommended"):
       pro = subprocess.Popen("cat /etc/modsecurity/modsecurity.conf-recommended", shell=True, stdout=subprocess.PIPE)
       display = pro.stdout.read()
       pro.stdout.close()
       pro.wait()
       if "SecRequestBodyAccess Off" in display:
           score = score+1
           f = open('index.html', 'a')
           f.write('Added WAF Protection to Apache Server')
           f.close()


def update_programs(topic,respository):
   global score
   pro = subprocess.Popen("cat /etc/apt/sources.list", shell=True, stdout=subprocess.PIPE)
   display = pro.stdout.read()
   pro.stdout.close()
   pro.wait()
   if respository in display:
      score = score+1
      f = open('index.html', 'a')
      f.write('Respository Added To Debian Package Lists')
      f.close()


def user_passwd(user,hash):
   global score
   pro = subprocess.Popen("cat /etc/shadow | grep "+user, shell=True, stdout=subprocess.PIPE)
   display = pro.stdout.read()
   pro.stdout.close()
   pro.wait()
   if hash not in display:
      score = score+1
      f = open('index.html', 'a')
      f.write('Changed '+user+' Password')
      f.close()


def firewall_check():
   global score
   pro = subprocess.Popen("crontab -e", shell=True, stdout=subprocess.PIPE)
   display = pro.stdout.read()
   pro.stdout.close()
   pro.wait()
   if 'Firewall/setup.py' not in display:
      score = score+1
      points.append('Enabled The Firewall')
      f = open('index.html', 'a')
      f.write('Enabled The Firewall')
      f.close()


def group_check(user):
   global score
   pro = subprocess.Popen("cat /etc/group | grep sudo", shell=True, stdout=subprocess.PIPE)
   display = pro.stdout.read()
   pro.wait()
   if user in display:
      score = score+1
      f = open('index.html', 'a')
      f.write('Added '+user+' To The Sudo Group')
      f.close()


def password_complexity():
   global score
   pro = subprocess.Popen("cat /etc/pam.d/common-password", shell=True, stdout=subprocess.PIPE)
   display=pro.stdout.read()
   pro.wait()
   f = open('index.html', 'a')
   if "remember=5" in display:
     score = score+1
     f.write('Added Password History')
   if "minlen=8" in display:
     score = score+1
     f.write('Enforced Password Length')
   if "ucredit" and "lcredit" and "dcredit" and "ocredit" in display:
     score = score+1
     f.write('Added Password Complexity')
     f.close()


def password_history():
   global score
   pro = subprocess.Popen("cat /etc/login.defs", shell=True, stdout=subprocess.PIPE)
   display = pro.stdout.read()
   pro.wait()
   if "PASS_MAX_DAYS " and "PASS_MIN_DAYS " and "PASS_WARN_AGE " in display:
     score = score+1
     f = open('index.html', 'a')
     f.write('Added Password History Standards')
     f.close()


def account_policy():
   global score
   pro = subprocess.Popen("cat /etc/pam.d/common-auth", shell=True, stdout=subprocess.PIPE)
   display = pro.stdout.read()
   pro.wait()
   if "deny=" and "unlock_time=" in display:
      score = score+1
      f = open('index.html', 'a')
      f.write('Set Account Policy Standards')
      f.close()


def guest_account(file_path):
   global score
   if os.path.isfile(file_path):
     pro = subprocess.Popen("cat "+file_path, shell=True, stdout=subprocess.PIPE)
     display = pro.stdout.read()
     pro.wait()
     if "allow-guest=false" in display:
        score = score+1
        f = open('index.html', 'a')
        f.write('Disabled Guest Account')
        f.close()


def apache_security(file):
   global score
   if os.path.isfile(file):
      pro = subprocess.Popen("cat " +file, shell=True, stdout=subprocess.PIPE)
      display = pro.stdout.read()
      pro.wait()
      if "ServerSignature" and "ServerTokens" in display:
          score = score+1
          f = open('index.html', 'a')
          f.write('Secured Apache Web Server')
          f.close()


def ssh_security():
   global score
   pro = subprocess.Popen("cat /etc/ssh/sshd_config | grep PermitRootLogin", shell=True, stdout=subprocess.PIPE)
   display = pro.stdout.read()
   pro.wait()
   f = open('index.html', 'a')
   if "no" in display:
      score = score+1
      f.write('Disabled Root Login for SSH')
   subpro = subprocess.Popen("cat /etc/ssh/sshd_config", shell=True, stdout=subprocess.PIPE)
   subdisplay = subpro.stdout.read()
   subpro.wait()
   if "AllowUsers" in subdisplay:
      score = score+1
      f.write('Secured SSH User Login')
      f.close()


def samba_security():
   global score
   pro = subprocess.Popen("cat /etc/samba/smb.conf", shell=True, stdout=subprocess.PIPE)
   display = pro.stdout.read()
   pro.wait()
   f = open('index.html', 'a')
   if "guest ok = no" in display:
      score = score+1
      f.write('Secured Samba Server')
      f.close()


def php_security():
   global score
   pro = subprocess.Popen("cat /etc/php/7.0/apache2/php.ini | grep expose_php", shell=True, stdout=subprocess.PIPE)
   display = pro.stdout.read()
   pro.wait()
   if "Off" in display:
     score = score+1
     f = open('index.html', 'a')
     f.write('secured PHP Version')
     f.close()


def malware_check(file_path):
   global score
   if not os.path.isfile(file_path):
      score = score+1
      f = open('index.html', 'a')
      f.write('Removed Harmful File')
      f.close()


def user_check(user):
   global score
   jenny = 0
   for line in open('/etc/passwd'):
       if user in line:
           jenny = 1
   if jenny == 0:
       score = score+1
       f = open('index.html','a')
       f.write('Removed The User '+user)
       f.close()


def main():
   global score
   global points
   if not program_check('nmap'):
      score = score+1
      f = open('index.html','a')
      f.write('Removed The Tool Nmap')
      f.close()
   if not program_check('medusa'):
      score = score+1
      d = open('index.html','a')
      d.write('Removed The Tool Medusa')
      d.close()
   user_check('jennylewis')
   user_check('moses')
   group_check('juan')
   user_passwd('cyber', '$6$FicC')
   user_passwd('jimmy', '$6$QMoj')
   user_passwd('ben',   '$6$SkT') 
   malware_check('/home/cyber/.virus.py')
   malware_check('/root/Firewall/setup.py')
   firewall_check()
   update_programs('General','http://us.archive.ubuntu.com/ubuntu')
   update_programs('Security','http://security.ubuntu.com/ubuntu')
   password_complexity()
   password_history()
   account_policy()
   guest_account('/etc/lightdm/lightdm.conf')
   apache_security('/etc/apache2/conf-available/myconf.conf')
   ssh_security()
   php_security()
   waf_check()
   samba_security()
   for point in points:
       print point
   print str(score),"/25 Total Points"


if __name__ == '__main__':
   main()

