-- Admin Table
INSERT INTO Admin (adminID, name, email, password) VALUES
(1, 'Ali Raza', 'ali.raza@tourism.pk', 'kL9#xY2pQ'),
(2, 'Fatima Khan', 'fatima.k@travelpak.com', 'mZ8!rT5sW'),
(3, 'Bilal Ahmed', 'bilal.a@discoverpk.com', 'pG3$fH7jK'),
(4, 'Zainab Shah', 'zainab.s@visitpak.com', 'qJ6^dN9bV'),
(5, 'Omar Hassan', 'omar.h@explorepk.com', 'tR4@cM1lP'),
(6, 'Sana Malik', 'sana.m@adventurepk.com', 'vX7%zF3kD'),
(7, 'Yusuf Sheikh', 'yusuf.s@heritagepk.com', 'wB5&hG8yU'),
(8, 'Ayesha Iqbal', 'ayesha.i@mountainpk.com', 'eK2!nJ7rT'),
(9, 'Kamran Siddiqui', 'kamran.s@culturalpk.com', 'sM4#pL9cA'),
(10, 'Hina Riaz', 'hina.r@desertpk.com', 'uI8$oZ1iX'),
(11, 'Tariq Mahmood', 'tariq.m@coastpk.com', 'fO6^vQ3jY'),
(12, 'Nadia Akhtar', 'nadia.a@valleypk.com', 'gP9&wR2bN'),
(13, 'Imran Aslam', 'imran.a@historicsites.pk', 'aD7@kS5mF'),
(14, 'Faisal Qureshi', 'faisal.q@northernareas.pk', 'bC1%hT4zL'),
(15, 'Mehwish Ali', 'mehwish.a@silkroadpk.com', 'iV3!jU6eW');

-- User Table
INSERT INTO User (userID, name, email, password, contactNumber) VALUES
(101, 'Ahmed Khan', 'ahmed.k@example.com', 'xY5$gH9pL', '+923331234567'),
(102, 'Sara Jamal', 'sara.j@mail.pk', 'zR8^vB2nM', '+923004567890'),
(103, 'Haris Mahmood', 'haris.m@travel.pk', 'qW7!sK3dF', '+923214567890'),
(104, 'Amina Sheikh', 'amina.s@outlook.pk', 'eT4&uJ6yI', '+923331112233'),
(105, 'Usman Raza', 'usman.r@tour.pk', 'rU9@oP1aZ', '+923008877665'),
(106, 'Zara Iqbal', 'zara.i@explore.pk', 'iP5%lO8cX', '+923214477889'),
(107, 'Babar Siddiqui', 'babar.s@adventure.pk', 'oA2^mV7bN', '+923005566778'),
(108, 'Lubna Akhtar', 'lubna.a@journey.pk', 'uL6#fK9jG', '+923219988776'),
(109, 'Kashif Malik', 'kashif.m@voyage.pk', 'yB3$hD4qR', '+923002233445'),
(110, 'Nida Hassan', 'nida.h@wander.pk', 'wV1&sE8tC', '+923216677889'),
(111, 'Farhan Qureshi', 'farhan.q@globe.pk', 'cZ7!nJ5rT', '+923001122334'),
(112, 'Saima Riaz', 'saima.r@passport.pk', 'dF9@mX2pY', '+923218899776'),
(113, 'Javed Iqbal', 'javed.i@nomad.pk', 'gH4^bU6vI', '+923004455667'),
(114, 'Tahira Shah', 'tahira.s@expedition.pk', 'jM8%kO3wA', '+923217788990'),
(115, 'Asim Ali', 'asim.a@odyssey.pk', 'lN1#qR7eS', '+923009988776');

