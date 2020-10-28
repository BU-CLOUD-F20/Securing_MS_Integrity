from in_toto.util import import_rsa_key_from_file
from in_toto.models.layout import Layout
from in_toto.models.metadata import Metablock
import json

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
  
  # f = open('tasks_commands.json','r')
  # commands = json.loads(f.read())
  # f.close()

  steps_temp = layout_temp["steps"]
  steps_temp.append({
    "name": "clone",
    "expected_materials": [],
    "expected_products": [],
    "pubkeys": [key_Dimitris["keyid"]],
    "expected_command": [
        "git",
        "clone",
        "https://github.com/pluralsight/intro-to-pytest.git"
    ],
    "threshold": 1,
  })
  steps_temp.append({
      "name": "pytest",
      "expected_materials": [],
      "expected_products": [],
      "pubkeys": [key_Dimitris["keyid"]],
      "expected_command": [
        "pytest",
        "test/01_basic_test.py"
      ],
      "threshold": 1,
    })
  # intoto 

  ### Test of add extra steps into "steps" in layout_temp
  
  steps_temp.append({
    "name": "package",
    "expected_materials": [],
    "expected_products": [["CREATE", "intro-to-pytest.tar.gz"], ["DISALLOW", "*"]],
    "pubkeys": [key_Ningrong["keyid"]],
    "expected_command": [
        "tar",
        "--exclude",
        ".git",
        "-zcvf",
        "intro-to-pytest.tar.gz",
        "intro-to-pytest",
    ],
    "threshold": 1,
  })
  layout_temp.update({
    "inspect": [{
      "name": "untar",
      "expected_materials": [
          ["MATCH", "intro-to-pytest.tar.gz", "WITH", "PRODUCTS", "FROM", "package"],
          # FIXME: If the routine running inspections would gather the
          # materials/products to record from the rules we wouldn't have to
          # ALLOW other files that we aren't interested in.
          ["ALLOW", ".keep"],
          ["ALLOW", "Zhou.pub"],
          ["ALLOW", "root.layout"],
          # ["DISALLOW", "*"]
      ],
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
  
  # Sign and dump layout to "root.layout"
  metadata.sign(key_alice)
  metadata.dump("root.layout")

if __name__ == '__main__':
  main()
