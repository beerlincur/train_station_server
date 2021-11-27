import bcrypt

print(bcrypt.hashpw('ruya_parod'.encode(), bcrypt.gensalt()))