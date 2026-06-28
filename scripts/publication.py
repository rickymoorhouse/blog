import datetime
import os
import re
import subprocess

from atproto import Client
import click
import yaml
import requests

# Publication record
BLOG_DID = 'at://did:plc:r53zv4vpzeihop3aliwyejlu/site.standard.publication/3mos5q3a7jf2w'


def upload_image(agent, image_path):
    """ Upload the featured image to the atmosphere and return the blob reference """
    click.echo(click.style(f'Uploading featured image ({image_path}) to Atmosphere...', fg='blue'))
    with open(image_path, 'rb') as f:
        blob_response = agent.com.atproto.repo.upload_blob(f)
        blob_ref = blob_response['blob']
        click.echo(click.style(f'Blob uploaded: {blob_ref}', fg='green'))
        return blob_ref



@click.command()
def main():
    """ Main function to update publication. """

    agent = Client()

    # load credential from env variables
    password = os.environ.get('ATPROTO_APP_PASSWORD')
    handle = os.environ.get('ATPROTO_APP_HANDLE')
    agent.login(handle, password)

    publication_record = {
        "url": "https://rickymoorhouse.uk",
        "name": "Ricky Moorhouse",
        "$type": "site.standard.publication",
        "createdAt": "2026-06-21T10:23:50.966Z",
        "basicTheme": {
            "$type": "site.standard.theme.basic",
            "accent": {
            "b": 102,
            "g": 153,
            "r": 0,
            "$type": "site.standard.theme.color#rgb"
            },
            "background": {
            "b": 255,
            "g": 255,
            "r": 255,
            "$type": "site.standard.theme.color#rgb"
            },
            "foreground": {
            "b": 34,
            "g": 34,
            "r": 34,
            "$type": "site.standard.theme.color#rgb"
            },
            "accentForeground": {
            "b": 255,
            "g": 255,
            "r": 255,
            "$type": "site.standard.theme.color#rgb"
            }
        },
        "description": "Ricky's personal corner of the web - photos, APIs, travel and tech",
        "preferences": {
            "showInDiscover": True
        }
    }

    # Upload to atmosphere and get the blob reference
    blob_ref = upload_image(agent, '/Users/rickymoorhouse/blog/themes/2026/static/apple-touch-icon.png')
    publication_record['icon'] = blob_ref

    # if there is already an atUri in the frontmatter, we can update
    click.echo(click.style(f'Updating existing post: {BLOG_DID}', fg='blue'))
    try:
        response = agent.com.atproto.repo.put_record({
            'repo': agent.me.did,
            'did': BLOG_DID,
            'collection': 'site.standard.publication',
            'rkey': BLOG_DID.split('/')[-1],
            'record': publication_record,
        })
        click.echo(click.style('Publication record updated!', fg='green'))

    except Exception as error:
        print('Failed to update document:', error)

if __name__ == '__main__':
    main()
