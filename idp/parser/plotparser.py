"""
This file is part of imdb-data-parser.

imdb-data-parser is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

imdb-data-parser is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with imdb-data-parser.  If not, see <http://www.gnu.org/licenses/>.
"""

from .baseparser import BaseParser
from ..utils.regexhelper import *
import logging

class PlotParser(BaseParser):
    """
    RegExp: /(.+?): (.*)/g
    pattern: (.+?): (.*)
    flags: g
    2 capturing groups: 
       group 1: (.+?)   type of the line
       group 2: (.*)    if the line-type is PL then this line is plot, not the whole but one line of it
                        if the line-type is MV then this line is movie
    """
  
    # properties
    baseMatcherPattern = "(.+?): (.*)"
    inputFileName = "plot.list"
    numberOfLinesToBeSkipped = 15

    def __init__(self, preferencesMap):
        self._preferencesMap = preferencesMap

    @property
    def preferencesMap(self):
        return self._preferencesMap

    def parse_into_tsv(self):
        import time
        startTime = time.time()

        inputFile = self.get_input_file()
        outputFile = self.get_output_file()
        counter = 0
        fuckedUpCount = 0

        title = ""
        plot = ""

        numberOfProcessedLines = 0

        for line in inputFile :
            if(numberOfProcessedLines >= self.numberOfLinesToBeSkipped):
                matcher = RegExHelper(line)
                isMatch = matcher.match(self.baseMatcherPattern)

                if(isMatch):
                    if(matcher.group(1) == "MV"): #Title
                        if(title != ""):
                            outputFile.write(title + self.seperator + plot + "\n")

                        plot = ""
                        title = matcher.group(2)

                    elif(matcher.group(1) == "PL"): #Descriptive text
                        plot += matcher.group(2)
                    elif(matcher.group(1) == "BY"):
                        continue
                    else:
                        logging.critical("Unhandled abbreviation: " + matcher.group(1) + " in " + line)
                #else:
                    #just ignore this part, useless lines
            numberOfProcessedLines +=  1
          
        # Covers the last item
        outputFile.write(title + self.seperator + plot + "\n")
          
        outputFile.flush()
        outputFile.close()
        inputFile.close()

        logging.info("Finished with " + str(fuckedUpCount) + " fucked up line\n")
        logging.info("Duration: " + str(round(time.time() - startTime)))

    def parse_into_db(self):
        #TODO
        pass
