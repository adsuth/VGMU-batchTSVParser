
"""
Utility that aims to clean up the songParser directory.
Moves "NEO_" files to NEO_BIN
Moves "OLD_" files to OLD_BIN
"""

import shutil as su
import os
from globals import NEO_BIN, OLD_BIN 

def cleanUpAndQuit():
  cleanUpFiles()
  exit()

def cleanUpFiles():
  createDirIfNotExist( NEO_BIN )
  createDirIfNotExist( OLD_BIN )

  for dir in os.listdir( "./" ):
    if not os.path.isfile( dir ):
      continue
    if dir.startswith( "NEO_" ):
      moveToBin( dir, NEO_BIN )
    if dir.startswith( "OLD_" ):
      moveToBin( dir, OLD_BIN )

def moveToBin( tgt, dest ):
  su.copy( tgt, dest )
  os.remove( tgt )

def createDirIfNotExist( dir ):
  if not os.path.isdir( dir ):
    os.makedirs( dir )



cleanUpFiles()