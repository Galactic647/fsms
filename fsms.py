import requests
import re

url = r'https://alpha.payuterus.biz/index.php?a=keluar'
valid_number = re.compile(r'^((0|62)8[0-9]{10,11})$')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0',
    'Referer': 'https://alpha.payuterus.biz/send.php'
}


def message(phone_number: str, msg: str) -> None:
    with requests.Session() as session:
        s = session.get(url)
        text = s.text

        captcha = eval(re.findall(r'<span>(.+?) = </span>', text)[0])
        key = re.findall(r'value="(\d+?)"', text)[0]

        data = {
            'nohp': phone_number,
            'pesan': msg,
            'captcha': captcha,
            'key': key
        }

        response = session.post(r'https://alpha.payuterus.biz/send.php', headers=headers, data=data).text
        if 'Telah Dikirim' in response:
            print(f"Send Successful -> {phone_number}")
        elif 'MAAF...' in response:
            print("Please wait for 30 minutes for the next message")
        else:
            print("Failed to send")

        session.close()


def main():
    print('Message should be in range of 15-122 characters')
    pn = input('Phone number: ')
    msg = input('Message: ')

    if valid_number.match(pn) is None:
        print('Incorrect Phone Number Pattern')
    elif 15 > len(msg):
        print('Message should have at least 15 characters')
    elif len(msg) > 122:
        print('Message should have a maximum of 122 characters')
    else:
        message(pn, msg)


if __name__ == '__main__':
    main()
