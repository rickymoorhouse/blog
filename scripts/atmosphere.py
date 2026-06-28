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

def parse_post(post_file):
    """ Parse the post file and return a dict with frontmatter and body. """
    with open(post_file, 'r', encoding='utf-8') as f:
        content = f.read()
    # Separate content into frontmatter and body
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter = parts[1].strip()
            body = parts[2].strip()
            # parse frontmatter from yaml into dict
            frontmatter = yaml.safe_load(frontmatter)
            return {'frontmatter': frontmatter, 'body': body}


def build_url(frontmatter):
    """ Build the canonical URL for the post based on the frontmatter.
        The URL is in the format /blog/yyyy/slug, where:
            yyyy is the year from the date in frontmatter,
            slug is the slug from frontmatter or the slugified title. """
    # date in the frontmatter is a date object so extract the year
    year = frontmatter.get('date', datetime.datetime.now()).year

    slug = frontmatter.get('slug', frontmatter.get('title', '').lower().replace(' ', '-'))
    return f'https://rickymoorhouse.uk/blog/{year}/{slug}'


def strip_markdown(text):
    """ Strip markdown formatting from text, 
        leaving the plain text content. """

    text = re.sub(r'#{1,6}\s+', '', text)
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'__(.+?)__', r'\1', text)
    text = re.sub(r'\*(.+?)\*', r'\1', text)
    text = re.sub(r'_(.+?)_', r'\1', text)
    text = re.sub(r'~~(.+?)~~', r'\1', text)
    text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)
    text = re.sub(r'\[(.+?)\]\[.*?\]', r'\1', text)
    text = re.sub(r'\[(.+?)\]\[\]', r'\1', text)
    text = re.sub(r'!\[.*?\]\(.+?\)', '', text)
    text = re.sub(r'`{3}.*?`{3}', '', text, flags=re.DOTALL)
    text = re.sub(r'`(.+?)`', r'\1', text)
    text = re.sub(r'>\s+', '', text)
    text = re.sub(r'^[\s]*[-*+]\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'^[\s]*\d+\.\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'^---+$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\*\*\*+$', '', text, flags=re.MULTILINE)
    return text.strip()


def upload_featured_image(agent, post_path, featured_image):
    """ Upload the featured image to the atmosphere and return the blob reference """
    click.echo(click.style(f'Uploading featured image ({featured_image}) to Atmosphere...', fg='blue'))
    with open(post_path + '/' + featured_image, 'rb') as f:
        blob_response = agent.com.atproto.repo.upload_blob(f)
        blob_ref = blob_response['blob']
        click.echo(click.style(f'Blob uploaded: {blob_ref}', fg='green'))
        return blob_ref


def social_text(post_text):
    """ Generate a short teaser post for social media from the post file. """
    click.echo(click.style('Generating social media text...', fg='blue'))
    llm_url = os.environ.get('LLM_URL', 'http://localhost:8080/api/chat')
    llm_model = os.environ.get('LLM_MODEL', 'unsloth/gemma-4-12b-it-GGUF:Q4_K_M')
    response = requests.post(llm_url, json={
        "model": llm_model,
        "messages": [
            {
                "role": "user",
                "content": """
                Read the attached post and provde me a short teaser post
                for social media that will entice people to read the full post.
                Keep it short and snappy, no more than 2 sentences.
                Do not use hashtags or emojis. My style is personal,
                approachable and friendly. Retain the tone of the post.
                Avoid using the words 'learn', 'click here' or 'read more'.
                I do not want this to sound like marketing copy, but rather
                a personal recommendation. Only return a single option.
                \n---\n""" + post_text
            }
        ]
    }, timeout=120)
    try:
        return response.json()['choices'][0]['message']['content'].strip()
    except (KeyError, IndexError):
        click.echo(click.style('Error generating social media text.' + response.text, fg='red'))
        return ''

