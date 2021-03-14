from flask import request

def get_patients():

    address = request.args.get("address")
    print(address)

    return "test"
