import hashlib

def EncryptPassword(password):
    salted = "%s%s%s" % ("asdpio78v&Dg76fb", password, "iousihfg87V#^$b7v691")
    return hashlib.sha256(password).hexdigest()

