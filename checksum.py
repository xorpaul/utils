#!/usr/bin/env python

"""
 Filename: checksum.py
 Version: 1.0
 Requires: sys, os, md5, string
 Date: 2010-05-25 09:55
 Author: Andreas Paul

 This script downloades various source archives
 with matching checksum files, verifies these checksums
 and checking the genuineness with the signature file.
"""

import sys
import os
import string 
try: 
   from hashlib import md5
except ImportError:
   from md5 import md5

usage = """
usage: %s [package ...]
package ...  : one or multiple packages to download, sum, validate and authenticate

Recognized parameters are:
  tomcat-[VERSION] | apache-[VERSION] | php-[VERSION] | jk-[VERSION]

Examples of valid packages are:
  - tomcat-7.0.23
  - apache-2.2.21
  - php-5.3.8
  - jk-1.2.32
  
Example call with arguments:
  %s php-5.3.8 apache-2.2.21
""" % (sys.argv[0], sys.argv[0])


def getSum(filename, out):
  """ Identifies the requested package and handles the download
      
  The desired package is selected via primitive string matching.
  To download the source archive the filename has to be modified
  with the appending of an extension (+ '.tar.gz').
  Using the package variable an appropriate mirror will be chosen
  to download from. If the first mirror couldn't provide the
  archive a different mirror will be selected until the successful
  download occured or all mirrors has been tried.
  Same procedure will be used to download the checksum files and 
  signature files.
  The function will bomb out if the download of the source 
  archive and/or the download of the checksum or signature file fails.

  Args:
    filename: A string with the filename of the downloaded source archive,
      which is used to download the source archive, the validation and 
      signature file.
    out: Used to define output channel.

  Returns:
    1: If the download of the source archive and/or the download 
      of the checksum file fails.
    0: All download, sum, validation and authenticity of the package 
      has been successful.
  """
  out.write('#############\n')
  out.write(filename + '\n')
  out.write('#############\n')
  
  origParameter = filename
  wgetParamSrc = 'wget --tries=2 --timeout=10 '
  wgetParamHash = 'wget --tries=2 --timeout=10 -nv '

  ######################
  # package identification
  ######################

  if 'apache' in filename:
    filename = string.replace(filename, 'apache', 'httpd') + '.tar.gz'
    package = 'apache'
  elif 'tomcat' in filename:
    version = string.split(filename, '-')
    filename = 'apache-' + filename + '-src.tar.gz'
    package = 'tomcat'
  elif 'jk' in filename:
    version = filename
    filename = string.replace(filename, 'jk', 'tomcat-connectors') + '-src.tar.gz'
    package = 'jk'
  elif 'php' in filename:
    filename = filename + '.tar.gz'
    package = 'php'
    
  else:     # bomb out if no recognized package is given       
    out.write('not a recognized package: \n %s \n' % (filename))
    return 1  # bomb out!


  ######################
  # source archive download
  ######################
    
  header('downloading source archive', out)

  if package == 'apache':

    #mirrors = array(['http://apache.mirroring.de/httpd/', '', ''])

    if not os.path.isfile(filename):
      os.system(wgetParamSrc + 'http://www.apache.org/dist/httpd/' + filename)
    if not os.path.isfile(filename):
      os.system(wgetParamSrc + 'http://apache.openmirror.de/httpd/' + filename)
    else:   # no need to download source archive because it already exists
      out.write('Using already existing source archive %s\n' % (filename))
  
  elif package == 'tomcat':
    endURL = version[1][0] + '/v' + version[1] + '/src/'
    if not os.path.isfile(filename):
      os.system(wgetParamSrc + 'http://apache.prosite.de/tomcat/tomcat-' + endURL + filename)
    if not os.path.isfile(filename):
      os.system(wgetParamSrc + 'http://apache.easy-webs.de/tomcat/tomcat-' + endURL + filename)
    if not os.path.isfile(filename):
      os.system(wgetParamSrc + 'http://apache.abdaal.com/tomcat/tomcat-' + endURL + filename)
    else:   # no need to download source archive because it already exists
      out.write('Using already existing source archive %s\n' % (filename))

  elif package == 'jk':
    if not os.path.isfile(filename):
      os.system(wgetParamSrc + 'http://www.apache.org/dist/tomcat/tomcat-connectors/jk/' + filename)
    else:   # no need to download source archive because it already exists
      out.write('Using already existing source archive %s\n' % (filename))

  elif package == 'php':
    if not os.path.isfile(filename):
      print wgetParamSrc + 'http://de2.php.net/get/' + filename + '/from/this/mirror -O' + filename
      os.system(wgetParamSrc + 'http://de2.php.net/get/' + filename + '/from/this/mirror -O' + filename)
    elif not os.path.isfile(filename):
      os.system(wgetParamSrc + 'http://de2.php.net/get/' + filename  + '/from/de.php.net/mirror')
    elif not os.path.isfile(filename):
      os.system(wgetParamSrc + 'http://de2.php.net/get/' + filename  + '/from/de.php.net/mirror')
    else:   # no need to download source archive because it already exists 
      out.write('Using already existing source archive %s\n' % (filename))

  ######################
  # checksum download
  ######################

  if os.path.isfile(filename):
    header('downloading checksum', out)
    checksumFile = filename + '.md5'
    if package == 'tomcat':
      os.system(wgetParamHash + 'http://www.apache.org/dist/tomcat/tomcat-' + endURL + checksumFile)
    elif package == 'apache':
      os.system(wgetParamHash + 'http://www.apache.org/dist/httpd/' + checksumFile)
    elif package == 'jk':
      os.system(wgetParamHash + 'http://www.apache.org/dist/tomcat/tomcat-connectors/jk/' + checksumFile)
    elif package == 'php':
      # php.net doesn't provide a dedicated md5 file,
      # but makes the checksums available on the download site.
      # Therefore the download site can be used as a checksum file
      # by giving it an appropriate filename (-O wget parameter).
      os.system(wgetParamHash + '-O ' + checksumFile + ' http://www.php.net/downloads.php')

    # download of checksum file failed
    if not os.path.isfile(checksumFile):
      out.write('Download of checksum file %s failed!\nCheck version or mirrors!\n' % (checksumFile))
      return 1  # bomb out!

  # download of source archive unsuccessful
  else:
    out.write('Download of package %s failed!\nCheck version or mirrors!\n' % (filename))
    return 1  # bomb out!

  ######################
  # signature download
  ######################

  if package in ['tomcat', 'apache', 'jk']:
      header('downloading signature', out)

      signatureFile = filename + '.asc'
      if package == 'tomcat':
        os.system(wgetParamHash + 'http://www.apache.org/dist/tomcat/tomcat-' + version[1][0] + '/KEYS')
        os.system(wgetParamHash + 'http://www.apache.org/dist/tomcat/tomcat-' + endURL + signatureFile)
      elif package == 'apache':
        os.system(wgetParamHash + 'http://www.apache.org/dist/httpd/KEYS')
        os.system(wgetParamHash + 'http://www.apache.org/dist/httpd/' + signatureFile)
      elif package == 'jk':
        os.system(wgetParamHash + 'http://www.apache.org/dist/httpd/KEYS')
        os.system(wgetParamHash + 'http://www.apache.org/dist/tomcat/tomcat-connectors/jk/' + signatureFile)
      # PHP offers no signatures :*(

      # download of signature file failed
      if not os.path.isfile(signatureFile):
        out.write('Download of signature file %s failed!\nCheck version or mirrors!\n' % (signatureFile))
        return 1  # bomb out!

  return checkPackage(filename, origParameter, out)


