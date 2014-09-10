#!/usr/bin/env python
import threading
import time
import paramiko
import os,sys
from optparse import OptionParser
from sshconfig.cfg.config import host_msg,ip_msg
def opts():
    parser = OptionParser(usage="usage %prog options")
    parser.add_option("-i","--item",
                        dest="item",
                        default="",
                        action="store",
                        )
    parser.add_option("-p","--host",
                        dest="host",
                        default="",
                        action="store",
                        )
    parser.add_option("-f","--file",
                        dest="file",
                        default="",
                        action="store",
                        )
    parser.add_option("-s","--sfile",
                        dest="sfile",
                        default="",
                        action="store",
                        )
    parser.add_option("-d","--dfile",
                        dest="dfile",
                        default="",
                        action="store",
                        )
    parser.add_option("-c","--cmd",
                        dest="cmd",
                        default="",
                        action="store",
                        )
    parser.add_option("-x","--xia",
                        dest="xsfile",
                        default="",
                        action="store",
                        )
    parser.add_option("-z","--zai",
                        dest="zdfile",
                        default="",
                        action="store",
                        )
    return parser.parse_args()
class Get_date(object):
    def ssh_cmd(self,number,user,ip,port,cmd):
        for i in xrange(number):
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip,port,user,"")
            stdin1, stdout1, stderr1 = ssh.exec_command("hostname")
            stdin2, stdout2, stderr2 = ssh.exec_command(cmd)
            out1 = stdout1.read()
            #in2 = stdin2.read()
            out2 = stdout2.read()
            err2 = stderr2.read()
            if out2 or err2:
                #print "\033[32;1m%s-%s:\033[0m\n%s %s" %(out1.strip(),ip,out2.strip(),err2.strip())
                print "%s-%s:\n%s %s" %(out1.strip(),ip,out2.strip(),err2.strip())
                #print "\033[33;1m-\033[0m"*120
                print "-"*120
                ssh.close()
            else:
                #print "\033[32;1m%s-%s:\033[0m\n%s %s" %(out1.strip(),ip,"operation successfully [ok]",err2.strip())
                print "%s-%s:\n%s %s" %(out1.strip(),ip,"operation successfully [ok]",err2.strip())
                #print "\033[33;1m-\033[0m"*120
                print "-"*120
                ssh.close()
    def ssh_file(self,number,user,ip,port,path_ssh_key,sfile,dfile):
        key = paramiko.DSSKey.from_private_key_file(path_ssh_key)
        for i in xrange(number):
            ssh = paramiko.Transport((ip,port))
            ssh_f=ssh.connect(username = user, pkey = key)
            sftp = paramiko.SFTPClient.from_transport(ssh)
            path=os.path.split(dfile)[0]
            try:
                ssh_result=sftp.put(sfile,dfile)
            except Exception as e:
                for i in xrange(1,len(path.split('/'))+1):
                    try:
                        a=path.split('/')[0:i]
                        new_path='/'.join(a)
                        sftp.mkdir(new_path)
                    except Exception as e:
                        continue
                ssh_result=sftp.put(sfile,dfile)
            #print "\033[31;1m%s\033[0m"%(ip)
            print "%s"%(ip)
            #print "\033[32;1m%s:---------->%s\033[0m\n%s"%(sfile,dfile,ssh_result)
            print "%s:---------->%s\n%s"%(sfile,dfile,ssh_result)
            #print "\033[33;1m-\033[0m"*120
            print "-"*120
            ssh.close()
    def ssh_down(self,number,user,ip,port,path_ssh_key,sfile,dfile):
        key = paramiko.DSSKey.from_private_key_file(path_ssh_key)
        for i in xrange(number):
            ip_ID="-"+ip.split(".")[-1]
            ssh = paramiko.Transport((ip,port))
            ssh_f=ssh.connect(username = user, pkey = key)
            sftp = paramiko.SFTPClient.from_transport(ssh)
            path=os.path.split(dfile)[0]
            try:
                ssh_result=sftp.get(sfile,dfile+ip_ID)
            except Exception as e:
                for i in xrange(1,len(path.split('/'))+1):
                    try:
                        a=path.split('/')[0:i]
                        new_path='/'.join(a)
                        os.mkdir(new_path)
                    except Exception as e:
                        continue
                ssh_result=sftp.get(sfile,dfile+ip_ID)
            #print "\033[31;1m%s\033[0m"%(ip)
            print "%s"%(ip)
            #print "\033[32;1m%s:---------->%s\033[0m\n%s"%(sfile,dfile,ssh_result)
            print "%s:---------->%s\n%s"%(sfile,dfile,ssh_result)
            #print "\033[33;1m-\033[0m"*120
            print "-"*120
    def cmd(self,user,ip,port,cmd):
        for i in xrange(len(ip)):
            a=threading.Thread(target=self.ssh_cmd,args=(1,user,ip[i],port,cmd))
            a.start()
    def dfile(self,user,ip,port,path_ssh_key,sfile,dfile):
        for i in xrange(len(ip)):
            a=threading.Thread(target=self.ssh_down,args=(1,user,ip[i],port,path_ssh_key,sfile,dfile))
            a.start()
    def ufile(self,user,ip,port,path_ssh_key,sfile,dfile):
        for i in xrange(len(ip)):
            a=threading.Thread(target=self.ssh_file,args=(1,user,ip[i],port,path_ssh_key,sfile,dfile))
            a.start()
