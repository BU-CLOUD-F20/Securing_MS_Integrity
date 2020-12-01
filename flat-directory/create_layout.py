#!/usr/bin/env python2
#from securesystemslib.util import import_rsa_key_from_file
from in_toto.models.layout import Layout
from in_toto.models.metadata import Metablock
import json
import sys
import getpass


import securesystemslib.formats
import securesystemslib.hash
import securesystemslib.interface
import securesystemslib.keys
import securesystemslib.exceptions
import securesystemslib.gpg.functions

def import_rsa_key_from_file(filepath, password=None):
  """
  <Purpose>
    Import the RSA key stored in PEM format to 'filepath'. This can be
    a public key or a private key.
    If it is a private key and the password is specified, it will be used
    to decrypt the private key.

  <Arguments>
    filepath:
      <filepath> file, an RSA PEM file

    password: (optional)
      If a password is specified, the imported private key will be decrypted

  <Exceptions>
    securesystemslib.exceptions.FormatError, if the arguments are
    improperly formatted

  <Side Effects>
    'filepath' is read and its contents extracted

  <Returns>
    An RSA key object conformant to 'tuf.formats.RSAKEY_SCHEMA'
  """
  securesystemslib.formats.PATH_SCHEMA.check_match(filepath)

  with open(filepath, "rb") as fo_pem:
    rsa_pem = fo_pem.read().decode("utf-8")

  if securesystemslib.keys.is_pem_private(rsa_pem):
    rsa_key = securesystemslib.keys.import_rsakey_from_private_pem(
        rsa_pem, password=password)

  elif securesystemslib.keys.is_pem_public(rsa_pem):
    rsa_key = securesystemslib.keys.import_rsakey_from_public_pem(rsa_pem)
  else:
    raise securesystemslib.exceptions.FormatError(
        "The key has to be clear either a private or"
        " public RSA key in PEM format")

  return rsa_key


def main():
  ### Read keys
  key_alice = import_rsa_key_from_file("alice")
  key_Dimitris = import_rsa_key_from_file("Dimitris.pub")
  key_Ningrong = import_rsa_key_from_file("Ningrong.pub")
  ### initialize layout dic
  layout_temp = {
    "_type": "layout",
    "keys": {
        key_Dimitris["keyid"]: key_Dimitris,
        key_Ningrong["keyid"]: key_Ningrong,
    },
    "steps": []
  }

  steps_temp = layout_temp["steps"]

  f = open('tasks_commands.json','r')
  commands = json.loads(f.read())
  f.close()

  # print(type(commands))
  # eval("fake_key = key_Ningrong[\"keyid\"]")
  count = 0
  worker_key = key_Dimitris["keyid"]
  print(key_Ningrong["keyid"])
  for worker in commands.keys():
    # comm_name = commands[workers].keys()
    # comm_per_func = commands[workers].values()
    for name, comm in commands[worker].items():
      # a = 'worker_key = key_'+worker+'[\"keyid\"]'
      # print(a)
      # exec(a,globals())
      # print(a)
      
      worker_key = eval('key_'+worker+'[\"keyid\"]')
      print(worker_key)

      comm_dices = comm.split()
      steps_temp.append({
        "name": name,
        "expected_materials": [],
        "expected_products": [],
        # "pubkeys": [key_Dimitris["keyid"]],
        "pubkeys":[worker_key],
        "expected_command":[],
        # "expected_command": [
        #     # comm
        #     "tkn",
        #     "task",
        #     "start",
        #     "clone-python-repo-original"
        # ],
        "threshold": 1,
      })
      # print(steps_temp[0]["expected_command"])
      for dice in comm_dices:
        exec("steps_temp[count][\"expected_command\"].append(dice)")
    count = count+1

  # steps_temp = layout_temp["steps"]
  # steps_temp.append({
  #   "name": "package",
  #   "expected_materials": [],
  #   # "expected_products": [["CREATE", "intro-to-pytest.tar.gz"], ["DISALLOW", "*"]],
  #   "expected_products":[],
  #   "pubkeys": [key_Ningrong["keyid"]],
  #   "expected_command": [
  #     "tar --exclude .git -zcvf intro-to-pytest.tar.gz intro-to-pytest",
  #       # "tar",
  #       # "--exclude",
  #       # ".git",
  #       # "-zcvf",
  #       # "intro-to-pytest.tar.gz",
  #       # "intro-to-pytest",
  #   ],
  #   "threshold": 1,
  # })
  # steps_temp.append({
  #   "name": "clone",
  #   "expected_materials": [],
  #   "expected_products": [],
  #   "pubkeys": [key_Dimitris["keyid"]],
  #   "expected_command": [
  #     "git clone https://github.com/pluralsight/intro-to-pytest.git"
  #       # "git",
  #       # "clone",
  #       # "https://github.com/pluralsight/intro-to-pytest.git"
  #   ],
  #   "threshold": 1,
  # })
  # steps_temp.append({
  #     "name": "pytest",
  #     "expected_materials": [],
  #     "expected_products": [],
  #     "pubkeys": [key_Dimitris["keyid"]],
  #     "expected_command": [
  #       "pytest test/01_basic_test.py"
  #       # "pytest",
  #       # "test/01_basic_test.py"
  #     ],
  #     "threshold": 1,
  #   })

  # ## Test of add extra steps into "steps" in layout_temp
  
  
  layout_temp.update({
    "inspect": [{
      "name": "untar",
      # "expected_materials": [
      #     ["MATCH", "intro-to-pytest.tar.gz", "WITH", "PRODUCTS", "FROM", "package"],
      #     # FIXME: If the routine running inspections would gather the
      #     # materials/products to record from the rules we wouldn't have to
      #     # ALLOW other files that we aren't interested in.
      #     ["ALLOW", ".keep"],
      #     ["ALLOW", "Zhou.pub"],
      #     ["ALLOW", "root.layout"],
      #     # ["DISALLOW", "*"]
      # ],
      "expected_materials": [],
      "expected_products": [],
      "run": [
          "tar",
          "xzf",
          "intro-to-pytest.tar.gz",
      ]
    }],
  })
  layout = Layout.read(layout_temp)

  metadata = Metablock(signed=layout)
  
  # # Sign and dump layout to "root.layout"
  metadata.sign(key_alice)
  metadata.dump("test.layout")

if __name__ == '__main__':
  main()