-- Destination Table
INSERT INTO Destination (destinationID, adminID, name, street, city, description, category, image_url) VALUES
(201, 1, 'Badshahi Mosque', 'Fort Road', 'Lahore', 'Iconic Mughal-era mosque', 'Religious Site', 'https://example.com/images/badshahi_mosque.jpg'),
(202, 2, 'Faisal Mosque', 'Shah Faisal Avenue', 'Islamabad', 'Modern mosque with mountain backdrop', 'Religious Site', 'https://example.com/images/faisal_mosque.jpg'),
(203, 3, 'Lahore Fort', 'Fort Road', 'Lahore', 'UNESCO World Heritage fort complex', 'Historical', 'https://example.com/images/lahore_fort.jpg'),
(204, 4, 'Mohenjo-Daro', 'Mohenjo-Daro Road', 'Larkana', 'Ancient Indus Valley Civilization ruins', 'Archaeological', 'https://example.com/images/mohenjo_daro.jpg'),
(205, 5, 'Hunza Valley', 'Karimabad', 'Gilgit-Baltistan', 'Stunning mountain valley', 'Natural Landscape', 'https://example.com/images/hunza_valley.jpg'),
(206, 6, 'Shalimar Gardens', 'G.T. Road', 'Lahore', 'Mughal-era terraced gardens', 'Historical Garden', 'https://example.com/images/shalimar_gardens.jpg'),
(207, 7, 'K2 Base Camp', 'Concordia', 'Gilgit-Baltistan', 'Trekking destination near world''s 2nd highest peak', 'Adventure', 'https://example.com/images/k2_base_camp.jpg'),
(208, 8, 'Mazar-e-Quaid', 'M.A. Jinnah Road', 'Karachi', 'Tomb of Pakistan''s founder', 'Monument', 'https://example.com/images/mazar_e_quaid.jpg'),
(209, 9, 'Katpana Desert', 'Skardu Road', 'Skardu', 'Cold desert with sand dunes', 'Natural Landscape', 'https://example.com/images/katpana_desert.jpg'),
(210, 10, 'Baltit Fort', 'Karimabad', 'Hunza', 'Ancient fort overlooking Hunza Valley', 'Historical', 'https://example.com/images/baltit_fort.jpg'),
(211, 11, 'Derawar Fort', 'Ahmadpur East', 'Bahawalpur', 'Massive desert fortress', 'Historical', 'https://example.com/images/derawar_fort.jpg'),
(212, 12, 'Ansoo Lake', 'Kaghan Valley', 'Khyber Pakhtunkhwa', 'Tear-shaped high-altitude lake', 'Natural Landscape', 'https://example.com/images/ansoo_lake.jpg'),
(213, 13, 'Shah Jahan Mosque', 'Thatta', 'Thatta', '17th-century Mughal mosque', 'Religious Site', 'https://example.com/images/shah_jahan_mosque.jpg'),
(214, 14, 'Attabad Lake', 'Karakoram Highway', 'Hunza', 'Turquoise lake formed by landslide', 'Natural Landscape', 'https://example.com/images/attabad_lake.jpg'),
(215, 15, 'Taxila Museum', 'Taxila Museum Road', 'Taxila', 'Archaeological site museum', 'Museum', 'https://example.com/images/taxila_museum.jpg');


-- Favourite Table
INSERT INTO Favourite (destinationID, userID, favouriteDate) VALUES
(201, 101, '2023-05-15'),
(202, 102, '2023-06-20'),
(203, 103, '2023-07-10'),
(204, 104, '2023-08-05'),
(205, 105, '2023-09-12'),
(206, 106, '2023-10-18'),
(207, 107, '2023-11-22'),
(208, 108, '2023-12-03'),
(209, 109, '2024-01-15'),
(210, 110, '2024-02-20'),
(211, 111, '2024-03-10'),
(212, 112, '2024-04-05'),
(213, 113, '2024-05-12'),
(214, 114, '2024-06-18'),
(215, 115, '2024-07-22');

-- Visit Table
INSERT INTO Visit (destinationID, userID, visitDate) VALUES
(201, 101, '2023-05-20'),
(202, 102, '2023-06-25'),
(203, 103, '2023-07-15'),
(204, 104, '2023-08-10'),
(205, 105, '2023-09-17'),
(206, 106, '2023-10-23'),
(207, 107, '2023-11-27'),
(208, 108, '2023-12-08'),
(209, 109, '2024-01-20'),
(210, 110, '2024-02-25'),
(211, 111, '2024-03-15'),
(212, 112, '2024-04-10'),
(213, 113, '2024-05-17'),
(214, 114, '2024-06-23'),
(215, 115, '2024-07-27');

