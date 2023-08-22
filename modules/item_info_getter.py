import load_django
from parser_app.models import ItemInfo, ItemLink
from storiaro_parser_main import StoriaroParser
from time import sleep


URL = 'https://www.storia.ro/ro/rezultate/vanzare/apartament/toata-romania?market=ALL&viewType=listing&limit=72&page=1'



def main():
    parser = StoriaroParser()

    with parser.driver as driver:
        for item in ItemLink.objects.filter(status=False):
            try:
                parser.get_item_info(item)
                item.status = True
                item.save()
            except IndexError:
                item.delete()
                continue
            sleep(3)

if __name__ == '__main__':
    main()