def checkPackage(filename, origParameter, out=sys.stdout):
  """ Handles the result of the hash and authenticity validation.

  Tries to open the source archive to check the reading 
  permissions of the file and send the filepointer and filename
  to the next function, which handles the validation.
  The returned result will be saved in the boolean variable (found).
  The md5 file containing the checksums will always be deleted
  after the validation took place.

  Args:
    filename: A string with the filename of the downloaded source archive,
      which is used to open the validation file and for std output.
    origParameter: The original parameter with which the download function
      has been called before. This will be used to call the download 
      function (getSum) again in case the validation has failed and the 
      user insists to retry the download and validation.
    out: Used to define output channel.

  Returns:
    No other return value needed - either it has been reported 
    that the source file is valid, because a matching hash 
    has been found, or the user got informed of a possibly 
    invalid source archive and gets the option to retry the download.
  """
  try:
    filePointer = open(filename, 'r')
  except IOError, msg:
    sys.stderr.write('%s: Can\'t open: %s\n' % (filename, msg))
    return 1

  # calculate the checksum of the filePointer
  # and match the hash against the checksum file
  found = calcSum(filePointer, filename, out)

  filePointer.close()

  # import the KEYS file and
  # try to verify the authenticity 
  valid = True
  if 'php' not in filename:
      valid = checkSig(filename, out)
    
  #print "filename:", filename
  #print "valid:", valid

  md5File = filename + '.md5'
  signatureFile = filename + '.asc'
  os.system('rm ' + md5File)    # always remove the checksum file
  os.system('rm -f KEYS')    # always remove the KEYS file
  os.system('rm -f ' + signatureFile)    # always remove the signature file

  abort = False

  if not found:   # no matching hash has been found in the checksum file
    out.write('calculated checksum from file %s not found in verification file %s!\n' % (filename, md5File))
    out.write('-->> integrity of file %s is probably invalid!\n\n' % (filename))
    prompt = raw_input('Delete downloaded source file and retry? (Y/n): ')

    if prompt not in ('n', 'no', 'N', 'No'):
      # delete the source archive and retry the download
      os.system('rm ' + filename)
      found = getSum(origParameter, out)
      abort = True    # user wants to stop!

  if not valid and not abort:   # authenticity of file is invalid
    out.write('-->> authenticity of file %s is probably invalid!\n\n' % (filename))
    prompt = raw_input('Delete downloaded source file and retry? (Y/n): ')

    if prompt not in ('n', 'no', 'N', 'No'):
      # delete the source archive and retry the download
      os.system('rm ' + filename)
      found = getSum(origParameter, out)

  # user was informed about the result of the validation -> return
  return found


