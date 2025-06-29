"""
Database population script with consistent data for Pakistan's tourism
"""

from app import create_app, db
from models import Admin, User, Destination, Hotel, Restaurant, Review, Booking, Reservation, Favourite, Visit
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
import random

def get_placeholder_image(category):
    """Get a real placeholder image URL based on category"""
    base_urls = {
        'Religious Site': [
            'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Badshahi_Mosque_July_1_2005_pic32_by_Ali_Imran_%28crop%29.jpg/1280px-Badshahi_Mosque_July_1_2005_pic32_by_Ali_Imran_%28crop%29.jpg',  # Badshahi Mosque Full View
            'https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Faisal_Mosque_At_Night.jpg/1280px-Faisal_Mosque_At_Night.jpg',  # Faisal Mosque Night View
            'https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/Faisal_Mosque_Main_View.jpg/1280px-Faisal_Mosque_Main_View.jpg',  # Faisal Mosque Day View
            'https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Shah_Jahan_Mosque.jpg/300px-Shah_Jahan_Mosque.jpg'  # Shah Jahan Mosque
        ],
        'Historical': [
            'https://upload.wikimedia.org/wikipedia/commons/thumb/9/92/Lahore_Fort.jpg/250px-Lahore_Fort.jpg',  # Lahore Fort Main
            'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Lahore_Fort_view_from_Baradari.jpg/330px-Lahore_Fort_view_from_Baradari.jpg',  # Lahore Fort Baradari
            'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5b/Rohtas_Fort.jpg/300px-Rohtas_Fort.jpg'  # Rohtas Fort
        ],
        'Hill Station': [
            'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Muree_veiw.jpg/250px-Muree_veiw.jpg',  # Murree Viewpoint
            'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Murree_Mall.jpg/250px-Murree_Mall.jpg',  # Murree Mall Road
            'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Mall_Road_Murree.jpg/300px-Mall_Road_Murree.jpg'  # Mall Road Another View
        ],
        'Archaeological': [
            'https://upload.wikimedia.org/wikipedia/commons/thumb/8/89/Mohenjo-daro_Residential_Area.jpg/1280px-Mohenjo-daro_Residential_Area.jpg',  # Mohenjo-daro Residential Area
            'https://upload.wikimedia.org/wikipedia/commons/thumb/7/71/Takht-i-Bahi-Pakistan.jpg/1280px-Takht-i-Bahi-Pakistan.jpg',  # Takht-i-Bahi Panoramic View
            'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/Taxila_Ruins.jpg/1280px-Taxila_Ruins.jpg',  # Taxila Main Ruins
            'https://upload.wikimedia.org/wikipedia/commons/thumb/5/57/Taxila_Pakistan_2016.jpg/1280px-Taxila_Pakistan_2016.jpg'  # Taxila Archaeological Site
        ],
        'Monument': [
            'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Minar_e_Pakistan_night_image.jpg/250px-Minar_e_Pakistan_night_image.jpg',  # Minar-e-Pakistan
            'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/Pakistan_Monument_Islamabad_by_Usman_Ghani.jpg/300px-Pakistan_Monument_Islamabad_by_Usman_Ghani.jpg',  # Pakistan Monument
            'https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/Faisal_Mosque_From_Damn_e_Koh.jpg/300px-Faisal_Mosque_From_Damn_e_Koh.jpg'  # Faisal Mosque View
        ],
        'Natural Landscape': [
            'https://upload.wikimedia.org/wikipedia/commons/thumb/9/96/Mahodand_l.jpg/250px-Mahodand_l.jpg',  # Mahodand Lake
            'https://upload.wikimedia.org/wikipedia/commons/thumb/b/bf/Shangrila_resort_Skardu.jpg/300px-Shangrila_resort_Skardu.jpg',  # Shangrila Resort
            'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/Deosai_Plains_Pakistan.jpg/300px-Deosai_Plains_Pakistan.jpg',  # Deosai Plains
            'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e8/Hingol_National_Park_Balochistan_Pakistan.jpg/300px-Hingol_National_Park_Balochistan_Pakistan.jpg'  # Hingol National Park
        ],
        'City View': [
            'https://upload.wikimedia.org/wikipedia/commons/thumb/0/0b/Ataturk_Avenue_-_Islamabad.JPG/330px-Ataturk_Avenue_-_Islamabad.JPG',  # Islamabad
            'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Mall_Road%2C_Lahore.jpg/300px-Mall_Road%2C_Lahore.jpg',  # Lahore Mall Road
            'https://upload.wikimedia.org/wikipedia/commons/thumb/0/06/Liberty_Market.jpg/300px-Liberty_Market.jpg'  # Liberty Market Lahore
        ],
        'Historical Garden': [
            'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d8/Shalimar_Gardens_Lahore.jpg/300px-Shalimar_Gardens_Lahore.jpg',  # Shalimar Gardens
            'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c4/Hazuri_Bagh_Lahore.JPG/300px-Hazuri_Bagh_Lahore.JPG',  # Hazuri Bagh
            'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/Khyber_Pass_Photo.jpg/300px-Khyber_Pass_Photo.jpg'  # Khyber Pass View
        ],
        'Mountain': [
            'https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/Passu_Cones_from_Karakoram_Highway.jpg/300px-Passu_Cones_from_Karakoram_Highway.jpg',  # Passu Cones
            'https://upload.wikimedia.org/wikipedia/commons/thumb/5/59/Nanga_Parbat_from_Fairy_Meadows.jpg/300px-Nanga_Parbat_from_Fairy_Meadows.jpg',  # Nanga Parbat
            'https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Baltoro_glacier_from_Urdukas.jpg/300px-Baltoro_glacier_from_Urdukas.jpg'  # Baltoro Glacier
        ],
        'hotel': [
            'https://upload.wikimedia.org/wikipedia/commons/thumb/6/61/Pearl_Continental_Hotel_Lahore_at_Night.jpg/1280px-Pearl_Continental_Hotel_Lahore_at_Night.jpg',  # PC Hotel Lahore Night View
            'https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/Islamabad_Serena_Hotel_at_Night.jpg/1280px-Islamabad_Serena_Hotel_at_Night.jpg',  # Serena Hotel Islamabad Night View
            'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Marriott_Hotel_Islamabad_Facade.jpg/1280px-Marriott_Hotel_Islamabad_Facade.jpg',  # Marriott Islamabad Facade
            'https://upload.wikimedia.org/wikipedia/commons/thumb/8/89/Islamabad_Marriott_Hotel_Evening_View.jpg/1280px-Islamabad_Marriott_Hotel_Evening_View.jpg',  # Marriott Evening View
            'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Avari_Lahore_Hotel_Facade.jpg/1280px-Avari_Lahore_Hotel_Facade.jpg',  # Avari Lahore
            'https://upload.wikimedia.org/wikipedia/commons/thumb/b/bf/Shangrila_resort_Skardu.jpg/1280px-Shangrila_resort_Skardu.jpg',  # Shangrila Resort
            'https://upload.wikimedia.org/wikipedia/commons/thumb/9/96/PC_Bhurban.jpg/1280px-PC_Bhurban.jpg',  # PC Hotel Bhurban
        ],
        'restaurant': [  # Keeping the working restaurant images
            'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4',
            'https://images.unsplash.com/photo-1552566626-52f8b828add9',
            'https://images.unsplash.com/photo-1559339352-11d035aa65de'
        ]
    }
    
    # Get the appropriate category URLs or default to hotel images
    urls = base_urls.get(category, base_urls['hotel'])
    return random.choice(urls)

