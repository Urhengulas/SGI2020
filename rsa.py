import json
import logging

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa

# set up logger
logging.basicConfig(
    format="%(asctime)s.%(msecs)03d - %(module)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# load keys
with open("id_rsa.pub", "rb") as f:
    public_key = serialization.load_pem_public_key(
        f.read(),
        backend=default_backend()
    )
with open("id_rsa", "rb") as f:
    private_key = serialization.load_pem_private_key(
        f.read(),
        password=None,
        backend=default_backend(),
    )
logger.info(f"public_key={public_key}")
logger.info(f"private_key={private_key}")

algorithm = hashes.SHA256()
padding = padding.PSS(
    mgf=padding.MGF1(algorithm),
    salt_length=padding.PSS.MAX_LENGTH
)


def sign_data(data: dict) -> dict:
    data["signature"] = private_key.sign(
        data=json.dumps(data["payload"]).encode("utf-8"),
        padding=padding,
        algorithm=algorithm,
    )
    return data


def verify_data(data: dict) -> bool:
    try:
        public_key.verify(
            signature=data["signature"],
            data=json.dumps(data["payload"]).encode("utf-8"),
            padding=padding,
            algorithm=algorithm,
        )
    except InvalidSignature:
        return False
    else:
        return True


if __name__ == "__main__":
    data = {
        "payload": {
            "material": "wood",
            "OEM": "Beckhoff",
        },
        # signature: added later
    }

    # sign data
    signed_data = sign_data(data)
    logger.info(f"signed_data={signed_data}")

    # tests
    print("Tests:")
    print("# test 1 - ", end="")
    print("passed") if verify_data(signed_data) == True else print("failed")
    print("# test 2 - ", end="")
    # change data
    changed_data = signed_data.copy()
    changed_data["payload"]["corrupted"] = True
    print("passed") if verify_data(changed_data) == False else print("failed")
