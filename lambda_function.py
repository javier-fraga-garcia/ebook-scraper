import os
import hashlib
import logging
from dataclasses import dataclass, asdict, field
from datetime import datetime
from decimal import Decimal

import requests
from bs4 import BeautifulSoup
import boto3

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_hash_value(title: str, author: str) -> str:
    string = f'{title}, {author}'
    return hashlib.sha256(string.encode()).hexdigest()

@dataclass
class Book:
    id: str
    title: str
    author: str
    price: Decimal
    url: str
    date: str = field(default_factory=lambda: datetime.now().strftime('%d/%m/%Y'))

def get_page_content(url: str) -> requests.Response|None:
    logger.info(f'Requesting page {url}...')
    try:
        res = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        })
        if res.status_code == 200:
            return res.content
        else:
            raise Exception(f'Page response code: {res.status_code}')
    except Exception as e:
        logger.error(f'Error: {e}')
        return None

def parse_content(content: str) -> Book:
    logger.info(f'Parsing content...')
    html = BeautifulSoup(content, 'html.parser')
    url = html.select('a.item-link-underlay')[0]['href'].strip() or None
    title = html.select('h3.title.product-field')[0].text.strip().lower()
    author = html.select('div.synopsis-contributors span.synopsis-text')[0].text.strip().lower()
    price = Decimal(html.select('p.product-field.price span.alternate-price-style')[0].text.replace(',', '.').replace('€', '').strip())
    id = get_hash_value(title, author)
    return Book(id, title, author, price, url)


def _get_table():
    table_name = os.environ.get('TABLE_NAME')
    return boto3.resource('dynamodb').Table(table_name)


def write_book(book: Book) -> str:
    table = _get_table()

    response = table.get_item(Key={
        'id': book.id
    })
    if not 'Item' in response:
        try:
            table.put_item(Item=asdict(book))
            return f'The book with id {book.id} has been saved in the database'
        except Exception as e:
            logger.error(f'Error: {e}')
            return 'Something went wrong with the DB'
    else:
        return f'The book with id {book.id} was already in the database'

def lambda_handler(event: any, context: any):
    PAGE = 'https://www.kobo.com/es/es/p/todaslasofertas'
    content = get_page_content(PAGE)
    if content is not None:
        book = parse_content(content)
        message = write_book(book)
    else:
        message = 'No page content has been recovered'
        
    logger.info(message)
    return {
        'message': message
    }