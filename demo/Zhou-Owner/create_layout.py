from in_toto.util import import_rsa_key_from_file
from in_toto.models.layout import Layout
from in_toto.models.metadata import Metablock

def main():
  # Load Alice's private key to later sign the layout
  key_alice = import_rsa_key_from_file("alice")
  # Fetch and load Bob's and Carl's public keys
  # to specify that they are authorized to perform certain step in the layout
  key_Dimitris = import_rsa_key_from_file("../Dimitris-clone&pytest/Dimitris.pub")
  key_Ningrong = import_rsa_key_from_file("../Ningrong-package/Ningrong.pub")

  layout = Layout.read({
      "_type": "layout",
      "keys": {
          key_Dimitris["keyid"]: key_Dimitris,
          key_Ningrong["keyid"]: key_Ningrong,
      },
      "steps": [{
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
        },
        # {
        #   "name": "update-version",
        #   "expected_materials": [["MATCH", "demo-project/*", "WITH", "PRODUCTS",
        #                         "FROM", "clone"], ["DISALLOW", "*"]],
        #   "expected_products": [["ALLOW", "demo-project/foo.py"], ["DISALLOW", "*"]],
        #   "pubkeys": [key_bob["keyid"]],
        #   "expected_command": [],
        #   "threshold": 1,
        # },
        {
          "name": "pytest",
          "expected_materials": [],
          "expected_products": [],
          "pubkeys": [key_Dimitris["keyid"]],
          "expected_command": [
            "pytest",
            "test/01_basic_test.py"
          ],
          "threshold": 1,
        },{
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
        }],
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

  metadata = Metablock(signed=layout)

  # Sign and dump layout to "root.layout"
  metadata.sign(key_alice)
  metadata.dump("root.layout")

if __name__ == '__main__':
  main()