-- Hotel Table
INSERT INTO Hotel (hotelID, adminID, name, street, city, facilities, image_url) VALUES
(301, 1, 'Pearl Continental', 'Shahrah-e-Quaid-e-Azam', 'Lahore', 'Pool, Spa, Restaurants', 'https://example.com/images/pearl_continental.jpg'),
(302, 2, 'Serena Hotel', 'Khayaban-e-Suhrawardy', 'Islamabad', 'Gardens, Conference Rooms', 'https://example.com/images/serena_hotel.jpg'),
(303, 3, 'Nishat Hotel', 'Jail Road', 'Lahore', 'Luxury Rooms, Banquet Hall', 'https://example.com/images/nishat_hotel.jpg'),
(304, 4, 'PTDC Motel', 'Mohenjo-Daro Road', 'Larkana', 'Basic Lodging, Tours', 'https://example.com/images/ptdc_motel.jpg'),
(305, 5, 'Eagle''s Nest', 'Duikar', 'Hunza', 'Mountain Views, Restaurant', 'https://example.com/images/eagles_nest.jpg'),
(306, 6, 'Avari Hotel', 'Beaumont Road', 'Lahore', 'Business Center, Gym', 'https://example.com/images/avari_hotel.jpg'),
(307, 7, 'Concordia Lodge', 'K2 Base Camp', 'Gilgit-Baltistan', 'Basic Amenities, Guided Treks', 'https://example.com/images/concordia_lodge.jpg'),
(308, 8, 'Beach Luxury', 'M.T. Khan Road', 'Karachi', 'Sea View, Pool', 'https://example.com/images/beach_luxury.jpg'),
(309, 9, 'Shangrila Resort', 'Skardu Road', 'Skardu', 'Lake View, Adventure Sports', 'https://example.com/images/shangrila_resort.jpg'),
(310, 10, 'Hunza Serena', 'Karimabad', 'Hunza', 'Traditional Architecture, Cultural Shows', 'https://example.com/images/hunza_serena.jpg'),
(311, 11, 'Fort Derawar Camp', 'Ahmadpur East', 'Bahawalpur', 'Desert Camping, Stargazing', 'https://example.com/images/fort_derawar_camp.jpg'),
(312, 12, 'PTDC Kaghan', 'Naran Road', 'Kaghan', 'Mountain Views, Restaurant', 'https://example.com/images/ptdc_kaghan.jpg'),
(313, 13, 'Redco Inn', 'G.T. Road', 'Thatta', 'Budget Rooms, Restaurant', 'https://example.com/images/redco_inn.jpg'),
(314, 14, 'Attabad Lake Resort', 'Karakoram Highway', 'Gojal', 'Lake View, Boating', 'https://example.com/images/attabad_lake_resort.jpg'),
(315, 15, 'Taxila Inn', 'Taxila Museum Road', 'Taxila', 'Archaeological Tours, Restaurant', 'https://example.com/images/taxila_inn.jpg');

-- Booking Table
INSERT INTO Booking (bookingID, userID, hotelID, checkInDate, checkOutDate, roomType, cost) VALUES
(401, 101, 301, '2023-06-01', '2023-06-05', 'Deluxe', 150.00),
(402, 102, 302, '2023-07-10', '2023-07-15', 'Standard', 200.00),
(403, 103, 303, '2023-08-20', '2023-08-25', 'Executive', 180.00),
(404, 104, 304, '2023-09-05', '2023-09-10', 'Heritage', 75.00),
(405, 105, 305, '2023-10-12', '2023-10-17', 'Mountain View', 120.00),
(406, 106, 306, '2023-11-15', '2023-11-20', 'Business', 160.00),
(407, 107, 307, '2023-12-01', '2023-12-06', 'Trekker', 90.00),
(408, 108, 308, '2024-01-10', '2024-01-15', 'Sea View', 140.00),
(409, 109, 309, '2024-02-14', '2024-02-19', 'Lake View', 130.00),
(410, 110, 310, '2024-03-20', '2024-03-25', 'Valley View', 150.00),
(411, 111, 311, '2024-04-05', '2024-04-10', 'Desert Camp', 100.00),
(412, 112, 312, '2024-05-15', '2024-05-20', 'Mountain Lodge', 85.00),
(413, 113, 313, '2024-06-10', '2024-06-15', 'Standard', 65.00),
(414, 114, 314, '2024-07-01', '2024-07-06', 'Lake View', 110.00),
(415, 115, 315, '2024-08-12', '2024-08-17', 'Heritage View', 95.00);

