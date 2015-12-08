#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from pyquery import PyQuery as pq
import urllib2 
import json

from oxygendemo.items import OxygendemoItem


class OxygenSpider(CrawlSpider):
    name = "oxygenboutique.com"
    allowed_domains = ["oxygenboutique.com"]
    start_urls = [
        'http://www.oxygenboutique.com/clothing.aspx?ViewAll=1',
        'http://www.oxygenboutique.com/Shoes-All.aspx?ViewAll=1',
        'http://www.oxygenboutique.com/accessories-all.aspx?ViewAll=1',
        'http://www.oxygenboutique.com/Sale-In.aspx?ViewAll=1'
     ]
    rules = [
        Rule(LxmlLinkExtractor(
            restrict_css='div.itm a:first-child'),
            callback='parse_item'
            )
    ]

    def __init__(self, *args, **kwargs):
        super(OxygenSpider, self).__init__(*args, **kwargs)
        self.usd_exchange_rate = self.get_usd_exchange_rate()
        self.eur_exchange_rate = self.get_eur_exchange_rate()
        """
        Defining some keywords for guessing the types of items
        These keywords can be more optimized
        Colors were crawled from colorhexa.com/color-names
        I can send the crawler code if necessary
        """
        self.apparel = {
            "jean", "bodysuit", "blazer", "bra", "coat", "shortsuit", 
            "blouse", "jacket", "romper", "sleeve", "suit", "dress", 
            "tunic", "tank", "shirt", "minidress", "frilltop", "trouser", 
            "corset", "sweater", "bikini", "frilltop", "hoody", "jumpsuit", 
            "sweatshirt", "scarf", "pant", "skirt", "top", "shorts", "lingerie"
            }
        self.shoes = {
            'heel', 'boot', 'sneaker', 'sandal', 'flat', 'wedge'
            }
        self.bags = {
            'briefcase', 'bag', 'purse', 'backpack' 
            }
        self.jewelry = {
            'necklace', 'bracelet', 'ring', 'earring'
            }
        self.accessories = {
            'tatoo', 'case', 'box', 'scent', 'hat', 'iphone case'
            }
        self.colors = {
            "air force blue", "alice blue", "alizarin crimson", "almond",
            "amaranth", "amber", "american rose", "amethyst",
            "android green", "anti-flash white", "antique brass", "antique fuchsia",
            "antique white", "ao", "apple green", "apricot",
            "aqua", "aquamarine", "army green", "arylide yellow",
            "ash grey", "asparagus", "atomic tangerine", "auburn",
            "aureolin", "aurometalsaurus", "awesome", "azure",
            "azure mist/web", "baby blue", "baby blue eyes", "baby pink",
            "ball blue", "banana mania", "banana yellow", "battleship grey",
            "bazaar", "beau blue", "beaver", "beige",
            "bisque", "bistre", "bittersweet", "black",
            "blanched almond", "bleu de france", "blizzard blue", "blond",
            "blue", "blue bell", "blue gray", "blue green",
            "blue purple", "blue violet", "blush", "bole",
            "bondi blue", "bone", "boston university red", "bottle green",
            "boysenberry", "brandeis blue", "brass", "brick red",
            "bright cerulean", "bright green", "bright lavender", "bright maroon",
            "bright pink", "bright turquoise", "bright ube", "brilliant lavender",
            "brilliant rose", "brink pink", "british racing green", "bronze",
            "brown", "bubble gum", "bubbles", "buff",
            "bulgarian rose", "burgundy", "burlywood", "burnt orange",
            "burnt sienna", "burnt umber", "byzantine", "byzantium",
            "cg blue", "cg red", "cadet", "cadet blue",
            "cadet grey", "cadmium green", "cadmium orange", "cadmium red",
            "cadmium yellow", "café au lait", "café noir", "cal poly pomona green",
            "cambridge blue", "camel", "camouflage green", "canary",
            "canary yellow", "candy apple red", "candy pink", "capri",
            "caput mortuum", "cardinal", "caribbean green", "carmine",
            "carmine pink", "carmine red", "carnation pink", "carnelian",
            "carolina blue", "carrot orange", "celadon", "celeste",
            "celestial blue", "cerise", "cerise pink", "cerulean",
            "cerulean blue", "chamoisee", "champagne", "charcoal",
            "chartreuse", "cherry", "cherry blossom pink", "chestnut",
            "chocolate", "chrome yellow", "cinereous", "cinnabar",
            "cinnamon", "citrine", "classic rose", "cobalt",
            "cocoa brown", "coffee", "columbia blue", "cool black",
            "cool grey", "copper", "copper rose", "coquelicot",
            "coral", "coral pink", "coral red", "cordovan",
            "corn", "cornell red", "cornflower", "cornflower blue",
            "cornsilk", "cosmic latte", "cotton candy", "cream",
            "crimson", "crimson red", "crimson glory", "cyan",
            "daffodil", "dandelion", "dark blue", "dark brown",
            "dark byzantium", "dark candy apple red", "dark cerulean", "dark chestnut",
            "dark coral", "dark cyan", "dark electric blue", "dark goldenrod",
            "dark gray", "dark green", "dark jungle green", "dark khaki",
            "dark lava", "dark lavender", "dark magenta", "dark midnight blue",
            "dark olive green", "dark orange", "dark orchid", "dark pastel blue",
            "dark pastel green", "dark pastel purple", "dark pastel red", "dark pink",
            "dark powder blue", "dark raspberry", "dark red", "dark salmon",
            "dark scarlet", "dark sea green", "dark sienna", "dark slate blue",
            "dark slate gray", "dark spring green", "dark tan", "dark tangerine",
            "dark taupe", "dark terra cotta", "dark turquoise", "dark violet",
            "dartmouth green", "davy grey", "debian red", "deep carmine",
            "deep carmine pink", "deep carrot orange", "deep cerise", "deep champagne",
            "deep chestnut", "deep coffee", "deep fuchsia", "deep jungle green",
            "deep lilac", "deep magenta", "deep peach", "deep pink",
            "deep saffron", "deep sky blue", "denim", "desert",
            "desert sand", "dim gray", "dodger blue", "dogwood rose",
            "dollar bill", "drab", "duke blue", "earth yellow",
            "ecru", "eggplant", "eggshell", "egyptian blue",
            "electric blue", "electric crimson", "electric cyan", "electric green",
            "electric indigo", "electric lavender", "electric lime", "electric purple",
            "electric ultramarine", "electric violet", "electric yellow", "emerald",
            "eton blue", "fallow", "falu red", "famous",
            "fandango", "fashion fuchsia", "fawn", "feldgrau",
            "fern", "fern green", "ferrari red", "field drab",
            "fire engine red", "firebrick", "flame", "flamingo pink",
            "flavescent", "flax", "floral white", "fluorescent orange",
            "fluorescent pink", "fluorescent yellow", "folly", "forest green",
            "french beige", "french blue", "french lilac", "french rose",
            "fuchsia", "fuchsia pink", "fulvous", "fuzzy wuzzy",
            "gainsboro", "gamboge", "ghost white", "ginger",
            "glaucous", "glitter", "gold", "golden brown",
            "golden poppy", "golden yellow", "goldenrod", "granny smith apple",
            "gray", "gray asparagus", "green", "green blue",
            "green yellow", "grullo", "guppie green", "halayà úbe",
            "han blue", "han purple", "hansa yellow", "harlequin",
            "harvard crimson", "harvest gold", "heart gold", "heliotrope",
            "hollywood cerise", "honeydew", "hooker green", "hot magenta",
            "hot pink", "hunter green", "icterine", "inchworm",
            "india green", "indian red", "indian yellow", "indigo",
            "international klein blue", "international orange", "iris", "isabelline",
            "islamic green", "ivory", "jade", "jasmine",
            "jasper", "jazzberry jam", "jonquil", "june bud",
            "jungle green", "ku crimson", "kelly green", "khaki",
            "la salle green", "languid lavender", "lapis lazuli", "laser lemon",
            "laurel green", "lava", "lavender", "lavender blue",
            "lavender blush", "lavender gray", "lavender indigo", "lavender magenta",
            "lavender mist", "lavender pink", "lavender purple", "lavender rose",
            "lawn green", "lemon", "lemon yellow", "lemon chiffon",
            "lemon lime", "light crimson", "light thulian pink", "light apricot",
            "light blue", "light brown", "light carmine pink", "light coral",
            "light cornflower blue", "light cyan", "light fuchsia pink", "light goldenrod yellow",
            "light gray", "light green", "light khaki", "light pastel purple",
            "light pink", "light salmon", "light salmon pink", "light sea green",
            "light sky blue", "light slate gray", "light taupe", "light yellow",
            "lilac", "lime", "lime green", "lincoln green",
            "linen", "lion", "liver", "lust",
            "msu green", "macaroni and cheese", "magenta", "magic mint",
            "magnolia", "mahogany", "maize", "majorelle blue",
            "malachite", "manatee", "mango tango", "mantis",
            "maroon", "mauve", "mauve taupe", "mauvelous",
            "maya blue", "meat brown", "medium persian blue", "medium aquamarine",
            "medium blue", "medium candy apple red", "medium carmine", "medium champagne",
            "medium electric blue", "medium jungle green", "medium lavender magenta", "medium orchid",
            "medium purple", "medium red violet", "medium sea green", "medium slate blue",
            "medium spring bud", "medium spring green", "medium taupe", "medium teal blue",
            "medium turquoise", "medium violet red", "melon", "midnight blue",
            "midnight green", "mikado yellow", "mint", "mint cream",
            "mint green", "misty rose", "moccasin", "mode beige",
            "moonstone blue", "mordant red 19", "moss green", "mountain meadow",
            "mountbatten pink", "mulberry", "munsell", "mustard",
            "myrtle", "nadeshiko pink", "napier green", "naples yellow",
            "navajo white", "navy blue", "neon carrot", "neon fuchsia",
            "neon green", "non-photo blue", "north texas green", "ocean boat blue",
            "ochre", "office green", "old gold", "old lace",
            "old lavender", "old mauve", "old rose", "olive",
            "olive drab", "olive green", "olivine", "onyx",
            "opera mauve", "orange", "orange yellow", "orange peel",
            "orange red", "orchid", "otter brown", "outer space",
            "outrageous orange", "oxford blue", "pacific blue", "pakistan green",
            "palatinate blue", "palatinate purple", "pale aqua", "pale blue",
            "pale brown", "pale carmine", "pale cerulean", "pale chestnut",
            "pale copper", "pale cornflower blue", "pale gold", "pale goldenrod",
            "pale green", "pale lavender", "pale magenta", "pale pink",
            "pale plum", "pale red violet", "pale robin egg blue", "pale silver",
            "pale spring bud", "pale taupe", "pale violet red", "pansy purple",
            "papaya whip", "paris green", "pastel blue", "pastel brown",
            "pastel gray", "pastel green", "pastel magenta", "pastel orange",
            "pastel pink", "pastel purple", "pastel red", "pastel violet",
            "pastel yellow", "patriarch", "payne grey", "peach",
            "peach puff", "peach yellow", "pear", "pearl",
            "pearl aqua", "peridot", "periwinkle", "persian blue",
            "persian indigo", "persian orange", "persian pink", "persian plum",
            "persian red", "persian rose", "phlox", "phthalo blue",
            "phthalo green", "piggy pink", "pine green", "pink",
            "pink flamingo", "pink sherbet", "pink pearl", "pistachio",
            "platinum", "plum", "portland orange", "powder blue",
            "princeton orange", "prussian blue", "psychedelic purple", "puce",
            "pumpkin", "purple", "purple heart", "purple mountain's majesty",
            "purple mountain majesty", "purple pizzazz", "purple taupe", "rackley",
            "radical red", "raspberry", "raspberry glace", "raspberry pink",
            "raspberry rose", "raw sienna", "razzle dazzle rose", "razzmatazz",
            "red", "red orange", "red brown", "red violet",
            "rich black", "rich carmine", "rich electric blue", "rich lilac",
            "rich maroon", "rifle green", "robin's egg blue", "rose",
            "rose bonbon", "rose ebony", "rose gold", "rose madder",
            "rose pink", "rose quartz", "rose taupe", "rose vale",
            "rosewood", "rosso corsa", "rosy brown", "royal azure",
            "royal blue", "royal fuchsia", "royal purple", "ruby",
            "ruddy", "ruddy brown", "ruddy pink", "rufous",
            "russet", "rust", "sacramento state green", "saddle brown",
            "safety orange", "saffron", "saint patrick blue", "salmon",
            "salmon pink", "sand", "sand dune", "sandstorm",
            "sandy brown", "sandy taupe", "sap green", "sapphire",
            "satin sheen gold", "scarlet", "school bus yellow", "screamin green",
            "sea blue", "sea green", "seal brown", "seashell",
            "selective yellow", "sepia", "shadow", "shamrock",
            "shamrock green", "shocking pink", "sienna", "silver",
            "sinopia", "skobeloff", "sky blue", "sky magenta",
            "slate blue", "slate gray", "smalt", "smokey topaz",
            "smoky black", "snow", "spiro disco ball", "spring bud",
            "spring green", "steel blue", "stil de grain yellow", "stizza",
            "stormcloud", "straw", "sunglow", "sunset",
            "sunset orange", "tan", "tangelo", "tangerine",
            "tangerine yellow", "taupe", "taupe gray", "tawny",
            "tea green", "tea rose", "teal", "teal blue",
            "teal green", "terra cotta", "thistle", "thulian pink",
            "tickle me pink", "tiffany blue", "tiger eye", "timberwolf",
            "titanium yellow", "tomato", "toolbox", "topaz",
            "tractor red", "trolley grey", "tropical rain forest", "true blue",
            "tufts blue", "tumbleweed", "turkish rose", "turquoise",
            "turquoise blue", "turquoise green", "tuscan red", "twilight lavender",
            "tyrian purple", "ua blue", "ua red", "ucla blue",
            "ucla gold", "ufo green", "up forest green", "up maroon",
            "usc cardinal", "usc gold", "ube", "ultra pink",
            "ultramarine", "ultramarine blue", "umber", "united nations blue",
            "university of california gold", "unmellow yellow", "upsdell red", "urobilin",
            "utah crimson", "vanilla", "vegas gold", "venetian red",
            "verdigris", "vermilion", "veronica", "violet",
            "violet blue", "violet red", "viridian", "vivid auburn",
            "vivid burgundy", "vivid cerise", "vivid tangerine", "vivid violet",
            "warm black", "waterspout", "wenge", "wheat",
            "white", "white smoke", "wild strawberry", "wild watermelon",
            "wild blue yonder", "wine", "wisteria", "xanadu",
            "yale blue", "yellow", "yellow orange", "yellow green",
            "zaffre", "zinnwaldite brown", "white gold"
            }

        self.apparel      |= {keyword+"s" for keyword in self.apparel}
        self.shoes        |= {keyword+"s" for keyword in self.shoes}
        self.bags         |= {keyword+"s" for keyword in self.bags}
        self.jewelry      |= {keyword+"s" for keyword in self.jewelry}
        self.accessories  |= {keyword+"s" for keyword in self.accessories}

    def get_usd_exchange_rate(self):
        exchange_link = "https://currency-api.appspot.com/api/GBP/USD.json"
        result = urllib2.urlopen(exchange_link).read()
        exchange_rate = json.loads(result).get('rate', None)
        if exchange_rate:
            return float(exchange_rate)
        else:
            return None

    def get_eur_exchange_rate(self):
        exchange_link = "https://currency-api.appspot.com/api/GBP/EUR.json"
        result = urllib2.urlopen(exchange_link).read()
        exchange_rate = json.loads(result).get('rate', None)
        if exchange_rate:
            return float(exchange_rate)
        else:
            return None

    def convert_from_gbp_to_usd(self, amount):
        if not self.usd_exchange_rate:
            return "Error"
        else:
            value = amount * self.usd_exchange_rate
            return float("{0:.1f}".format(value))

    def convert_from_gbp_to_eur(self, amount):
        if not self.eur_exchange_rate:
            return "Error"
        else:
            value = amount * self.eur_exchange_rate
            return float("{0:.1f}".format(value))

    def get_stock_status(self, sizes):
        stock_dic = {}
        for el in sizes:
            value = el.get("value")
            size = el.text.replace("- Sold Out", "").strip()
            if value == "0":
                stock_dic[size] = 1
            elif not value == "-1":
                stock_dic[size] = 3
        return stock_dic

    def get_color(self, item_name):
        for i in self.colors:
            self_color = i
            color = 'None'
            if self_color in item_name.encode('utf8').lower():
                color = self_color
                break
            else:
                continue
        return color

    def get_type(self, name, description):
        occurrences = {
            'apparel': 0,
            'shoes': 0,
            'bags': 0,
            'jewelry': 0,
            'accessories': 0
        }
        occurrences_occured = False

        name_keywords = set(name.lower().split(" "))
        if len(self.apparel.intersection(name_keywords)):
            return "A"
        elif len(self.shoes.intersection(name_keywords)):
            return "S"
        elif len(self.bags.intersection(name_keywords)):
            return "B"
        elif len(self.jewelry.intersection(name_keywords)):
            return "J"
        elif len(self.accessories.intersection(name_keywords)):
            return "R"

        description_keywords = set(description.lower().split(" "))
        intersection = self.apparel.intersection(description_keywords)
        if len(intersection):
            occurrences['apparel'] += len(intersection)
            occurrences_occured = True
        intersection = self.shoes.intersection(description_keywords)
        if len(intersection):
            occurrences['shoes'] += len(intersection)
            occurrences_occured = True
        intersection = self.bags.intersection(description_keywords)
        if len(intersection):
            occurrences['bags'] += len(intersection)
            occurrences_occured = True
        intersection = self.jewelry.intersection(description_keywords)
        if len(intersection):
            occurrences['jewelry'] += len(intersection)
            occurrences_occured = True
        intersection = self.accessories.intersection(description_keywords)
        if len(intersection):
            occurrences['accessories'] += len(intersection)
            occurrences_occured = True

        if not occurrences_occured:
            return ""

        matched_type = max(occurrences, key=occurrences.get)
        if matched_type == "apparel":
            return "A"
        elif matched_type == "shoes":
            return "S"
        elif matched_type == "bags":
            return "B"
        elif matched_type == "jewelry":
            return "J"
        elif matched_type == "accessories":
            return "R"
        else:
            return ""

    def parse_item(self, response):
        product = OxygendemoItem()
        d = pq(response.body)

        name = d("#container .right h2").text().strip()
        description = d("#accordion div")[0].text.strip()
        if not description:
            description = d("p.MsoNormal").text().strip()
        img_objects = d('.cloud-zoom-gallery')
        sizes = d("select#ctl00_ContentPlaceHolder1_ddlSize option")
        price_object = d(".price.geo_16_darkbrown span")
        price = price_object[1].text.strip()
        sale_price = price_object[2].text.strip()
        sale_discount = 0
        if not price and not sale_price:
            price = d(".price.geo_16_darkbrown").text().strip()[1:]
            price = float(price)
        else:
            price = float(price)
            sale_price = float(sale_price)
            sale_discount = (sale_price / price) * 100
            sale_discount = float("{0:.1f}".format(sale_discount))
        designer_desc_1 = d("#accordion div")[-1].text
        designer_desc_2 = d("#accordion div p").text()
        name = unicode(name)
        description = unicode(description)

        product['type_'] = self.get_type(name, description)
        # All oxygenboutique's products are for female customers
        # I could guess gender by the type of a product but it was unnecessary
        product['gender']= 'F'
        product['designer'] = d(".brand_name a").text().strip()
        product['code'] = response.url.rpartition("/")[2].replace(".aspx","")
        product['name'] = unicode(name)
        product['description'] = unicode(description)
        product['raw_color'] = self.get_color(product['name'])
        product['image_urls'] = [response.urljoin(i.get("href")) for i in img_objects]
        product["usd_price"] = self.convert_from_gbp_to_usd(price)
        product['sale_discount'] = sale_discount
        product['stock_status'] = self.get_stock_status(sizes)
        product['link'] = response.url
        product['eur_price'] = self.convert_from_gbp_to_eur(price)
        product['gpb_price'] = price
        return product