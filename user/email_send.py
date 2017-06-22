from random import Random
import string

from django.core.mail import send_mail
from .models import EmailVerifyRecord

from myblog.settings import EMAIL_FROM


def send_register_email(email, send_type='register'):
    email_record = EmailVerifyRecord()
    code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    if send_type == 'register':
        email_title = '何佳豪个人站点激活链接'
        email_body = '请点击下面的链接激活你的账号：http://www.hjhgo.cn/active/{0}'.format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            # TODO
            print('发送成功')

    elif send_type == 'forget':
        email_title = '何佳豪个人站点密码重置链接'
        email_body = '请点击下面的链接重置你的密码：http://www.hjhgo.cn/reset/{0}'.format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            # TODO 提示发送成功
            pass


def random_str(random_length=16):
    code = ''
    # 26个大小写字母加数字
    chars = string.ascii_letters + str(string.digits)
    length = len(chars) - 1

    for i in range(random_length):
        code += chars[Random().randint(0, length)]
    return code