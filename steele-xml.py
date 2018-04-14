# python 2.x
import xml.etree.ElementTree as ET, urllib, gzip, io

import astropy.time
from astropy.time import Time
from astropy.time import TimeDelta

import time
from datetime import date
from datetime import datetime

url = "https://github.com/OpenExoplanetCatalogue/oec_gzip/raw/master/systems.xml.gz"
oec = ET.parse(gzip.GzipFile(fileobj=io.BytesIO(urllib.urlopen(url).read())))


# Output mass and radius of all planets 
for planet in oec.findall(".//planet"):
    print [planet.findtext("name"),planet.findtext("mass"), planet.findtext("radius")]
 
# Find all circumbinary planets 
for planet in oec.findall(".//binary/planet"):
    print planet.findtext("name")
 
# Output distance to planetary system (in pc, if known) and number of planets in system
for system in oec.findall(".//system"):
    print system.findtext("distance"), len(system.findall(".//planet"))

# Searching for transiting planets and estimate when the next transit will occur.

dt2 = TimeDelta(50.0, format='sec')
dt8hr = TimeDelta(60*60*8, format='sec')

for planet in oec.findall(".//planet"):
    if planet.findtext("istransiting") == '1':
        if planet.findtext("transittime") != None:
            print [planet.findtext("name"),   planet.findtext("istransiting"), planet.findtext("mass"),
                   planet.findtext("radius"), planet.findtext("transittime"),  planet.findtext("period"),
                   planet.findtext("lastupdate")]
            planetPeriod = planet.findtext('period')

            # Look for a valid looking period, one that is not '' nore 'None'.
            
            if planetPeriod != '' and planetPeriod != None:

                planetPeriod = float(planetPeriod)
                print "period              : ", planetPeriod
                
                transitTimeBJD = float(planet.findtext('transittime'))
                print "transitTimeBJD      : ", transitTimeBJD

                t = Time(transitTimeBJD, format = 'jd', scale='utc')
                print "t.jd                : ", t.jd
                print "t.fits              : ", t.fits

                dateTime = datetime.today();
                print "dateTime            : ", dateTime

                dateTimeUTC = datetime.utcnow()
                print "dateTimeUTC         : ", dateTimeUTC
                
                now = Time (datetime.today())
                now = Time (dateTimeUTC, scale='utc');
                
                print "now                 : ", now
                print "now jd              : ", now.jd
                print "now fits            : ", now.fits

                delta  = now.jd - transitTimeBJD;
                print "delta               : ", delta
                
                revolutionCount = delta / planetPeriod
                print "revolutionCount     : ", revolutionCount

                print "int revoultionCount : ", int(revolutionCount) + 1
                intRevolutionCount = int(revolutionCount) + 1
                nextTransit = transitTimeBJD + (intRevolutionCount * planetPeriod)
                print "nextTransit         : ", nextTransit

                nextTransitTime = Time (nextTransit, format ='jd', scale = 'utc');
                print "nextTransitTime     : ", nextTransitTime.fits

                daysToTransit = nextTransit - now.jd
                print "daysToTransit       : ", daysToTransit

                nextTransitTimePST = nextTransit - (1.0/24.0*8.0)
                print "nextTransitTimePST  : ", nextTransitTimePST

                nTTPST = Time (nextTransitTimePST, format='jd', scale='utc')
                print "nTTPST.jd           : ", nTTPST.jd
                print "nTTPST.fits         : ", nTTPST.fits, "PST"

# print "url : ", url
# print "oec : ", oec

