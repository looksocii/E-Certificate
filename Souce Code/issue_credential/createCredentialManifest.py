from createCredential import Credential
from createManifest import Manifest, AggregateCredential

def create():
   credential = Credential()
   credential.create()
   print("\ncreate credential success!")

   manifest = Manifest()
   manifest.create()

   aggregateCredential = AggregateCredential()
   aggregateCredential.addProof2manifest()

if __name__ == '__main__':
    create()