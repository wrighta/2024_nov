// create flask_user if not created

GRANT ALL PRIVILEGES ON DATABASE recipes_db TO flask_user;


CREATE SEQUENCE category_seq;
CREATE SEQUENCE recipe_seq;

CREATE TABLE category (
    id INT PRIMARY KEY DEFAULT nextval('category_seq'),
    name VARCHAR(50) NOT NULL,
    image VARCHAR(100)
);

CREATE TABLE recipe (
    id INT PRIMARY KEY DEFAULT nextval('recipe_seq'),
    title VARCHAR(100) NOT NULL,
    description TEXT,
	ingredients TEXT,
    category_id INT,
    image VARCHAR(100),
    FOREIGN KEY (category_id) REFERENCES category(id)
);

INSERT INTO category (name, image) VALUES 
('Vegetarian', 'vegetarian.jpg'),
('Desserts', 'desserts.jpg'),
('Main Courses', 'main_courses.jpg'),
('Snacks', 'snacks.jpg'),
('Drinks', 'drinks.jpg');

INSERT INTO recipe (title, description, category_id, image, ingredients) VALUES 
-- Vegetarian Recipes
('Veggie Curry', 'Healthy and wholesome.', 1, 'veggie_curry.jpg', 'Mixed vegetables, curry powder, coconut milk, onions, garlic'),
('Mushroom Risotto', 'Creamy and flavourful.', 1, 'mushroom_risotto.jpg', 'Mushrooms, arborio rice, vegetable stock, onions, Parmesan cheese'),
('Stuffed Peppers', 'A colourful and nutritious meal.', 1, 'stuffed_peppers.jpg', 'Bell peppers, rice, tomatoes, cheese, herbs'),

-- Desserts Recipes
('Apple Pie', 'A delicious dessert.', 2, 'apple_pie.jpg', 'Apples, flour, sugar, butter, cinnamon'),
('Chocolate Chip Cookies', 'A classic treat.', 2, 'chocolate_chip_cookies.jpg', 'Flour, sugar, chocolate chips, butter, eggs, vanilla extract'),
('Lemon Drizzle Cake', 'Zesty and moist.', 2, 'lemon_drizzle_cake.jpg', 'Flour, sugar, eggs, lemon zest, butter'),

-- Main Courses Recipes
('Grilled Cheese Sandwich', 'Comfort food at its best.', 3, 'grilled_cheese_sandwich.jpg', 'Bread, cheese, butter'),
('Beef Lasagna', 'A hearty Italian favourite.', 3, 'beef_lasagna.jpg', 'Minced beef, lasagna sheets, tomato sauce, cheese, onions'),
('Chicken Stir Fry', 'Quick and healthy.', 3, 'chicken_stir_fry.jpg', 'Chicken, mixed vegetables, soy sauce, garlic, ginger'),

-- Snacks Recipes
('Popcorn', 'Perfect for movie nights.', 4, 'popcorn.jpg', 'Corn kernels, butter, salt'),
('Nachos', 'A great sharing dish.', 4, 'nachos.jpg', 'Tortilla chips, cheese, salsa, sour cream, jalapenos'),
('Hummus and Veggies', 'A healthy snack option.', 4, 'hummus_and_veggies.jpg', 'Chickpeas, tahini, olive oil, garlic, carrots, celery'),

-- Drinks Recipes
('Fruit Smoothie', 'A refreshing drink.', 5, 'fruit_smoothie.jpg', 'Bananas, strawberries, orange juice, yoghurt, ice'),
('Iced Coffee', 'A cool caffeine boost.', 5, 'iced_coffee.jpg', 'Coffee, milk, ice, sugar'),
('Green Tea Lemonade', 'Refreshing with a tangy twist.', 5, 'green_tea_lemonade.jpg', 'Green tea, lemon juice, honey, ice');
