import requests

def rembg(body_path,nobg_path):
    response = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        files={'image_file': open(body_path, 'rb')},
        data={'size': 'auto'},
        headers={'X-Api-Key': '2Vp5jqzVGViJDdYdaLN6Mwfs'},
    )
    if response.status_code == requests.codes.ok:
        with open(nobg_path, 'wb') as out:
            out.write(response.content)
    else:
        print("Error:", response.status_code, response.text)