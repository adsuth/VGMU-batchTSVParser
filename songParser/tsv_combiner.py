import cleanup
import globals

def combineTSV( sourceFiles, targetFile ):
  cleanup.createDirIfNotExist( globals.TSV_BIN )
  output = ""

  for file in sourceFiles:
    with open( file, "r" ) as f:
      for line in f:
        output += line.replace( ",", "\t") if file.endswith( ".csv" ) else line  
  
  if targetFile.endswith( ".tsv" ):
    targetFile = targetFile[ :targetFile.rfind( "." ) ] + ".tsv"

  with open( globals.TSV_BIN + targetFile, "w" ) as o:
    for line in output:
      o.write( line )
        