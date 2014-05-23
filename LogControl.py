import logging
logfile="/home/admin/zookeeper/logs/zk.log"
error_logfile="/home/admin/zookeeper/logs/zk.log"
class LogControl:
    def debug(self,message):
        self.message = message
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(levelname)-8s %(message)s',
                            filename=logfile)
        logging.debug('bkeep %s', self.message)
 
    def info(self,message):
        self.message = message
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(levelname)-8s %(message)s',
                            filename=logfile)
        logging.info('bkeep %s', self.message)
    def warning(self,message):
        self.message = message
        nn = 30
        logging.basicConfig(level=logging.WARNING,
                            format='%(asctime)s %(levelname)-8s %(message)s',
                            filename=logfile)
        logging.warning('bkeep %s', self.message)
    def error(self,message):
        self.message = message
        nn = 30
        logging.basicConfig(level=logging.ERROR,
                            format='%(asctime)s %(levelname)-8s %(message)s',
                            filename=error_logfile)
        logging.error('bkeep %s', self.message)
    def critical(self,message):
        self.message = message
        nn = 30
        logging.basicConfig(level=logging.CRITICAL,
                            format='%(asctime)s %(levelname)-8s %(message)s',
                            filename=logfile)
        logging.critical('bkeep %s', self.message)
