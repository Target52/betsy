__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

from models import *
from datetime import datetime
from rich import print
import os

# Search:
def search(term: str):
    term = term.lower()
    query = Products.select().where(Products.name.contains(term) | Products.desc.contains(term))
    p_q = []
    if query:
        for product in query:
            p_q.append(product.name)
        print(f"Search term {term} found in:{p_q}")
    else:
        print(f"[bold red]No products found with {term}[/bold red]")

# Producten van user:
def list_user_products(user_id: int):
    query = Products.select().where(Products.owner == user_id)
    if query:
        user = Users.get_by_id(user_id)
        print(f"Products of {user.name}:")
        for product in query: print(f"{product.name}, stock: {product.stock}")
    else:
        print(f"[bold red]No match found or invalid id was given.[/bold red]")

# Producten per tag:
def list_products_per_tag(tag_id: int):
    query = Products.select().join(ProductTag).join(
        Tags).where(Tags.tag_id == tag_id)
    if query:
        tag = Tags.get_by_id(tag_id)
        p_q = []
        for product in query:
            p_q.append(product.name)
        print(f"Tagged products with tag {tag.name}: {p_q}")
    else:
        print("[bold red]No products with this tag or tag doesn't exist[/bold red]")

# Product toevoegen:
def add_product_to_catalog(user_id: int, product_id: int):
    user = Users.get_by_id(user_id)
    product = Products.get_by_id(product_id)
    product.owner = user
    product.save()
    print(f"Product {product.name} added for {user.name}")

# Product hoeveelheid veranderen:
def update_stock(product_id, new_quantity):
    query = Products.get_by_id(product_id)
    old_stock = query.stock
    query.stock = new_quantity
    query.save()
    print(f"Stock changed of {query.name} from: {old_stock} to: {new_quantity}")

# Product verkopen:
def purchase_product(product_id: int, buyer_id: int, quantity: int):
    product = Products.get_by_id(product_id)
    buyer = Users.get_by_id(buyer_id)
    if buyer_id == product.owner:
        print(f"[bold red]You cannot buy products from yourself {buyer.name}.[/bold red]")
    if quantity >= product.stock:
        print(f"[bold red]Insufficient stock of {product.name}![/bold red] [bold]Current stock is {product.stock}.[/bold]")
    else:
        print(f"{buyer.name} bought {quantity} {product.name}")
        new_quantity = product.stock - quantity
        update_stock(product_id, new_quantity)

# Product verwijderen:
def remove_product(product_id):
    try:
        query = Products.get_by_id(product_id)
        print(f"Product {query.name} removed")
        query.delete_instance()
    except DoesNotExist:
        print(f"Product id {product_id} doesn't exist or already removed.")

# Database verwijderen:
def delete_database():
    cwd = os.getcwd()
    database_path = os.path.join(cwd, "betsy.db")
    if os.path.exists(database_path):
        os.remove(database_path)

# Aanmaken database:
def insert_data():
    db.connect()
    db.create_tables([Users, Products, Tags, ProductTag, Transactions])
    # create users
    jdehaan = Users.create(name="Jeroen de Haan", street="Kerkstraat 32", zip_code="1433 ZS", city="Meppel", billing_info="iDeal 1234567890")
    sgroot = Users.create(name="Saskia Groot", street="Laan vanm Vrede  34", zip_code="4356 BD", city="Mssstricht", billing_info="Visa")
    benniekoekoek = Users.create( name="Bennie Koekoek", street="AAchteromsteeg 31", zip_code="2388 LF", city="Amsterdam", billing_info="CC")
    jdegroot = Users.create(name="jan de Groot", street="De Waag 3", zip_code="4567 DD", city="Den Haag", billing_info="RABO")

    # create products
    appeltaart = Products.create(owner=jdehaan, name="Appeltaart", desc="Taart met appel, kaneel en rozijnen. Allergenen: gluten, lactose", price=12.00, stock=2,)
    cocoscake = Products.create(owner=sgroot, name="Cocoscake", desc="Cake met cocos en amandelmeel. Allergenen: noten", price=8.75, stock=3,)
    brownies = Products.create(owner=benniekoekoek, name="Vegan Brownies", desc="Vegan Brownies met chocolade. Allergenen: gluten", price=6.95, stock=1,)
    scones = Products.create(owner=jdegroot, name="Scones", desc="Soort kleine cakejes. Allergenen: gluten, lactose", price=3.65, stock=13,)
    gev_koek = Products.create(owner=jdegroot, name="Gevulde koek", desc="Koek gevuld met amandelspijs. Allergenen: gluten, noten, lactose", price=2.95, stock=9,)

    # Tags
    tags_list = ['taart', 'cake', 'vegan', 'gluten', 'noten', 'cocos', 'chocolade', 'lactose', 'koek']
    for item in tags_list:
        globals()[item] = Tags.create(name=item)

    # ProductTags appeltaart:
    tags_list = ['taart', 'gluten', 'chocolade', 'lactose']
    for item in tags_list:
        ProductTag.create(product=appeltaart, tag=globals()[item])

    # Product tags brownies:
    tags_list = ['vegan', 'gluten', 'chocolade']
    for item in tags_list:
        ProductTag.create(product=brownies, tag=globals()[item])

    # Product tags cocoscake:
    tags_list = ['cake', 'gluten', 'noten']
    for item in tags_list:
        ProductTag.create(product=cocoscake, tag=globals()[item])

    # Product tags scones:
    tags_list = ['cake', 'gluten', 'lactose']
    for item in tags_list:
        ProductTag.create(product=scones, tag=globals()[item])

    # ProductTags gevulde koek:
    tags_list = ['koek', 'gluten', 'noten', 'lactose']
    for item in tags_list:
        ProductTag.create(product=gev_koek, tag=globals()[item])

def main():
    print("")
    print("Nieuwe database wordt aangemaakt")
    print("")
    if os.path.exists("betsy.db") == True:
        delete_database()
    insert_data()
    
    # Search function:
    print("Search with term [bold green]taart[/bold green], command: search('taart')")
    search("taart")
    print("")
    
    # List User Products function:
    print("Stock of user with [bold green]user_id: 4[/bold green], command: list_user_products(4)")
    list_user_products(4)
    print("")
    
    # List Products Per Tag function:
    print("Products per tag with [bold green]tag_id: 2[/bold green], command: list_products_per_tag(2)")
    list_products_per_tag(2)
    print("")

    # Add Product To Catalog function:
    print("Add product to database [bold green]user_id: 3[/bold green] and [bold green]product id: 1[/bold green], command: add_product_to_catalog(3, 1)")
    add_product_to_catalog(3, 1)
    print("")
    
    # Update Stock function:
    print("Change stock with [bold green]product_id: 2[/bold green] and adjust the [bold green]stock[/bold green] to 11, command: update_stock(2, 11)")
    update_stock(2, 11)
    print("")
    
    # Purchase Product function:
    print("Purchase product with [bold green]product_id: 4[/bold green], [bold green]buyer_id: 3[/bold green] and [bold green]quantity[/bold green] of [bold]3[/bold], command: purchase_product(4, 3, 3)")
    purchase_product(4, 3, 3)
    print("")

    # Remove Product function:
    print("remove Product with [bold green]product_id: 2[/bold green], command: remove_product(2)")
    remove_product(2)

if __name__ == '__main__':
    main()