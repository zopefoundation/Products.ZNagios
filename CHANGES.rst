Changelog
=========

0.7.3 (2017-03-22)
------------------

- Always close connection when there is an exception/error in a probe.
  [bsuttor]

- Python2.7 compatibility for munin_client.py 
  [fRiSi]


0.7.2 (2016-09-26)
------------------

- Use same way to get stats database than stats connection probes.
  [bsuttor]


0.7.1 (2015-08-11)
------------------

- Do not get threads in stats probe.
  [bsuttor]

- Fix beautify_return_values for date.
  [bsuttor]


0.7 (2015-07-17)
----------------

- Add MANIFEST.in
  [bsuttor]

- Fix stats probe for probe which are collection and other args
  [bsuttor]

- Add stats probe
  [jfroche]


0.6 (2012-12-19)
----------------

- Enable registration of znagios probes as zc.monitor utilities (using five.z2monitor)

0.5 - 2011-03-14
----------------

- `munin_client.py` can handle multiple databases now.
  [davisagli]

0.4.2 - 2010-10-21
------------------

- fixed ``Control_Panel/munin`` for Zope 2.10.11
  which is used for plone 3.3.4 and 3.3.5 and ships
  w/o version information
  (see https://bugs.launchpad.net/zope2/+bug/510477)
  [fRiSi]

0.4.1 - 2010-06-14
------------------

- fixed ``Control_Panel/munin`` for Zope >= 2.11
  (conflict_error are not global anymore)
  [fRiSi]

0.4 - 2009-11-19
----------------

- uptime is given in days now, instead of seconds which is much more readable.
  `fetch` still returns seconds for backward compatibility,
  but `config` tells to compute the value (``uptime.cdef uptime,86400,/``)
  [fRiSi]

- `zeo_munin.py` can handle multiple Databases now
  [fRiSi]

- Documented munin data and configuration in README
  [fRiSi]

- Corrected labels in `Per connection caches` graph
  [fRiSi]

- Added `dbsize` graph to `munin_client.py`
  [fRiSi]


0.3 - 2009-02-25
----------------

- Changed an import of Zope.App to Zope2.App for compatibility with recent
  Zope versions.
  [hannosch]

- Added package infrastructure.
  [hannosch]

- Moved the source code from https://svn.gocept.com/repos/gocept/ZNagios/trunk
  to the svn.zope.org repository at revision 29315.
  [hannosch]

0.2 - 2008-05-26
----------------

- Remove hard-coded authorization string.
  [ctheune]

- A script for reading data from a ZEO monitor server.
  [ctheune]

- Added basic munin support.
  [ctheune]

- Original implementation.
