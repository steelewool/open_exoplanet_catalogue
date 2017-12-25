import xml.etree.ElementTree as ET

import fnmatch
import os

import astropy.time
from astropy.time import Time
from astropy.time import TimeDelta

import time
from datetime import date
from datetime import datetime

# import subprocess

# subprocess.call ('ls')
# subprocess.call ('rm xml_files/*')
# subprocess.call ('ln -s systems/*.xml xml_files/.')

import commands
commands.getstatusoutput ('ls')
commands.getstatusoutput ('rm xml_files/*')
commands.getstatusoutput ('cd xml_files; ln -s ../systems/*.xml .;cd ..')
commands.getstatusoutput ('cd xml_files; ln -s ../systems_kepler/*.xml .;cd ..')
commands.getstatusoutput ('rm xml_files/WISE*.xml')
commands.getstatusoutput ('rm xml_files/PSO?J318.5-22.xml')
commands.getstatusoutput ('rm xml_files/CFBDSIR2149.xml')

# This creates a list of all of the files in systems and systems_kepler.
# If I can get this working in the 'for file' I won't need the silly softlinks

fileList = (os.listdir('systems') and os.listdir('systems_kepler'))

#worked: for file in (os.listdir('systems') and os.listdir('systems_kepler')):

#worked: for file in os.listdir('systems'):
#worked:     if fnmatch.fnmatch(file,'*xml'):
#worked:         print "file: ", file
#worked:         tree = ET.parse('systems/'+file)

count = 0

# Set up by grabbing the current date and then using the Time object from astropy.time

dateTime    = datetime.today()
nowPST      = Time (dateTime, scale='utc')

dateTimeUTC = datetime.utcnow()
now         = Time (dateTimeUTC, scale='utc')

for file in os.listdir('xml_files'):

# Because of the way I set my the xml_files directory all of the files are xml files

    if fnmatch.fnmatch(file, '*.xml'):
#        print 'file                  : ', file
        
        tree = ET.parse ('xml_files/'+file)
        root = tree.getroot();

        try: 
            star = tree.find('.//star')
        except:
            print 'tree.find raised an exception'
            
        for planet in star.findall('.//planet'):
            if planet.findtext ('istransiting') == '1':

                if star.findtext('magV') != None:
#                    print 'star.magV           : ', star.findtext('magV')
                    mag = star.findtext('magV')
                else:
                    if star.findtext('magB') != None:
#                        print 'star.magB      : ', star.findtext('magB')
                        mag = star.findtext('magB')
                    else:
                        if star.findtext('magJ') != None:
#                            print 'star.magJ             : ', star.findtext('magJ')
                            mag = star.findtext('magJ')

                planetPeriod = planet.findtext('period')

                # Look for a valid looking period, one that is not '' nore 'None'.
            
                if planetPeriod != '' and planetPeriod != None:

                    planetPeriod = float(planetPeriod)

                    if planet.findtext('transittime') != None:

                        transitTimeBJD = float(planet.findtext('transittime'))

                        t = Time(transitTimeBJD, format = 'jd', scale='utc')

                        delta  = now.jd - transitTimeBJD;
                
                        revolutionCount = delta / planetPeriod

                        intRevolutionCount = int(revolutionCount) + 1
                        nextTransit = transitTimeBJD + (intRevolutionCount * planetPeriod)

                        nextTransitTime = Time (nextTransit, format ='jd', scale = 'utc');

                        daysToTransit = nextTransit - now.jd

#
# Change the time to PST by subtracting 8 hours from the UTC time
#
                        nextTransitTimePST = nextTransit - (1.0/24.0*8.0)
                        nTTPST = Time (nextTransitTimePST, format='jd', scale='utc')

                        a = nextTransitTimePST
                        b = nowPST.jd + 1
                        c = a < b

                        if (float(mag) < 11) and (nextTransitTimePST < (nowPST.jd + 1)):
                            count = count + 1
                            print 'dateTime              : ', dateTime
                            print 'dateTimeUTC           : ', dateTimeUTC
                            print
                            print 'System name           : ', root.findtext('name')
                            print 'System rightascension : ', root.findtext('rightascension')
                            print 'System declination    : ', root.findtext('declination')
                            print 'System magnitude      : ', mag
                            print
                            print 'Planet name           : ', planet.findtext('name')
                            print 'Planet period         : ', planet.findtext('period') 
                            print
                            print 'transitTimeBJD        : ', transitTimeBJD
                            print 't.jd                  : ', t.jd
                            print 't.fits                : ', t.fits
                            print 'now                   : ', now
                            print 'now jd                : ', now.jd
                            print 'now fits              : ', now.fits
                            print 'delta                 : ', delta
                            print 'revolutionCount       : ', revolutionCount
                            print 'int revoultionCount   : ', int(revolutionCount) + 1
                            print 'nextTransit           : ', nextTransit
                            print 'nextTransitTime       : ', nextTransitTime.fits
                            print 'daysToTransit         : ', daysToTransit
                            print 'nextTransitTimePST    : ', nextTransitTimePST
                            print 'nTTPST.jd             : ', nTTPST.jd
                            print 'nTTPST.fits           : ', nTTPST.fits, 'PST'

                            print 'count: ', count
                            print
                            




        






