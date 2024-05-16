import hmac
import hashlib
import os


def check(request):
    x_kushki_simplesignature = request.headers["x-kushki-simplesignature"]
    x_kushki_id = request.headers["x-kushki-id"]
    webhook_signature = os.getenv('WEBHOOK_SIGNATURE')  # 20000000105986396000
    generated_signature = hmac.new(bytes(webhook_signature, 'utf-8'),
                                   msg=bytes(x_kushki_id, 'utf-8'),
                                   digestmod=hashlib.sha256).hexdigest()
    if x_kushki_simplesignature == generated_signature:
        return True
    else:
        return False
