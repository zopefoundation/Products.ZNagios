# -*- coding: utf-8 -*-
from cStringIO import StringIO
from os import getpid
from Products.ZNagios import get_activity
from Products.ZNagios import get_conflictInfo
from Products.ZNagios import get_refcount
from zc.z3monitor.interfaces import IZ3MonitorPlugin
from Zope2 import app as App

import inspect
import psutil
import re
import time
import ZODB.interfaces
import zope.component


def zc_uptime(connection):
    """uptime of the zope instance in seconds"""
    app = App()
    try:
        elapsed = time.time() - app.Control_Panel.process_start
        print >> connection, elapsed
    except:
        print >> connection, 0
    finally:
        app._p_jar.close()


def zc_dbsize(connection, database='main'):
    """size of the database (default=main) in bytes"""
    app = App()
    try:
        db = app.Control_Panel.Database[database]
        print >> connection, db._p_jar.db().getSize()
    except:
        print >> connection, 0
    finally:
        app._p_jar.close()


def zc_objectcount(connection, database='main'):
    """number of object in the database (default=main)"""
    db = zope.component.getUtility(ZODB.interfaces.IDatabase, database)
    print >> connection, db.objectCount()


def zc_refcount(connection):
    """the total amount of object reference counts"""
    app = App()
    try:
        print >> connection, get_refcount(app)
    except:
        print >> connection, 0
    finally:
        app._p_jar.close()


def zc_errorcount(connection, objectId=None):
    """number of error present in error_log (default in the root).

    You can also provide the objectId of the object that contains another error_log
    """
    app = App()
    try:
        if objectId is not None:
            app = getattr(app, objectId)
        print >> connection, len(app.error_log._getLog())
    except:
        print >> connection, 0
    finally:
        app._p_jar.close()


def zc_conflictcount(connection):
    """number of all conflict errors since startup"""
    print >> connection, get_conflictInfo().conflict_errors


def zc_unresolved_conflictcount(connection):
    """number of all unresolved conflict errors since startup"""
    print >> connection, get_conflictInfo().unresolved_conflict_errors


def zc_dbactivity(connection, database='main', last_minutes=60 * 5):
    """number of load, store and connections on database (default=main) for the last x minutes (default=5)"""
    app = App()
    try:
        db = app.Control_Panel.Database[database]
        activity = get_activity(db)
        print >> connection, activity['total_load_count'], " ", activity['total_store_count'], " ", activity['total_connections']
    except:
        print >> connection, 0, " ", 0, " ", 0
    finally:
        app._p_jar.close()


def zc_requestqueue_size(connection):
    """number of requests waiting in the queue to be handled by zope threads"""
    from ZServer.PubCore import _handle
    queue_size = 0
    if _handle is not None:  # no request yet
        zrendevous = _handle.im_self
        queue_size = len(zrendevous._lists[1])
    print >> connection, queue_size


def zc_memory_percent(connection):
    pid = getpid()
    p = psutil.Process(pid)
    print >> connection, p.memory_percent()


def zc_cpu_times(connection):
    pid = getpid()
    p = psutil.Process(pid)
    cpu_times = p.cpu_times()
    print >> connection, cpu_times.user, cpu_times.system


GAUGE_RETURNS = {'cpu_times': ['user', 'system'],
                 'dbactivity': ['load_count', 'store_count', 'total_connections']}


def return_values(stream, prefix):
    values = re.split(' +', stream.getvalue().strip())
    if prefix in GAUGE_RETURNS.keys():
        return dict(zip(GAUGE_RETURNS.get(prefix, [prefix]), values))
    else:
        return {prefix: " ".join(values)}


def beautify_return_values(connection, tempStream, name, dbname=None):
    values = return_values(tempStream, name)
    if dbname is not None:
        prefix = '%s.%s' % (dbname, name)
    else:
        prefix = name
    for probe_detail, value in values.items():

        if len(values) > 1:
            print >> connection, str("%s.%s : %s" % (prefix, probe_detail, value))
        else:
            print >> connection, str("%s : %s" % (prefix, value))


def stats(connection):
    app = App()
    dbs = app.Control_Panel.Database.getDatabaseNames()
    dbs.remove('temporary')
    for name, probe in zope.component.getUtilitiesFor(IZ3MonitorPlugin):
        if name in ['help', 'stats', 'threads']:
            continue
        argspec = inspect.getargspec(probe)
        if 'database' in argspec.args:
            for dbname in dbs:
                try:
                    tempStream = StringIO()
                    probe(tempStream, dbname)
                    beautify_return_values(connection, tempStream, name, dbname)
                except:
                    pass
        elif 'connection' in argspec.args:
            tempStream = StringIO()
            try:
                probe(tempStream)
                beautify_return_values(connection, tempStream, name)
            except:
                pass
    app._p_jar.close()
