#!env python3
from exif import Image
import click


@click.command()
@click.argument('filename')
@click.argument('description')
def set_description(filename, description):
    with open(filename, 'rb') as img:
      imgobj = Image(img)

    print(imgobj.list_all())
    imgobj.image_description = description
    print(imgobj.list_all())
    with open(filename, 'wb') as writeimg:
      writeimg.write(imgobj.get_file())

if __name__ == "__main__":
    set_description()
