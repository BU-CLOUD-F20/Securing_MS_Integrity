from in_toto.util import import_rsa_key_from_file
from in_toto.models.layout import Layout
from in_toto.models.metadata import Metablock

def main():
  # Load Alice's private key to later sign the layout
  key_alice = import_rsa_key_from_file("alice")
  # Fetch and load Bob's and Carl's public keys
  # to specify that they are authorized to perform certain step in the layout
  key_bob = import_rsa_key_from_file("../Ningrong/carl.pub")
  key_carl = import_rsa_key_from_file("../Dimitris/bob.pub")

  layout = Layout.read({
      "_type": "layout",
      "keys": {
          key_bob["keyid"]: key_bob,
          key_carl["keyid"]: key_carl,
      },
      "steps": [{
          "name": "clone",
          "expected_materials": [],
          "expected_products": [["CREATE", "intro-to-pytest/"], ["DISALLOW", "*"]],
          "pubkeys": [key_bob["keyid"]],
          "expected_command": [
              "git",
              "clone",
              "https://github.com/pluralsight/intro-to-pytest.git"
          ],
          "threshold": 1,
        },{
          "name": "pytest",
          "expected_materials": [["MATCH", "intro-to-pytest/*", "WITH", "PRODUCTS",
                                "FROM", "clone"], ["DISALLOW", "*"]],
          "expected_products": [],
          "pubkeys": [key_bob["keyid"]],
          "expected_command": [
            "pytest",
            "intro-to-pytest/tests/01_basic_test.py"
          ],
          "threshold": 1,
        },
        ],
      "inspect": [],
  })

  metadata = Metablock(signed=layout)

  # Sign and dump layout to "root.layout"
  metadata.sign(key_alice)
  metadata.dump("root.layout")

if __name__ == '__main__':
  main()
