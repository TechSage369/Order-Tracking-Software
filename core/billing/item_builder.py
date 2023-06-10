from .models import Item, Order, OrderItem

ITEMS = [
    # Starter Section
    ('Chicken Chilli', 150),
    ('Pork Chilli', 180),
    ('Chicken Septa', 140),
    ('Pork Septa', 170),
    ('Chicken 65', 170),
    ('Chicken Schzwan', 160),
    ('Chicken Lollypop', 180),

    # Fried Rice Section
    ('Chicken Fried Rice', 120),
    ('Pork Fried Rice', 140),
    ('Veg Fried Rice', 100),
    ('Chicken Schezwan Fried Rice', 140),
    ('Pork Schezwan Fried Rice', 160),
    ('Veg Schezwan Fried Rice', 120),
    ('Veg Mixed Fried Rice', 130),
    ('Chicken Mixed Fried Rice', 170),
    ('Pork Mixed Fried Rice', 180),
    ('Veg Ginger Burn Fried Rice', 130),
    ('Chicken Ginger Burn Fried Rice', 150),
    ('Mushroom Capsicum Fried Rice', 120),
    ('Egg Fried Rice', 120),
    ('Triple Fried Rice', 200),

    # Noodles Section
    ('Chicken Noodles', 100),
    ('Chicken Chowmein', 120),
    ('Pork Chowmein', 140),
    ('Veg Hakka Noodles', 100),
    ('Chicken Hakka Noodles', 120),
    ('Pork Hakka Noodles', 140),
    ('Veg Schezwan Noodles', 120),
    ('Chicken Schezwan Noodles', 150),
    ('Pork Schezwan Noodles', 170),
    ('Veg Chilli Garlic Noodles', 120),
    ('Chicken Chilli Garlic Noodles', 140),
    ('Pork Chilli Garlic Noodles', 160),
    ('Veg Mixed Noodles', 140),
    ('Chicken Mixed Noodles', 170),
    ('Pork Mixed Noodles', 190),
    ('Egg Noodles', 120),
    ('Ramen Noodles', 150),

    # Thukpa Setion
    ('Veg Thukpa', 50),
    ('Chicken Thukpa', 60),
    ('Pork Thukpa', 80),

    # Momo Section
    ('Veg Momo', 50),
    ('Veg Fried Momo', 70),
    ('Chicken Momo', 70),
    ('Chicken Fried Momo', 90),
    ('Chicken Thai-pho', 70),

    # Pasta section
    ('Veg Pasta', 90),
    ('Veg Cheese Pasta', 110),
    ('Chicken With Cheese Pasta', 130),
    ('Cheese Pasta', 100),
    ('Carbonara Pasta', 150),

    # Burger Section
    ('Veg Burger', 80),
    ('Chicken Burger', 100),
    ('Ham Burger', 150),

    # Coffee Section
    ('Cafe Latte', 60),
    ('Honey Latte', 80),
    ('Cafe Mocha', 80),
    ('Hazelnut Capuccino', 80),
    ('Mocha Madness', 90),
    ('Cold Coffee', 70),
    ('Cold Coffee With Ice Cream', 90),
    ('Americano', 30),
    ('Ice Latte', 60),
    ('Ice Hazelnut Capuccino', 80),
    ('Ice Mocha', 60),

    # Pizza
    ('Magarita Pizza', 220),
    ('Double Cheese Pizza', 250),
    ('Special Veg pizza', 240),
    ('Creamy Veg Pizza', 220),
    ('Mushroom Pizza', 250),
    ('Chicken Red Pizza', 250),
    ('Chicken Sausage Pizza', 250),
    ('Regina Pizza', 260),
    ('Queen Pizza', 270),

    # Tea
    ('Milk Tea', 20),
    ('Black Tea', 15),
    ('Lemon Tea', 20),
    ('Ginger Black Tea', 25),
    ('Honey Black Tea', 30),

    # Sandwich
    ('Veg Sandwich(Non Grilled)', 50),
    ('Veg Sandwich(Grilled)', 70),
    ('Chicken Sandwich(Non Grilled)', 70),
    ('Chicken Sandwich(Grilled)', 90),
    ('Cheese Sandwich(Non Grilled)', 70),
    ('Cheese Sandwich(Grilled)', 90),
    ('Chicken Cheese Sandwich(Non Grilled)', 80),
    ('Chicken Cheese Sandwich(Grilled)', 100),

    # Milkshake
    ('Oreo Milkshake', 90),
    ('Strawberry Milkshake', 90),
    ('Mango Milkshake', 90),
    ('Black Current Milkshake', 90),
    ('Kiwi Milkshake', 90),
    ('Blue Berry Milkshake', 90),
    ('Blue Lagoon Milkshake', 110),

    # Chocolate
    ('Hot Chocolate', 70),
    ('Cold Chocolate', 50),

    # Soda
    ('Fresh Lime Soda (Sweet)', 70),
    ('Fresh Lime Soda (Salty)', 40),

    # Sausage
    ('Chicken Sausage', 150),
    ('Pork Sausage', 160),

    # Manchurian
    ('Veg Manchurian', 100),
    ('Chicken Manchurian', 150),

    # Pakoda
    ('Veg Pakoda', 60),
    ('Onion Pakoda', 70),
    ('Cheese Pakoda', 70),

    # Fries
    ('French Fries', 100),
    ('Peri Peri Fries', 100),
    ('Cheese Fries', 130),
]


def build_items(items: list = ITEMS):
    for item in items:
        print('Creating item: ', item[0])
        Item.objects.create(
            name=item[0],
            price=item[1]
        )
    print('Items created successfully.')


if __name__ == "__main__":
    build_items()
