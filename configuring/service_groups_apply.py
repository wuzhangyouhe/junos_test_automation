from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos.exception import ConnectError
from jnpr.junos.exception import LockError
from jnpr.junos.exception import UnlockError
from jnpr.junos.exception import ConfigLoadError
from jnpr.junos.exception import CommitError

def groups_apply_by_cli(hostname, username, password, cli):
    # open a connection with the device and start a NETCONF session
    try:
        dev = Device(host=hostname,username=username,password=password)
        dev.open()
        dev.timeout = 300
    except ConnectError as err:
        print ("Cannot connect to device: {0}".format(err))
        return
    dev.bind(cu=Config)
    # Lock the configuration, load configuration changes, and commit
    print ("Locking the configuration")
    try:
        dev.cu.lock()
    except LockError as err:
        print ("Unable to lock configuration: {0}".format(err))
        dev.close()
        return
    try:
        dev.cu.load(cli, format='set')
        dev.cu.pdiff()
    except (ConfigLoadError, Exception) as err:
        print ("Unable to load configuration changes: {0}".format(err))
        print ("Unlocking the configuration")
        try:
                dev.cu.unlock()
        except UnlockError:
            print ("Unable to unlock configuration: {0}".format(err))
        dev.close()
        return

    print("Committing the configuration")
    try:
        dev.cu.commit_check()
        dev.cu.commit(confirm=2, comment='Apply service group configurations')
        dev.cu.commit(comment='Confirm commit by PyEZ SQT Auto-provisioning Tool.',
                      timeout=120)
    except CommitError as err:
        print("Unable to commit configuration: {0}".format(err))
        print("Unlocking the configuration")
        try:
            dev.cu.unlock()
        except UnlockError as err:
            print("Unable to unlock configuration: {0}".format(err))
            dev.close()
            return
    print("Unlocking the configuration")
    try:
        dev.cu.unlock()
    except UnlockError as err:
        print("Unable to unlock configuration: {0}".format(err))
    # End the NETCONF session and close the connection
    dev.close()