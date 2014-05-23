import ConfigParser
cf_file = "/home/admin/zookeeper/zk.conf"
cf = ConfigParser.ConfigParser()
cf.read(cf_file)
def get_secs():
    try:
        secs = cf.sections() 
        return secs
    except Exception,e:
        print e
        return 2

def get_opts():
    try:
        secs = cf.sections()
        opts = cf.options(secs[0])
        #['ips', 'name', 'port']
        return opts
    except Exception,e:
        print e
        return 2

def get_iteam(secs,opts):
    cf.get(secs,opts)
    try:
        str = cf.get(secs,opts)
        return str 
    except Exception,e:
        print e
        return 2

if __name__ == "__main__":
    print get_secs()
    print get_opts()
    
    for secs in get_secs():
        print secs,get_iteam(secs,'ip')
