import load_django
from parser_app.models import ItemLink
from storiaro_parser_main import StoriaroParser



URL = 'https://www.storia.ro/ro/rezultate/vanzare/apartament/toata-romania?market=ALL&viewType=listing&limit=72&page=1'


def main():
    parser = StoriaroParser()

    with parser.driver as driver:
        driver.get(url=URL)
        # sleep(2)
        # pagen = parser.get_pagen()
        pagen = 2
        if pagen:
            for i in range(1, pagen + 1):
                url = f'https://www.storia.ro/ro/rezultate/vanzare/apartament/toata-romania?market=ALL&viewType=listing&limit=72&page={i}'
                parser.collect_links(url=url)


if __name__ == '__main__':
    main()




