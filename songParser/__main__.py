from OLD_parser import processJSON as oldProcessor
from NEO_parser import processJSON as neoProcessor

import cleanup

import os
import re
import json
from argparse import ArgumentParser
from globals import NEO_BIN, OLD_BIN, TSV_BIN
from tsv_combiner import combineTSV 


"""
TSV Batch Processor
-------------------
Batch converter of VGMB TSV and CSV files, simply provide the directory
of any file or folder and the program will process them into one big JSON file,
ready to use. Note: The formatting follows the new VGMVersus format.

Arguments:
  sourceDir >> The directory (or directories) with TSV or CSV files to be processed.
               You can provide them as files or folders, files not of the CSV or TSV
               type will be ignored.
  targetDir >> Optional, the directory of the output JSON file. Extensions will be ignored,
               so it doesn't matter if you don't provide one. Default is autogenerated, and
               placed in the same directory as this script.
  verbose   >> Optional, if given, turns on verbose messaging. This will provide error and
               warning messages for given source paths - whether they could be found etc.
  combine   >> Optional, if given, will ONLY combine given TSV or CSV files.
"""

class CLR:
  HEADER    = '\033[95m'
  OKBLUE    = '\033[94m'
  OKCYAN    = '\033[96m'
  OKGREEN   = '\033[92m'
  WARNING   = '\033[93m'
  FAIL      = '\033[91m'
  ENDC      = '\033[0m'
  BOLD      = '\033[1m'
  UNDERLINE = '\033[4m'

class STATE:
  def __init__( self ):
    self.args = None
    self.sourceFiles = []
    self.targetFile  = ""
    self.verboseMessagingOn = False
    self.useLegacyParser = False
  
  def _getSourceFiles( self ):
    output = []
    for dir in self.args.sourceDir:
      if os.path.isdir( dir ):
        dir = dir if dir.endswith( "/" ) else dir + "/"
        for file in os.listdir( dir ):
          if file.lower().endswith( ".tsv" ) or file.lower().endswith( ".csv" ):
            output.append( dir + file )
          else:
            verbosePrint( f"{CLR.FAIL}Directory {file} is not a CSV or TSV. Rejected. {CLR.ENDC}" )
      
      elif os.path.isfile( dir ):
        if dir.lower().endswith( ".tsv" ) or dir.lower().endswith( ".csv" ):
          output.append( dir )
        else:
          verbosePrint( f"{CLR.FAIL}Directory {file} is not a CSV or TSV. Rejected. {CLR.ENDC}" )

      else:
        verbosePrint( f"{CLR.FAIL}Directory {dir} is not a folder nor a file. {CLR.ENDC}" )

    return output

  def _getTargetFile( self ):
    if self.args.targetDir == None:
      directory = ""
      for source in self.sourceFiles:
        source = source.replace( "\\", "/" )
        directory += source[ source.rfind( "/" )+1:source.rfind( "." ) ] + "_"
      
      directory += "songs"

    else:
      directory = self.args.targetDir[0] if isinstance( self.args.targetDir, list ) else self.args.targetDir
      
    return getUniqueDirName( directory )

  def initArgs( self, args ):
    self.args = args
    self.verboseMessagingOn = args.verboseMessagingOn
    self.sourceFiles = self._getSourceFiles()
    self.targetFile = self._getTargetFile()

def verbosePrint( msg ):
  if state.verboseMessagingOn:
    print( msg )

def getUniqueDirName( dir ):
  copyNumber = 0
  newDir = dir[:dir.rfind( "." )] if "." in dir else dir

  if not os.path.isfile( OLD_PREFIX + newDir + ".json" ) and not os.path.isfile( NEW_PREFIX + newDir + ".json" ):
    return newDir + ".json"

  while os.path.isfile( f"{OLD_PREFIX}{newDir} ({copyNumber}).json" ) or os.path.isfile( f"{NEW_PREFIX}{newDir} ({copyNumber}).json" ):
    copyNumber += 1
  return f"{newDir} ({copyNumber}).json"

def fetchArguments():
  parser = ArgumentParser( f"{CLR.WARNING}Batch converter of VGMB TSV and CSV files {CLR.ENDC}\n simply provide the directory \nof any file or folder and the program will process them into one big JSON file, \nready to use. Note: The formatting follows the new VGMVersus format. " )
  parser.add_argument( "sourceDir", nargs = "+", help = f"{CLR.BOLD}Source directories{CLR.ENDC}, folders or files, containing TSV or CSV files for processing. ", metavar="" )
  parser.add_argument( "-t", "--target", help = f"{CLR.BOLD}Target directory{CLR.ENDC} for the JSON output. ", default = None, dest = "targetDir", metavar="" )
  parser.add_argument( "-v", "--verbose", action = "store_true", dest = "verboseMessagingOn", help = f"If present, {CLR.BOLD}verbose messaging{CLR.ENDC} will be enabled - error and warning messages will be shown. ")
  parser.add_argument( "-c", "--combine", action = "store_true", dest = "combineTSV", help = f"If present, {CLR.BOLD}will ONLY combine TSV and CSV into one master file{CLR.ENDC}.")

  return parser.parse_args()

def getPluralisedFile( qty ):
  return "s" if qty > 1 else ""

def main():
  state.initArgs( fetchArguments() )
  qty = len( state.sourceFiles )

  if state.args.combineTSV:
    if qty < 2:
      print( f"{CLR.WARNING}Nothing to do, only one file was given.\n {CLR.ENDC}" )
      quit()
    
    state.targetFile = state.targetFile[:state.targetFile.rfind( ".json" )] + ".tsv"

    print( f"{CLR.BOLD}Starting to combine {qty} TSV or CSV files ...{CLR.ENDC}" )
    combineTSV( state.sourceFiles, state.targetFile )
    print( f"{CLR.OKGREEN}Done. Dumped to {TSV_BIN}{ state.targetFile }{CLR.ENDC}\n" )
    quit()



  old_data = {}
  neo_data = {}
  
  
  if qty < 1:
    print( f"{CLR.WARNING}No files to process. If this is wrong, use --verbose to debug.{CLR.ENDC}\n" )
    exit()

  print( f"{CLR.BOLD}Starting to process {qty} file{getPluralisedFile( qty )} ...{CLR.ENDC}" )

  for file in state.sourceFiles:
    print( f"{CLR.OKCYAN}Processing {file} ...{CLR.ENDC}" )
    neo_data = {**neo_data, **neoProcessor( file )}
    old_data = {**old_data, **oldProcessor( file )}
  
  cleanup.createDirIfNotExist( NEO_BIN )
  cleanup.createDirIfNotExist( OLD_BIN )

  with open( NEO_BIN + state.targetFile, "w" ) as outputFile:
    json.dump( neo_data, outputFile )
  with open( OLD_BIN + state.targetFile, "w" ) as outputFile:
    json.dump( old_data, outputFile )


  print( f"{CLR.OKGREEN}Done.\nDumped to {state.targetFile}\nNew parser >> {NEO_BIN}\nOld parser >> {OLD_BIN}{CLR.ENDC}\n" )
  
# def combineTSV():

#   with open( state.targetFile, "w" ) as output:

# # # # #
# Entry #
# # # # #
if __name__ == "__main__":
  state = STATE()
  NEW_PREFIX = "NEO_"
  OLD_PREFIX = "OLD_"
  main()