def calcSum(filePointer, filename, out=sys.stdout):
  """ Calculates the checksum and validates it.

  Tries to read in 8 bytewise of the given filepointer until the end of the file
  and from that calculates the md5 hash.
  After that it opens the validation file containing the md5 checksums
  and checks every line for the md5 hash calculated before.

  Args:
    filePointer: A filepointer to the source archive downloaded before, which 
      is read in and used to calculate the checksum.
    filename: A string with the filename of the downloaded source archive,
      which is used to open the validation file and for std output.
    out: Used to define output channel.

  Returns:
    A boolean (found) containing the success of the validation.
    If the boolean is True the calculated md5 sum has been
    found in the validation file. Otherwise it will remain set 
    to False if no matching hash is found in the validation file.
  """
  m = md5()
  try:
    while 1:
      data = filePointer.read(8096)
      if not data:
        break
      m.update(data)
  except IOError, msg:
    sys.stderr.write('%s: I/O error: %s\n' % (filename, msg))
    return 1

  header('validating checksum', out)
  md5hash = m.hexdigest()  
  checksumFile = filename + '.md5'
  hashfp = open(checksumFile, 'r')
  out.write('calculated checksum: \n %s %s\n' % (md5hash, filename))
  found = False
  for line in hashfp:
    # uncomment next line to simulate invalid downloads
    # md5hash = 'e6504ce44628ca18deaa5wr0ngHasH'
    if md5hash in line:
      out.write('downloaded checksum: \n %s \n' % (line))
      out.write('-->> file %s seems to be valid!\n\n' % (filename))
      found = True
      break   # found matching hash! bomb out!

  hashfp.close()
  return found


def checkSig(filename, out=sys.stdout):
  """ Check the authenticity of the downloaded source
  
  Import all keys from the KEYS file and try to verify the
  authenticity of the downloaded source archive by Using
  the gpg command.
  Write the output to a temporary file and delete this file 
  after the check.

  Args.
    filename: A string with the filename of the downloaded source archive,
      which is used for user output only.
    out: Used to define output channel.

  Returns:
    A boolean (valid) containing the success of the authenticity check.
    If the boolean is True the signature of the downloaded source archive
    has been validated.
    Otherwise it will remain set to False if the signature was invalid.
  """

  header('validating signature', out)
  signatureFile = filename + '.asc'
  tmpGPGoutput = 'signature.tmp'
  
  os.system('gpg --import KEYS 2> /dev/null')
  os.system('gpg --verify ' + signatureFile + ' 2>' + tmpGPGoutput)

  valid = False

  try:
    filePointer = open(tmpGPGoutput, 'r')
  except IOError, msg:
    sys.stderr.write('%s: Can\'t open: %s\n' % (tmpGPGoutput, msg))
    return 1

  for line in filePointer:
    if 'Good signature from' in line:
      print line
      out.write('-->> authenticity of file %s seems to be valid!\n\n' % (filename))
      valid = True
      break   # found good signature! bomb out!

  filePointer.close()

  # always remove the tmp gpg output file
  os.system('rm ' + tmpGPGoutput)    

  return valid


def main(args = sys.argv[1:], out=sys.stdout):
  """ Iterates over the arguments and handles the correct usage

  Prints the usage string if the script was called
  without any arguments and terminates.
  If called with one or multiple arguments it will
  send each one of them to the next functioni with
  one argument at a time.

  Args:
    args: List of the sys arguments the script has been called 
      with, exculding the first ([0]) which contains the 
      filename of the executed script.
    out: Used to define output channel.

  Returns:
    1: Script was called with no arguments. Print usage and
      terminate.
    0: All Download, Sum and Validation of all packages has been
      successful.
  """
  if not args:  # no arguments found
    out.write(usage)
    return 1  # bomb out!

  # download src, hash and validate for each package
  for filename in args: 
    returnCode = getSum(filename, out)
  return returnCode


def header(string, out):
  """ Print function to uniform output """
  out.write('### %s...\n' % (string))


if __name__ == '__main__' or __name__ == sys.argv[0]:
  sys.exit(main(sys.argv[1:], sys.stdout))