-- Restaurant Table
INSERT INTO Restaurant (restaurantID, adminID, destinationID, name, street, city, cuisine, image_url) VALUES
(501, 1, 201, 'Cuckoo''s Den', 'Fort Road', 'Lahore', 'Pakistani BBQ', 'https://example.com/images/cuckoos_den.jpg'),
(502, 2, 202, 'Monal', 'Pir Sohawa Road', 'Islamabad', 'Pakistani/Continental', 'https://example.com/images/monal.jpg'),
(503, 3, 203, 'Andaaz', 'Fort Road', 'Lahore', 'Mughlai', 'https://example.com/images/andaaz.jpg'),
(504, 4, 204, 'Mohenjo Cafe', 'Mohenjo-Daro Site', 'Larkana', 'Local Sindhi', 'https://example.com/images/mohenjo_cafe.jpg'),
(505, 5, 205, 'Cafe de Hunza', 'Karimabad', 'Hunza', 'Local Fusion', 'https://example.com/images/cafe_de_hunza.jpg'),
(506, 6, 206, 'Cooco''s', 'G.T. Road', 'Lahore', 'Traditional Pakistani', 'https://example.com/images/coocos.jpg'),
(507, 7, 207, 'Concordia Kitchen', 'K2 Base Camp', 'Gilgit', 'High-Altitude Meals', 'https://example.com/images/concordia_kitchen.jpg'),
(508, 8, 208, 'Kolachi', 'Seaview', 'Karachi', 'Seafood', 'https://example.com/images/kolachi.jpg'),
(509, 9, 209, 'Desert Grill', 'Skardu Main Road', 'Skardu', 'BBQ', 'https://example.com/images/desert_grill.jpg'),
(510, 10, 210, 'Baltit Fort Cafe', 'Karimabad', 'Hunza', 'Traditional Hunza', 'https://example.com/images/baltit_fort_cafe.jpg'),
(511, 11, 211, 'Cholistan Tent', 'Derawar Fort', 'Bahawalpur', 'Desert Cuisine', 'https://example.com/images/cholistan_tent.jpg'),
(512, 12, 212, 'Lakeview Restaurant', 'Naran', 'Kaghan', 'Pakistani', 'https://example.com/images/lakeview_restaurant.jpg'),
(513, 13, 213, 'Thatta Food Street', 'Makli Road', 'Thatta', 'Sindhi', 'https://example.com/images/thatta_food_street.jpg'),
(514, 14, 214, 'Attabad Grill', 'Attabad Lake', 'Gojal', 'Freshwater Fish', 'https://example.com/images/attabad_grill.jpg'),
(515, 15, 215, 'Taxila Food Point', 'Taxila Museum Road', 'Taxila', 'Punjabi', 'https://example.com/images/taxila_food_point.jpg');
-- Reservation Table
INSERT INTO Reservation (reservationID, userID, restaurantID, reservationDate, reservationTime, numberOfGuests, tableNumber) VALUES
(601, 101, 501, '2023-06-02', '19:00:00', 4, 'Terrace 2'),
(602, 102, 502, '2023-07-12', '20:00:00', 6, 'Mountain View'),
(603, 103, 503, '2023-08-22', '18:30:00', 3, 'Rooftop 5'),
(604, 104, 504, '2023-09-07', '20:30:00', 5, 'Courtyard 1'),
(605, 105, 505, '2023-10-14', '19:30:00', 2, 'Valley View'),
(606, 106, 506, '2023-11-17', '19:00:00', 4, 'Garden 3'),
(607, 107, 507, '2023-12-03', '18:00:00', 3, 'Base Camp 2'),
(608, 108, 508, '2024-01-12', '21:00:00', 4, 'Seaside 4'),
(609, 109, 509, '2024-02-16', '20:00:00', 2, 'Dune 1'),
(610, 110, 510, '2024-03-22', '19:30:00', 5, 'Fort View'),
(611, 111, 511, '2024-04-07', '20:00:00', 3, 'Oasis 3'),
(612, 112, 512, '2024-05-17', '19:00:00', 4, 'Lakeside 2'),
(613, 113, 513, '2024-06-12', '20:30:00', 6, 'Heritage 5'),
(614, 114, 514, '2024-07-03', '19:00:00', 2, 'Lakeview 3'),
(615, 115, 515, '2024-08-14', '20:00:00', 4, 'Museum 1');

INSERT INTO Transportation (transportationID, destinationID, adminID, type, provider) VALUES
(701, 201, 1, 'Bus Rapid Transit', 'Punjab Metro'),
(702, 202, 2, 'Metro Bus', 'CDA'),
(703, 203, 3, 'Auto Rickshaw', 'Local Transport'),
(704, 204, 4, 'Minibus', 'Sindh Tourism'),
(705, 205, 5, '4x4 Jeep', 'Hunza Tours'),
(706, 206, 6, 'Tourist Bus', 'Punjab Tourism'),
(707, 207, 7, 'Off-road Jeep', 'Adventure Pakistan'),
(708, 208, 8, 'Train', 'Pakistan Railways'),
(709, 209, 9, '4x4 Jeep', 'Skardu Travels'),
(710, 210, 10, 'Minivan', 'Hunza Transport'),
(711, 211, 11, '4x4 Jeep', 'Bahawalpur Tourism'),
(712, 212, 12, 'Minibus', 'Kaghan Transport'),
(713, 213, 13, 'Minibus', 'Sindh Tourism'),
(714, 214, 14, 'Boat', 'Attabad Tours'),
(715, 215, 15, 'Auto Rickshaw', 'Taxila Transport');



