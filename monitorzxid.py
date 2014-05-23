# -*- coding: utf-8 -*-
import getconf
from kazoo.client import KazooClient,KazooState
import socket,sys, os, time, atexit
from signal import SIGTERM
import threading
import LogControltest as log
import MySQLdb
logger = log.LogControl()

class storage:
    def __init__(self):
        pass
    def _mysql(self,times,ip,percentage):
        connection = MySQLdb.connect(host='20.1.46.37',user='root', passwd='***', db='zookeeper')
        cursor = connection.cursor()
        sql_update = """ insert into zxid (times,ip,percentage) values("%s","%s","%s");"""
        cursor.execute(sql_update %(times,ip,percentage))

    def _local(self):
        pass

sto = storage()

class dzk:
    def __init__(self,hosts):
        self.hosts = hosts
        self.BasePath = "/my/"
        #self.zk = KazooClient(hosts='10.1.1.1:2181',retry_max_delay=2000)
        self.zk = KazooClient(hosts=self.hosts,retry_max_delay=2000)
        try:
            self.zk.start()
            self.zk.add_listener(self.listener)
        except Exception,e:
            print "ERROR connect LOST ==============>"

    def listener(state):
        if state == KazooState.LOST:
            self.zk.start()
        elif state == KazooState.SUSPENDED:
            print "*******listener saw KazooState.LOST"
        else:
            print "*******listener saw KazooState.CONNECT"

    def getIpHost(self):
        self.myname  = socket.getfqdn(socket.gethostname())
        myip = socket.gethostbyname(self.myname)
        return  myip

    def getData(self):
        ip = self.getIpHost()
        if ip:
            NODE = self.BasePath + ip
            print "register:",NODE
        try:
            if not self.zk.exists(NODE): 
                self.zk.ensure_path(NODE)
            else:
                self.zk.set(NODE,"check zxid")
        except Exception,e:
            logger.error("%s ERROR set data" %(self.hosts)) 
            logger.error("%s" %(e)) 
        
        try:
            if self.zk.exists(NODE):
                date,stat = self.zk.get(NODE)
                #10 hex to 16 hex and cut right 8 character
                lastzxid = int(hex(stat.last_modified_transaction_id)[-8:],16)
                epoch = int(hex(stat.last_modified_transaction_id)[:-8],16)
                lasttime = self.datechange(stat.last_modified)
                #print "jjjjj",lastzxid,epoch,lasttime
                redict = {}
                relist=[]
                redict["lastzxid"] = lastzxid
                redict["epoch"] = epoch
                redict["lasttime"] = lasttime
                relist.append(redict)
                logger.info("%s, %s" % (self.hosts,relist))
                to_db = {}
                to_db["times"] = time.strftime( '%Y-%m-%d %X', time.localtime( time.time()))
                to_db["ip"] = self.hosts
                if relist[0]["lastzxid"] < 3006477106:
                    pc = float("%.2f" %(float(relist[0]["lastzxid"])/4581298449))*100
                    to_db["percentage"] = pc
                    sto._mysql(to_db["times"],to_db["ip"],to_db["percentage"])
                    logger.info("%s  OK,current is %s%s" %(self.hosts,pc,"%"))
                    print "%s  OK,current is %s%s" %(self.hosts,pc,"%")
                else:
                    pc = float("%.2f" %(float(relist[0]["lastzxid"])/4581298449))*100
                    logger.error("ERROR zxid bigger %s;%s%s" %(self.hosts,pc,"%"))
                    print "ERROR zxid bigger %s;%s%s" %(self.hosts,pc,"%")
                #[{'epoch': 3, 'lasttime': '1970-01-17 12:18:29', 'lastzxid': 219383}]
                return relist
        except Exception,e:
            logger.error("%s ERROR get data" %(self.hosts))
            logger.error("%s " %(e))
            print "%s ERROR get data" %(self.hosts)


    def datechange(self,mtime):
        #mtime: The time in milliseconds from epoch when this znode was last modified.
        self.mtime = mtime
        return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(self.mtime))

class Daemon:
    """
    A generic daemon class.
    Usage: subclass the Daemon class and override the _run() method
    """
    #def __init__(self, pidfile, stdin=_logfile, stdout=_logfile, stderr=_logfile):
    def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile
    
    def _daemonize(self):
        """
        do the UNIX double-fork magic, see Stevens' "Advanced 
        Programming in the UNIX Environment" for details (ISBN 0201563177)
        http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
        """
        
        try: 
            pid = os.fork() 
            if pid > 0:
                sys.exit(0) 
        except OSError, e: 
            sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)
    
        os.setsid() 
        os.chdir("/") 
        os.umask(0) 
    
        try: 
            pid = os.fork() 
            if pid > 0:
                sys.exit(0) 
        except OSError, e: 
            sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1) 
    
        sys.stdout.flush()
        sys.stderr.flush()
        si = file(self.stdin, 'r')
        so = file(self.stdout, 'a+')
        se = file(self.stderr, 'a+', 0)
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())
    
        atexit.register(self.delpid)
        pid = str(os.getpid())
        file(self.pidfile,'w+').write("%s\n" % pid)
        print "start...ok!"
        logger.info("start...ok!")
    
    def delpid(self):
        os.remove(self.pidfile)
    def start(self):
        """
        Start the daemon
        """
        # Check for a pidfile to see if the daemon already runs
        try:
            pf = file(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None
    
        if pid:
            message = "pidfile %s already exist. Daemon already running?\n"
            sys.stderr.write(message % self.pidfile)
            sys.exit(1)
        
        # Start the daemon
        print "start success!"
        logger.info("start success!")
        self._daemonize()
        self._run()
    def stop(self):
        """
        Stop the daemon
        """
        # Get the pid from the pidfile
        try:
            pf = file(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None
    
        if not pid:
            message = "pidfile %s does not exist. Daemon not running?\n"
            sys.stderr.write(message % self.pidfile)
            return # not an error in a restart
        # Try killing the daemon process    
        try:
            while 1:
                os.kill(pid, SIGTERM)
                time.sleep(0.1)
                print "stoped"
        except OSError, err:
            err = str(err)
            if err.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                print str(err)
                sys.exit(1)
    def restart(self):
        """
        Restart the daemon
        """
        self.stop()
        self.start()
    def _run(self):
        """
        You should override this method when you subclass Daemon. It will be called after the process has been
        daemonized by start() or restart().
        """

class Threadgetzxid(threading.Thread):
    """Threaded Url Grab"""
    def __init__(self, secs):
        threading.Thread.__init__(self)
        logger.info("线程初始化，参数secs: %s" % (secs, ))
        self.secs = secs

    def run(self):
        self.hosts = getconf.get_iteam(self.secs,'ip')
        czk = dzk(self.hosts)

        while True:
            czk.getData()
            time.sleep(120)

class Myself:
    def _thread(self):

        workers = []

        list_secs = getconf.get_secs()
        for i in list_secs:                                                                                 
            t = Threadgetzxid(i)                                                                  
            t.setDaemon(True)                                                                          
            t.start()                                                                                  

            workers.append(t)

        for worker in workers:
            worker.join()
                                                                                                       
Mys = Myself()
#open for debug
#Mys._thread()

class MyDaemon(Daemon):
    def _run(self):
        Mys._thread()

if __name__ == "__main__":
    daemon = MyDaemon('/var/daemon_zk.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