def main():
    user=host_msg["user"]
    port=host_msg["port"]
    path_ssh_key=host_msg["ssh_key"]
    get_host_date=Get_date()
    opt,args=opts()
    ssh_xs=opt.xsfile
    ssh_zd=opt.zdfile
    ssh_item=opt.item
    ssh_file=opt.file
    ssh_sfile=opt.sfile
    ssh_dfile=opt.dfile
    ssh_cmd=opt.cmd
    ssh_ip=opt.host
    if ssh_cmd:
        if ssh_ip:
            if args:
                args.append(ssh_ip)
                get_host_date.cmd(user,args,port,ssh_cmd)
            else:
                get_host_date.cmd(user,[ssh_ip],port,ssh_cmd)
        if ssh_item and ssh_item in ip_msg.keys():
            get_host_date.cmd(user,ip_msg[ssh_item],port,ssh_cmd)
    if ssh_file:
        if ssh_ip:
            if args:
                args.append(ssh_ip)
                get_host_date.ufile(user,args,port,path_ssh_key,ssh_file,ssh_file)
            else:
                get_host_date.ufile(user,[ssh_ip],port,path_ssh_key,ssh_file,ssh_file)
        if ssh_item and ssh_item in ip_msg.keys():
            get_host_date.ufile(user,ip_msg[ssh_item],port,path_ssh_key,ssh_file,ssh_file)
    if ssh_sfile and ssh_dfile:
        if ssh_ip:
            if args:
                args.append(ssh_ip)
                get_host_date.ufile(user,args,port,path_ssh_key,ssh_sfile,ssh_dfile)
            else:
                get_host_date.ufile(user,[ssh_ip],port,path_ssh_key,ssh_sfile,ssh_dfile)
        if ssh_item and ssh_item in ip_msg.keys():
            get_host_date.ufile(user,ip_msg[ssh_item],port,path_ssh_key,ssh_sfile,ssh_dfile)
    if ssh_xs and ssh_zd:
        if ssh_ip:
            if args:
                args.append(ssh_ip)
                get_host_date.dfile(user,args,port,path_ssh_key,ssh_xs,ssh_zd)
            else:
                get_host_date.dfile(user,[ssh_ip],port,path_ssh_key,ssh_xs,ssh_zd)
        if ssh_item and ssh_item in ip_msg.keys():
            get_host_date.dfile(user,ip_msg[ssh_item],port,path_ssh_key,ssh_xs,ssh_zd)
if __name__=="__main__":
    main()    