@click.command()
@click.option('--post', help='md file for post.')
@click.option('--bluesky', is_flag=True, help='Post to Bluesky.')
@click.option('--use_commit', is_flag=True, help='Use previous commit.')
def main(post, bluesky, use_commit):
    """ Main function to post to atmosphere and optionally to Bluesky. """

    if not post:
        if use_commit:
            command = ['git','show','--name-only','--pretty=format:','HEAD']
        else:
            command = ['git', 'diff', '--cached', '--name-only']

        # No post specified - check the staged files in git and find the first .md file
        files = subprocess.run(
            command,
            capture_output=True, text=True, check=True
        ).stdout.splitlines()

        for filepath in files:
            if filepath.endswith('.md'):
                post = filepath
                break
        # If there's no file found then exit
        if not filepath:
            exit("No file specified or identified")

    agent = Client()

    # load credential from env variables
    password = os.environ.get('ATPROTO_APP_PASSWORD')
    handle = os.environ.get('ATPROTO_APP_HANDLE')
    agent.login(handle, password)

    post_data = parse_post(post)

    # text content should be the same as content, but without any markdown formatting
    text_content = strip_markdown(post_data['body'])
    post_url = build_url(post_data['frontmatter'])

    # TODO: If posting to bluesky, do this and get the did for the post
    if bluesky:
        social = social_text(text_content)
        click.echo(click.style('Suggested bluesky post:', fg='blue'))
        click.echo(click.style("\t" + social + " " + post_url, fg='green'))

    date = post_data['frontmatter'].get('date')
    if not isinstance(date, datetime.datetime):
        if date is None:
            date = datetime.datetime.now()
        elif isinstance(date, datetime.date):
            date = datetime.datetime.combine(date, datetime.time.min)    
    document_record = {
        '$type': 'site.standard.document',
        'site': BLOG_DID,
        'path': post_url.replace("https://rickymoorhouse.uk",""),
        'title': post_data['frontmatter'].get('title', 'Untitled'),
        'publishedAt': date.isoformat(),
        'textContent': text_content,
        'canonicalUrl': post_url,
        'contributor': {   
            'did': agent.me.did,
            'role': 'author',
            'displayName': "Ricky Moorhouse",
        }
    }
    # If there is a featured image, upload as blob and get the reference
    if 'featured' in post_data['frontmatter']:
        featured_image = post_data['frontmatter']['featured']

        # get relative path to the post file, removing the file name
        post_path = post.rsplit('/', 1)[0]
        print('Featured image:', featured_image)

        # Upload to atmosphere and get the blob reference
        blob_ref = upload_featured_image(agent, post_path, featured_image)
        document_record['cover'] = blob_ref

    if 'summary' in post_data['frontmatter']:
        document_record['description'] = post_data['frontmatter']['summary']

    if 'tags' in post_data['frontmatter']:
        document_record['tags'] = post_data['frontmatter']['tags']
    # if there is already an atUri in the frontmatter, we can update
    if 'atUri' in post_data['frontmatter']:
        at_uri = post_data['frontmatter']['atUri']
        click.echo(click.style(f'Updating existing post: {at_uri}', fg='blue'))
        try:
            response = agent.com.atproto.repo.put_record({
                'repo': agent.me.did,
                'did': post_data['frontmatter']['atUri'],
                'collection': 'site.standard.document',
                'rkey': post_data['frontmatter']['atUri'].split('/')[-1],
                'record': document_record,
            })
            click.echo(click.style('Document record updated!', fg='green'))

        except Exception as error:
            print('Failed to update document:', error)
    else:
        try:
            response = agent.com.atproto.repo.create_record({
                'repo': agent.me.did,
                'collection': 'site.standard.document',
                'record': document_record,
            })
            click.echo(click.style('Document record created!', fg='green'))
            click.echo(click.style(f'Your AT-URI is: {response.uri}', fg='green'))

            # inject the new atUri into the frontmatter of the post file
            with open(post, 'r', encoding='utf-8') as f:
                content = f.read()

            # replace the frontmatter with the new frontmatter that includes the atUri
            new_frontmatter = post_data['frontmatter']
            new_frontmatter['atUri'] = response.uri
            new_content = '---\n' + yaml.dump(new_frontmatter) + '---\n' + post_data['body']
            with open(post, 'w', encoding='utf-8') as f:
                f.write(new_content)

        except Exception as error:
            print('Failed to create document:', error)


if __name__ == '__main__':
    main()