-- Travel Table
INSERT INTO Travel (travelID, userID, transportationID, travelDate, departureTime, arrivalTime, fare, departurePoint, arrivalPoint) VALUES
(801, 101, 701, '2023-06-01', '08:30:00', '09:00:00', 0.50, 'Lahore Station', 'Badshahi Mosque'),
(802, 102, 702, '2023-07-10', '09:00:00', '09:30:00', 0.40, 'Blue Area', 'Faisal Mosque'),
(803, 103, 703, '2023-08-20', '08:00:00', '08:25:00', 0.60, 'Gaddafi Stadium', 'Lahore Fort'),
(804, 104, 704, '2023-09-05', '10:00:00', '12:30:00', 2.00, 'Larkana City', 'Mohenjo-Daro'),
(805, 105, 705, '2023-10-12', '11:00:00', '14:00:00', 15.00, 'Gilgit', 'Hunza Valley'),
(806, 106, 706, '2023-11-15', '06:00:00', '06:45:00', 1.00, 'Lahore Zoo', 'Shalimar Gardens'),
(807, 107, 707, '2023-12-01', '07:30:00', '10:00:00', 25.00, 'Skardu', 'K2 Base Camp'),
(808, 108, 708, '2024-01-10', '08:15:00', '08:45:00', 0.30, 'Karachi Station', 'Mazar-e-Quaid'),
(809, 109, 709, '2024-02-14', '09:30:00', '10:15:00', 5.00, 'Skardu City', 'Katpana Desert'),
(810, 110, 710, '2024-03-20', '07:00:00', '07:30:00', 1.50, 'Hunza Center', 'Baltit Fort'),
(811, 111, 711, '2024-04-05', '10:00:00', '12:00:00', 20.00, 'Bahawalpur', 'Derawar Fort'),
(812, 112, 712, '2024-05-15', '08:00:00', '10:30:00', 3.00, 'Mansehra', 'Ansoo Lake'),
(813, 113, 713, '2024-06-10', '14:00:00', '15:00:00', 1.20, 'Thatta City', 'Shah Jahan Mosque'),
(814, 114, 714, '2024-07-01', '09:00:00', '09:45:00', 5.00, 'Hunza', 'Attabad Lake'),
(815, 115, 715, '2024-08-12', '10:00:00', '10:20:00', 0.30, 'Taxila Station', 'Taxila Museum');

-- Review Table
INSERT INTO Review (reviewID, userID, destinationID, restaurantID, transportationID, hotelID, rating, comment, reviewType) VALUES
(901, 101, 201, NULL, NULL, NULL, 5, 'Magnificent Mughal architecture!', 'destination'),
(902, 102, NULL, 502, NULL, NULL, 4, 'Best views of Islamabad', 'restaurant'),
(903, 103, NULL, NULL, 703, NULL, 3, 'Authentic local experience', 'transportation'),
(904, 104, NULL, NULL, NULL, 304, 3, 'Basic but clean rooms', 'hotel'),
(905, 105, 205, NULL, NULL, NULL, 5, 'Heavenly mountain views', 'destination'),
(906, 106, NULL, 506, NULL, NULL, 4, 'Delicious traditional food', 'restaurant'),
(907, 107, NULL, NULL, 707, NULL, 5, 'Essential for K2 trek', 'transportation'),
(908, 108, NULL, NULL, NULL, 308, 4, 'Perfect sea breeze', 'hotel'),
(909, 109, 209, NULL, NULL, NULL, 4, 'Surreal desert experience', 'destination'),
(910, 110, NULL, 510, NULL, NULL, 5, 'Authentic Hunza cuisine', 'restaurant'),
(911, 111, NULL, NULL, 711, NULL, 4, 'Thrilling desert adventure', 'transportation'),
(912, 112, NULL, NULL, NULL, 312, 3, 'Cozy mountain stay', 'hotel'),
(913, 113, 213, NULL, NULL, NULL, 4, 'Historical gem', 'destination'),
(914, 114, NULL, 514, NULL, NULL, 5, 'Fresh trout with lake view', 'restaurant'),
(915, 115, NULL, NULL, 715, NULL, 3, 'Convenient local transport', 'transportation');


