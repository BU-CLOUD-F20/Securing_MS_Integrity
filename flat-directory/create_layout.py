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

  steps_temp = layout_temp["steps"]

  f = open('tasks_commands.json','r')
  commands = json.loads(f.read())
  f.close()

  # print(type(commands))
  functionaries = commands.keys()
  # eval("fake_key = key_Ningrong[\"keyid\"]")
  for workers in functionaries:
    # comm_name = commands[workers].keys()
    # comm_per_func = commands[workers].values()
    for name, comm in commands[workers].items():
      worker_key = ""
      exec("worker_key = key_"+workers+"[\"keyid\"]")
      steps_temp.append({
        "name": name,
        "expected_materials": [],
        "expected_products": [],
        # "pubkeys": [key_Dimitris["keyid"]],
        "pubkeys":[worker_key],
        "expected_command": [
            # "git",
            # "clone",
            # "https://github.com/pluralsight/intro-to-pytest.git"
            comm
        ],
        "threshold": 1,
      })

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

  ### Test of add extra steps into "steps" in layout_temp
  
  
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

