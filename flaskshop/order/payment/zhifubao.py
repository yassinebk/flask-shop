from alipay import AliPay
from flask import url_for

with open("./flaskshop/order/payment/app_private_key.pem") as f:
    app_private_key_string = f.read()

with open("./flaskshop/order/payment/ali_public_key.pem") as f:
    alipay_public_key_string = f.read()

pay_obj = AliPay(
    appid=2016080400161922,
    app_notify_url=None,  # 默认回调url
    app_private_key_string=app_private_key_string,
    alipay_public_key_string=alipay_public_key_string,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
    sign_type="RSA2",  # RSA 或者 RSA2
    debug=True  # 默认False
)


def send_order(no, payment_no, total_amount):
    subject = "订单" + no
    # 电脑网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
    order_string = pay_obj.api_alipay_trade_page_pay(
        out_trade_no=payment_no,
        total_amount=str(total_amount),
        subject=subject,
        return_url='http://127.0.0.1:5000/orders/',
        notify_url='http://a5d267a6.ngrok.io/orders/alipay/notify'
    )
    return order_string


def verify_order(data, signature):
    success = pay_obj.verify(data, signature)
    if success and data["trade_status"] in ("TRADE_SUCCESS", "TRADE_FINISHED"):
        return True
    return False