def populate_database():
    # Create application context
    app = create_app()
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()

        # Create admin
        admin = Admin(
            name='System Admin',
            email='admin@tourism.pk',
        )
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Create sample users (25 users)
        user_names = [
            'Asad Khan', 'Fatima Ahmad', 'Omar Malik', 'Zainab Ali', 'Hassan Raza',
            'Ayesha Siddiqui', 'Imran Qureshi', 'Sana Malik', 'Bilal Ahmed', 'Mehwish Khan',
            'Adeel Hussain', 'Saima Nawaz', 'Kamran Ali', 'Nadia Malik', 'Shahid Khan',
            'Amna Zahid', 'Faisal Mahmood', 'Hira Abbas', 'Naveed Ahmed', 'Sadia Khan',
            'Usman Ali', 'Rabia Aziz', 'Tariq Malik', 'Samina Rashid', 'Yasir Hameed'
        ]
        users = []
        for i, name in enumerate(user_names):
            email = f"{name.lower().replace(' ', '.')}@example.com"
            phone = f"+92 {random.choice(['300','301','302','303','304','305','333'])} {random.randint(1000000,9999999)}"
            user = User(name=name, email=email, contactNumber=phone)
            user.set_password('user123')
            db.session.add(user)
            users.append(user)

        # Create destinations (updated with real Pakistani locations)
        destinations_data = [
            # Historical Sites
            ('Lahore Fort', 'Fort Road', 'Lahore', 'Historical',
             'A UNESCO World Heritage site built in the 11th century and extensively rebuilt during the Mughal era. ' +
             'Features stunning architectural masterpieces like Sheesh Mahal (Palace of Mirrors), Diwan-i-Aam (Hall of Public Audience), ' +
             'and Naulakha pavilion, showcasing the grandeur of Mughal architecture.'),
            
            # Religious Sites
            ('Badshahi Mosque', 'Walled City', 'Lahore', 'Religious Site',
             'Built in 1673 by Mughal Emperor Aurangzeb, it is one of the world\'s largest mosques with a capacity of 100,000 worshippers. ' +
             'Known for its stunning Mughal architecture with four minarets, three domes, and a vast courtyard made of handcrafted marble.'),
            ('Faisal Mosque', 'Shah Faisal Avenue', 'Islamabad', 'Religious Site',
             'The largest mosque in Pakistan, designed by Turkish architect Vedat Dalokay to resemble a Bedouin tent. ' +
             'Located at the foot of Margalla Hills, its modern Islamic architecture and serene atmosphere make it a must-visit landmark.'),
            ('Wazir Khan Mosque', 'Delhi Gate', 'Lahore', 'Religious Site',
             'Built in 1634, this mosque is renowned for its extensive fresco work and tile decorations. ' +
             'The mosque represents the finest elements of Mughal era architecture and Persian style tile work.'),
            
            # Archaeological Sites
            ('Mohenjo-daro', 'Larkana District', 'Larkana', 'Archaeological',
             'One of the largest settlements of the ancient Indus Valley Civilization, built around 2500 BCE. ' +
             'This UNESCO World Heritage site features well-preserved ruins of an ancient urban center with advanced city planning.'),
            ('Taxila', 'Taxila Valley', 'Rawalpindi', 'Archaeological',
             'An important archaeological site featuring ruins from multiple civilizations dating from 5th century BCE to 2nd century CE. ' +
             'Home to ancient Buddhist monasteries, temples, and the famous Taxila Museum.'),
            ('Takht-i-Bahi', 'Mardan', 'Mardan', 'Archaeological',
             'A well-preserved Buddhist monastery from the 1st century CE. This UNESCO World Heritage site ' +
             'sits atop a hill and offers insights into ancient Buddhist architecture and life.'),
            
            # Monuments
            ('Minar-e-Pakistan', 'Greater Iqbal Park', 'Lahore', 'Monument',
             'A national monument built between 1960-1968 on the site where the Pakistan Resolution was passed. ' +
             'The 70-meter tall tower blends Islamic, Mughal and modern architecture, symbolizing Pakistan\'s independence.'),
            ('Pakistan Monument', 'Shakarparian Hills', 'Islamabad', 'Monument',
             'A modern architectural marvel representing Pakistan\'s four provinces and three territories. ' +
             'The flower-shaped monument offers a museum and stunning views of Islamabad.'),
            ('Tomb of Jahangir', 'Shahdara Bagh', 'Lahore', 'Monument',
             'The mausoleum of Mughal Emperor Jahangir, built in 1637. Known for its intricate marble work, ' +
             'pietra dura inlay, and geometrical patterns representing Mughal architecture at its finest.'),

            # Natural Landscapes
            ('Mahodand Lake', 'Ushu Valley', 'Swat', 'Natural Landscape',
             'A stunning alpine lake surrounded by snow-capped peaks in the Ushu Valley of Swat. ' +
             'Known for its crystal-clear waters, surrounding meadows, and excellent trout fishing opportunities.'),
            ('Hunza Valley', 'Karakoram Highway', 'Hunza', 'Natural Landscape',
             'A picturesque valley surrounded by snow-capped peaks including Rakaposhi and Ultar Sar. ' +
             'Famous for its turquoise rivers, ancient forts, and apricot orchards.'),
            ('Deosai Plains', 'Skardu Region', 'Skardu', 'Natural Landscape',
             'The second-highest plateau in the world at 4,114 meters. Known as the "Land of Giants", ' +
             'it features stunning wildflower meadows and is home to the Himalayan brown bear.'),
            ('Fairy Meadows', 'Diamer District', 'Chilas', 'Natural Landscape',
             'A lush green plateau offering spectacular views of Nanga Parbat, the world\'s ninth-highest mountain. ' +
             'Popular for camping, hiking, and experiencing traditional mountain life.'),

            # Museums
            ('Lahore Museum', 'Mall Road', 'Lahore', 'Museum',
             'Founded in 1865, it houses one of Pakistan\'s finest collections of Buddhist art, ' +
             'Mughal and Sikh artifacts, and Islamic relics. Features the famous Fasting Buddha statue.'),
            ('Pakistan National Museum', 'Burns Road', 'Karachi', 'Museum',
             'The country\'s premier museum showcasing artifacts from the Indus Valley Civilization, ' +
             'Gandhara period, and Islamic era, along with manuscripts and paintings.'),
            ('Lok Virsa Museum', 'Garden Avenue', 'Islamabad', 'Museum',
             'A cultural museum preserving Pakistan\'s folk heritage through exhibits of traditional ' +
             'crafts, music instruments, textiles, and cultural artifacts.'),

            # Historical Gardens
            ('Shalimar Gardens', 'GT Road', 'Lahore', 'Historical Garden',
             'A Persian-style garden built in 1642 by Mughal Emperor Shah Jahan. This UNESCO World Heritage site ' +
             'features three terraces, marble pavilions, and fountains in perfect symmetry.'),
            ('Hazuri Bagh', 'Walled City', 'Lahore', 'Historical Garden',
             'A garden square between Lahore Fort and Badshahi Mosque, featuring the white marble Hazuri Bagh ' +
             'Baradari built by Maharaja Ranjit Singh in 1818.'),
            ('Mughal Garden Wah', 'Wah', 'Wah Cantt', 'Historical Garden',
             'A classical Mughal garden built during Emperor Akbar\'s reign, featuring traditional char-bagh ' +
             'layout with water channels, fountains, and ancient trees.'),

            # Hill Stations
            ('Murree', 'Mall Road', 'Murree', 'Hill Station',
             'A charming hill station established in 1851, located in the Galyat region of Punjab. ' +
             'Famous for its colonial architecture, scenic Mall Road, and panoramic mountain views. ' +
             'Popular for summer retreats and winter snow activities.'),
            ('Kashmir Point', 'Upper Murree', 'Murree', 'Hill Station',
             'One of Murree\'s highest viewpoints offering breathtaking views of Kashmir and the surrounding mountains. ' +
             'Features historic architecture and traditional tea houses.'),
            ('Pindi Point', 'Lower Mall', 'Murree', 'Hill Station',
             'A famous tourist spot in Murree offering views of Rawalpindi and featuring a chair lift. ' +
             'Popular for its sunset views and family activities.')
        ]

        destinations = []
        for name, street, city, category, description in destinations_data:
            dest = Destination(
                name=name,
                street=street,
                city=city,
                description=description,
                category=category,
                imageURL=get_placeholder_image(category),
                adminID=1
            )
            db.session.add(dest)
            destinations.append(dest)
        db.session.flush()        # Create hotels
        hotels_data = [            # 5-Star Hotels
            ('Pearl Continental Lahore', 'Mall Road', 'Lahore',
             'Luxury 5-star hotel with swimming pool, spa, multiple fine dining restaurants, grand ballroom, ' 
             'state-of-the-art conference facilities, fully equipped gym, and premium shopping arcade'),
            ('Serena Islamabad', 'Khayaban-e-Suhrwardy', 'Islamabad',
             'Premium 5-star hotel featuring luxury spa, international cuisine restaurants, modern conference center, ' 
             'outdoor pool with garden views, traditional architecture, and diplomatic security standards'),
            ('Marriott Islamabad', 'Agha Khan Road', 'Islamabad',
             'Landmark 5-star hotel with multiple restaurants, extensive conference facilities, luxury spa, ' 
             'fitness center, outdoor pool, and premium security features'),
            ('Shangrila Resort Skardu', 'Skardu Valley', 'Skardu',
             'Spectacular resort overlooking Skardu Valley and Upper Kachura Lake, featuring traditional architecture, ' 
             'mountain views, restaurant serving local and international cuisine, and outdoor activities'),
            ('Pearl Continental Bhurban', 'Mall Road', 'Bhurban',
             'Mountain resort hotel with panoramic views, indoor pool, spa facilities, multiple restaurants, ' 
             'conference center, and recreational activities'),
            ('Avari Lahore', 'Mall Road', 'Lahore',
             'Historic 5-star hotel with rooftop pool, multiple restaurants, business center, spa facilities, ' 
             'and premium shopping area')
        ]

        hotels = []
        for name, street, city, facilities in hotels_data:
            hotel = Hotel(
                name=name,
                street=street,
                city=city,
                facilities=facilities,
                imageURL=get_placeholder_image('hotel'),
                adminID=1
            )
            db.session.add(hotel)
            hotels.append(hotel)
        db.session.flush()

        # Create restaurants (25 restaurants)
        cuisine_types = ['Pakistani', 'Continental', 'Chinese', 'BBQ', 'Seafood', 
                        'Traditional', 'Fast Food', 'Afghan', 'Italian', 'Local']
        
        restaurants_data = [
            # Fine Dining
            ('Andaaz Restaurant', 'Fort Road', 'Lahore', 'Pakistani'),
            ('Fujiyama', 'Zamzama', 'Karachi', 'Japanese'),
            ('Cosa Nostra', 'F-7', 'Islamabad', 'Italian'),
            ('Dumpukht', 'Pearl Continental', 'Lahore', 'Pakistani'),
            ('Okra', 'Zamzama', 'Karachi', 'Continental'),

            # Traditional Restaurants
            ('Haveli Restaurant', 'Food Street', 'Lahore', 'Pakistani'),
            ('Shiraz Golden', 'Jinnah Super', 'Islamabad', 'Afghan'),
            ('BBQ Tonight', 'Bilawal House', 'Karachi', 'BBQ'),
            ('Cafe Lazeez', 'Liberty', 'Lahore', 'Pakistani'),
            ('Dastarkhwan', 'Gulberg', 'Lahore', 'Pakistani'),

            # Cafes
            ('Cafe de Hunza', 'Karimabad', 'Hunza', 'Local'),
            ('Gloria Jeans', 'MM Alam Road', 'Lahore', 'Continental'),
            ('Mocca Coffee', 'F-6', 'Islamabad', 'Continental'),
            ('Butlers Chocolate Café', 'Clifton', 'Karachi', 'Continental'),
            ('Chai Kitchen', 'DHA', 'Lahore', 'Pakistani'),

            # Local Cuisine
            ('Peshawar Namak Mandi', 'Saddar', 'Peshawar', 'Pakistani'),
            ('Sindh Biryani House', 'Burns Road', 'Karachi', 'Pakistani'),
            ('Salt n Pepper Village', 'Liberty', 'Lahore', 'Pakistani'),
            ('Islamabad Dharbar', 'Blue Area', 'Islamabad', 'Pakistani'),
            ('Balochi Sajji', 'Maripur', 'Karachi', 'Pakistani'),

            # Specialty Restaurants
            ('Bamboo Union', 'MM Alam Road', 'Lahore', 'Chinese'),
            ('Pompei', 'Zamzama', 'Karachi', 'Italian'),
            ('Khiva', 'Saidpur Village', 'Islamabad', 'Continental'),
            ('Dynasty', 'Avari Towers', 'Karachi', 'Chinese'),
            ('Street 1 Cafe', 'Gulberg', 'Lahore', 'Continental')
        ]

        restaurants = []
        for name, street, city, cuisine in restaurants_data:
            # Find destinations in the same city
            city_destinations = [d for d in destinations if d.city == city]
            if not city_destinations:
                # If no destination in the same city, pick a random one
                dest = random.choice(destinations)
            else:
                dest = random.choice(city_destinations)
            
            restaurant = Restaurant(
                name=name,
                street=street,
                city=city,
                cuisine=cuisine,
                destinationID=dest.destinationID,
                adminID=1,
                imageURL=get_placeholder_image('restaurant')
            )
            db.session.add(restaurant)
            restaurants.append(restaurant)
        db.session.flush()

        # Create reviews (50 reviews)
        review_comments = [
            'Excellent experience!', 'Highly recommended!', 'Great service!',
            'Amazing place!', 'Will definitely come back!', 'Outstanding!',
            'Good value for money', 'Fantastic atmosphere', 'Lovely staff',
            'Perfect location', 'Beautiful view', 'Delicious food'
        ]
        
        for _ in range(50):
            review_type = random.choice(['destination', 'hotel', 'restaurant'])
            user = random.choice(users)
            rating = random.randint(3, 5)  # Mostly positive reviews
            comment = random.choice(review_comments)
            
            review = Review(
                userID=user.userID,
                rating=rating,
                comment=comment
            )
            
            if review_type == 'destination':
                review.destinationID = random.choice(destinations).destinationID
            elif review_type == 'hotel':
                review.hotelID = random.choice(hotels).hotelID
            else:
                review.restaurantID = random.choice(restaurants).restaurantID
                
            db.session.add(review)

        # Create bookings (30 bookings)
        room_types = ['Standard', 'Deluxe', 'Executive', 'Suite', 'Mountain View', 'Family Room']
        current_date = datetime.now()
        
        for _ in range(30):
            days_ahead = random.randint(1, 180)
            stay_duration = random.randint(1, 7)
            check_in = current_date + timedelta(days=days_ahead)
            check_out = check_in + timedelta(days=stay_duration)
            
            booking = Booking(
                userID=random.choice(users).userID,
                hotelID=random.choice(hotels).hotelID,
                checkInDate=check_in,
                checkOutDate=check_out,
                roomType=random.choice(room_types)
            )
            db.session.add(booking)

        # Create reservations (30 reservations)
        for _ in range(30):
            restaurant = random.choice(restaurants)  # First select a restaurant
            if restaurant:  # Only create reservation if we have a valid restaurant
                days_ahead = random.randint(1, 30)
                reservation_date = current_date + timedelta(days=days_ahead)
                hour = random.randint(18, 22)
                minute = random.choice([0, 30])
                reservation_time = datetime.strptime(f'{hour}:{minute}', '%H:%M').time()
                
                reservation = Reservation(
                    userID=random.choice(users).userID,
                    restaurantID=restaurant.restaurantID,  # Use the selected restaurant's ID
                    reservationDate=reservation_date,
                    reservationTime=reservation_time,
                    numberOfGuests=random.randint(2, 8)
                )
                db.session.add(reservation)

        # Create favorites (40 favorites)
        for _ in range(40):
            favorite = Favourite(
                userID=random.choice(users).userID,
                destinationID=random.choice(destinations).destinationID
            )
            db.session.add(favorite)

        # Create visits (40 visits)
        for _ in range(40):
            days_ago = random.randint(1, 365)
            visit_date = current_date - timedelta(days=days_ago)
            
            visit = Visit(
                userID=random.choice(users).userID,
                destinationID=random.choice(destinations).destinationID,
                visitDate=visit_date
            )
            db.session.add(visit)

        # Commit all changes
        db.session.commit()
        print("Database populated successfully!")

if __name__ == '__main__':
    populate_database()