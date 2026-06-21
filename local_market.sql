-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 22-05-2026 a las 21:01:57
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `local_market`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `alembic_version`
--

CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `categories`
--

CREATE TABLE `categories` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `description` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `categories`
--

INSERT INTO `categories` (`id`, `name`, `description`) VALUES
(1, 'Electrónica', 'Productos electrónicos como celulares, computadoras, etc.'),
(2, 'Ropa', 'Prendas de vestir para hombre, mujer y niños'),
(3, 'Hogar', 'Muebles, decoración y artículos para el hogar'),
(4, 'Deportes', 'Equipamiento deportivo y accesorios'),
(6, 'Juguetes', 'Juguetes y juegos para niños'),
(7, 'Cocina', 'Utensilios, electrodomésticos y accesorios de cocina');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `invoices`
--

CREATE TABLE `invoices` (
  `id` int(11) NOT NULL,
  `invoice_number` varchar(20) NOT NULL,
  `issue_date` datetime DEFAULT NULL,
  `pdf_path` varchar(255) DEFAULT NULL,
  `order_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `invoices`
--

INSERT INTO `invoices` (`id`, `invoice_number`, `issue_date`, `pdf_path`, `order_id`) VALUES
(1, 'FACT-20260407071303-', '2026-04-07 07:13:03', 'c:\\Users\\User\\Desktop\\Local_Market\\app\\static\\invoices\\factura_FACT-20260407071303-.pdf', 1),
(2, 'FACT-20260408092935-', '2026-04-08 09:29:35', 'c:\\Users\\User\\Desktop\\Local_Market\\app\\static\\invoices\\factura_FACT-20260408092935-.pdf', 2),
(3, 'FACT-20260408114511-', '2026-04-08 11:45:11', 'c:\\Users\\User\\Desktop\\Local_Market\\app\\static\\invoices\\factura_FACT-20260408114511-.pdf', 3),
(4, 'FACT-20260408124708-', '2026-04-08 12:47:08', 'c:\\Users\\User\\Desktop\\Local_Market\\app\\static\\invoices\\factura_FACT-20260408124708-.pdf', 4),
(5, 'FACT-20260408124750-', '2026-04-08 12:47:50', 'c:\\Users\\User\\Desktop\\Local_Market\\app\\static\\invoices\\factura_FACT-20260408124750-.pdf', 5),
(6, 'FACT-20260408125054-', '2026-04-08 12:50:54', 'c:\\Users\\User\\Desktop\\Local_Market\\app\\static\\invoices\\factura_FACT-20260408125054-.pdf', 6),
(7, 'FACT-20260408130339-', '2026-04-08 13:03:39', 'c:\\Users\\User\\Desktop\\Local_Market\\app\\static\\invoices\\factura_FACT-20260408130339-.pdf', 7),
(8, 'FACT-20260408131738-', '2026-04-08 13:17:38', 'c:\\Users\\User\\Desktop\\Local_Market\\app\\static\\invoices\\factura_FACT-20260408131738-.pdf', 8),
(9, 'FACT-20260408132400-', '2026-04-08 13:24:00', 'c:\\Users\\User\\Desktop\\Local_Market\\app\\static\\invoices\\factura_FACT-20260408132400-.pdf', 9),
(10, 'FACT-20260408132751-', '2026-04-08 13:27:51', 'c:\\Users\\User\\Desktop\\Local_Market\\app\\static\\invoices\\factura_FACT-20260408132751-.pdf', 10);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `orders`
--

CREATE TABLE `orders` (
  `id` int(11) NOT NULL,
  `order_date` datetime DEFAULT NULL,
  `status` enum('pendiente','completado','cancelado') DEFAULT NULL,
  `total` decimal(10,2) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `orders`
--

INSERT INTO `orders` (`id`, `order_date`, `status`, `total`, `user_id`) VALUES
(1, '2026-04-07 07:13:03', 'completado', 1000000.00, 1),
(2, '2026-04-08 09:29:35', 'completado', 499950.00, 1),
(3, '2026-04-08 11:45:11', 'completado', 2786500.00, 1),
(4, '2026-04-08 12:47:08', 'completado', 829900.00, 1),
(5, '2026-04-08 12:47:50', 'completado', 1167800.00, 1),
(6, '2026-04-08 12:50:54', 'completado', 2359800.00, 1),
(7, '2026-04-08 13:03:39', 'completado', 29530600.00, 1),
(8, '2026-04-08 13:17:38', 'completado', 14486700.00, 1),
(9, '2026-04-08 13:24:00', 'completado', 267700.00, 1),
(10, '2026-04-08 13:27:51', 'completado', 4229700.00, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `order_details`
--

CREATE TABLE `order_details` (
  `id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  `unit_price` decimal(10,2) NOT NULL,
  `subtotal` decimal(10,2) NOT NULL,
  `order_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `order_details`
--

INSERT INTO `order_details` (`id`, `quantity`, `unit_price`, `subtotal`, `order_id`, `product_id`) VALUES
(1, 1, 1000000.00, 1000000.00, 1, 1),
(2, 1, 499950.00, 499950.00, 2, 2),
(3, 1, 896950.00, 896950.00, 3, 1),
(4, 1, 139900.00, 139900.00, 3, 17),
(5, 1, 139900.00, 139900.00, 3, 19),
(6, 1, 499950.00, 499950.00, 3, 2),
(7, 1, 209900.00, 209900.00, 3, 23),
(8, 2, 449950.00, 899900.00, 3, 5),
(9, 1, 829900.00, 829900.00, 4, 44),
(10, 1, 148000.00, 148000.00, 5, 18),
(11, 1, 949900.00, 949900.00, 5, 46),
(12, 1, 69900.00, 69900.00, 5, 65),
(13, 1, 1409900.00, 1409900.00, 6, 45),
(14, 1, 949900.00, 949900.00, 6, 46),
(15, 4, 829900.00, 3319600.00, 7, 44),
(16, 2, 1409900.00, 2819800.00, 7, 45),
(17, 23, 949900.00, 21847700.00, 7, 46),
(18, 15, 102900.00, 1543500.00, 7, 49),
(19, 1, 1399000.00, 1399000.00, 8, 14),
(20, 3, 99900.00, 299700.00, 8, 21),
(21, 1, 279950.00, 279950.00, 8, 22),
(22, 1, 309900.00, 309900.00, 8, 24),
(23, 1, 139950.00, 139950.00, 8, 25),
(24, 3, 149900.00, 449700.00, 8, 26),
(25, 1, 449950.00, 449950.00, 8, 3),
(26, 1, 5899900.00, 5899900.00, 8, 32),
(27, 1, 249900.00, 249900.00, 8, 33),
(28, 1, 109900.00, 109900.00, 8, 34),
(29, 1, 139900.00, 139900.00, 8, 35),
(30, 1, 64900.00, 64900.00, 8, 39),
(31, 1, 549950.00, 549950.00, 8, 4),
(32, 1, 244900.00, 244900.00, 8, 40),
(33, 1, 184900.00, 184900.00, 8, 43),
(34, 1, 114900.00, 114900.00, 8, 48),
(35, 1, 169900.00, 169900.00, 8, 51),
(36, 1, 619900.00, 619900.00, 8, 56),
(37, 1, 429950.00, 429950.00, 8, 6),
(38, 1, 189900.00, 189900.00, 8, 60),
(39, 1, 69900.00, 69900.00, 8, 64),
(40, 1, 1989950.00, 1989950.00, 8, 67),
(41, 1, 129900.00, 129900.00, 8, 69),
(42, 1, 49900.00, 49900.00, 9, 47),
(43, 1, 114900.00, 114900.00, 9, 48),
(44, 1, 102900.00, 102900.00, 9, 49),
(45, 3, 1409900.00, 4229700.00, 10, 45);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `products`
--

CREATE TABLE `products` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` text DEFAULT NULL,
  `price` decimal(10,2) NOT NULL,
  `stock` int(11) DEFAULT NULL,
  `image_url` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `category_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `products`
--

INSERT INTO `products` (`id`, `name`, `description`, `price`, `stock`, `image_url`, `created_at`, `updated_at`, `user_id`, `category_id`) VALUES
(1, 'Tenis de Entrenamiento adidas', 'Zapatillas para correr', 896950.00, 5, 'https://assets.adidas.com/images/h_2000,f_auto,q_auto,fl_lossy,c_fill,g_auto/80416ef59f8a404898d4973b2a7d9d8e_9366/Tenis_de_entrenamiento_adidas_by_Stella_McCartney_DROPSET_4_Beige_KJ6183_01_00_standard.jpg', '2026-04-07 07:12:44', '2026-04-08 11:45:11', 2, 2),
(2, 'Tenis SUPERSTAR II', 'Zapatillas Adidas SUPERSTAR II\r\n', 499950.00, 9, 'https://assets.adidas.com/images/h_2000,f_auto,q_auto,fl_lossy,c_fill,g_auto/09134d2ebf7c4c8bb724252a8a9fe274_9366/Tenis_SUPERSTAR_II_Beige_IH9320_01_00_standard.jpg', '2026-04-08 08:00:41', '2026-04-08 11:45:11', 2, 2),
(3, 'Tenis TEKKIRA CUP', 'Zapatillas Adidas TEKKIRA CUP\r\n', 449950.00, 12, 'https://assets.adidas.com/images/h_2000,f_auto,q_auto,fl_lossy,c_fill,g_auto/b8a2e510163648ed8064a9b48d7ac331_9366/Tenis_TEKKIRA_CUP_Blanco_HQ5065_01_00_standard.jpg', '2026-04-08 08:01:34', '2026-04-08 13:17:38', 2, 2),
(4, 'TENIS ADISTAR CONTROL 5', 'Zapatillas Adidas ADISTAR CONTROL 5\r\n', 549950.00, 14, 'https://assets.adidas.com/images/h_2000,f_auto,q_auto,fl_lossy,c_fill,g_auto/63cd4022b6c8488eb278cbe0483fae05_9366/TENIS_ADISTAR_CONTROL_5_Negro_KI6150_01_00_standard.jpg', '2026-04-08 08:02:06', '2026-04-08 13:17:38', 2, 2),
(5, 'TENIS ADISTAR CONTROL 3', 'Zapatillas Adidas ADISTAR CONTROL 3\r\n', 449950.00, 17, 'https://assets.adidas.com/images/h_2000,f_auto,q_auto,fl_lossy,c_fill,g_auto/14fd418161ac4dc6a58602f4f7f18776_9366/TENIS_ADISTAR_CONTROL_3_Cafe_HQ2719_01_00_standard.jpg', '2026-04-08 08:02:55', '2026-04-08 11:45:11', 2, 2),
(6, 'Tenis Lightblaze', 'Zapatillas Adidas Lightblaze\r\n', 429950.00, 7, 'https://assets.adidas.com/images/h_2000,f_auto,q_auto,fl_lossy,c_fill,g_auto/528e4e7368b54d15a02fd99205536b41_9366/Tenis_Lightblaze_Beige_JH6962_HM1.jpg', '2026-04-08 08:03:24', '2026-04-08 13:17:38', 2, 2),
(7, 'Tenis Astrastar', 'Zapatillas Astrastar\r\n', 329950.00, 9, 'https://assets.adidas.com/images/h_2000,f_auto,q_auto,fl_lossy,c_fill,g_auto/99f8b82c8a9e4e42857e7efa17afe8ff_9366/Tenis_Astrastar_Negro_JP5938_HM1.jpg', '2026-04-08 08:03:49', '2026-04-08 08:03:49', 2, 2),
(8, 'TENIS ADISTAR XLG 2.0', 'Zapatillas Adidas ADISTAR XLG 2.0\r\n', 649950.00, 6, 'https://assets.adidas.com/images/h_2000,f_auto,q_auto,fl_lossy,c_fill,g_auto/6478fb39e74a489aad75638b10c690f0_9366/TENIS_ADISTAR_XLG_2.0_Blanco_HQ7468_01_00_standard.jpg', '2026-04-08 08:04:17', '2026-04-08 08:04:17', 2, 2),
(9, 'TENIS ADISTAR CONTROL 5', 'Zapatillas Adidas ADISTAR CONTROL 5\r\n', 549950.00, 7, 'https://assets.adidas.com/images/h_2000,f_auto,q_auto,fl_lossy,c_fill,g_auto/161b862051a6427a8fa3ac6a7555f0f5_9366/TENIS_ADISTAR_CONTROL_5_Negro_KI4204_01_00_standard.jpg', '2026-04-08 08:04:42', '2026-04-08 08:04:42', 2, 2),
(10, 'Tenis Terrex Agravic Speed Ultra', 'Zapatillas Adidas de trail running Terrex Agravic Speed Ultra\r\n', 899950.00, 8, 'https://assets.adidas.com/images/h_2000,f_auto,q_auto,fl_lossy,c_fill,g_auto/dc1a1128cd4f4f3f93417d449e2c7b88_9366/Tenis_de_trail_running_Terrex_Agravic_Speed_Ultra_Blanco_IH3764_HM1.jpg', '2026-04-08 08:33:58', '2026-04-08 08:33:58', 2, 2),
(11, 'Buzo UA Project Rock Disrupt Crew para Hombre', 'Buzo UA Project Rock Disrupt Crew para Hombre\r\n', 309900.00, 42, 'https://underarmourcol.vtexassets.com/arquivos/ids/553611-1365-2048?v=638356753441770000&width=1365&height=2048&aspect=true', '2026-04-08 08:48:07', '2026-04-08 08:48:07', 4, 2),
(12, 'PANTALON STRAIGHT FIT PIEL ANTE', 'Pantalón straight fit confeccionado en piel con acabado ante. Cinco bolsillos. Cierre frontal con cremallera y botón.\r\n', 139900.00, 6, 'https://static.zara.net/assets/public/5774/6f7f/51f7471e84ad/c1e75643fafd/04416407716-200-p/04416407716-200-p.jpg?ts=1770830307413&w=750', '2026-04-08 08:48:40', '2026-04-08 08:48:40', 4, 2),
(13, 'CAZADORA TÉCNICA REGULAR FIT', 'Cazadora regular fit confeccionada en tejido técnico. Cuello subido con cierre de botones. Manga larga. Bolsillos de doble vivo en cadera. Detalle de bolsillos interiores. Acabados con elástico. Cierre frontal con cremallera.\r\n', 499000.00, 8, 'https://static.zara.net/assets/public/adda/57a5/db3b45ed8d84/81734d53a788/02634221711-p/02634221711-p.jpg?ts=1773074285434&w=750', '2026-04-08 08:49:00', '2026-04-08 08:49:00', 4, 2),
(14, 'SOBRECAMISA REGULAR FIT PIEL ANTE', 'Sobrecamisa regular fit confeccionada en piel con acabdao ante. Cuello solapa y manga larga acabada en puño con botón. Bolsillos laterales ocultos en costura. Cierre frontal de botonadura oculta por solapa.\r\n', 1399000.00, 9, 'https://static.zara.net/assets/public/5a2f/0d9f/780248cfaae6/7b51c499cf09/04416502705-p/04416502705-p.jpg?ts=1773403213179&w=750', '2026-04-08 08:49:15', '2026-04-08 13:17:38', 4, 2),
(15, 'JEANS STRAIGHT ANKLE FIT', 'Pierna recta desde la cadera hasta el tobillo, con un ajuste que no se estrecha ni se ensancha. Tiro medio. Tejido rígido.\r\n', 329000.00, 9, 'https://static.zara.net/assets/public/3792/20c4/c9ee4e648aad/8ca78d55e4c8/05585421916-p/05585421916-p.jpg?ts=1771590092299&w=750', '2026-04-08 08:49:34', '2026-04-08 08:49:34', 4, 2),
(16, 'CAMISETA BOXY FIT LAVADA', 'Camiseta boxy fit. Cuello redondo y manga corta. Acabados irregulares. Efecto lavado.\r\n', 399950.00, 7, 'https://static.zara.net/assets/public/34b5/a44b/564a4d4cade3/d56a73cc135d/00526440811-p/00526440811-p.jpg?ts=1772032117562&w=750', '2026-04-08 08:50:04', '2026-04-08 08:50:16', 4, 2),
(17, 'BOXER SOFT PACK 3', 'Pack de tres calzoncillos tipo bóxer confeccionados en tejido elástico con acabado aterciopelado. Cintura elástica.\r\n', 139900.00, 10, 'https://static.zara.net/assets/public/144c/a0e8/9bcf4ac092a0/0f73563874e1/04442402555-e1/04442402555-e1.jpg?ts=1764684054275&w=750', '2026-04-08 08:50:36', '2026-04-08 11:45:11', 4, 2),
(18, 'BAÑADOR LARGO RAYAS', 'Bañador confeccionado en tejido técnico. Cintura elástica ajustable con cordón. Bolsillos frontales y detalle de bolsillo trasero de vivo. Forro interior.\r\n', 148000.00, 2, 'https://static.zara.net/assets/public/28e6/ce42/d9f245f09ce3/e85e02d97b86/08574429330-e1/08574429330-e1.jpg?ts=1774280840835&w=750', '2026-04-08 08:50:51', '2026-04-08 12:47:50', 4, 2),
(19, 'SANDALIA TIRAS', 'Sandalia fabricada en goma. Cuenta con dos tiras en el empeine que facilita el confort durante su uso. Suela plana.\r\n', 139900.00, 87, 'https://static.zara.net/assets/public/c516/ed31/cbab428ca37c/c09b4e7d73be/12796720202-a2/12796720202-a2.jpg?ts=1773399074630&w=750', '2026-04-08 08:51:06', '2026-04-08 11:45:11', 4, 2),
(20, 'GORRA VISOR PLANO BORDADO', 'Gorra con visera confeccionada en tejido de algod贸n. Bordado combinado a contraste en delantero. Ajuste en la parte posterior.\r\n', 109900.00, 45, 'https://static.zara.net/assets/public/aa00/5007/7e9940a98e2a/f11c524d2d95/03920554700-a1/03920554700-a1.jpg?ts=1770914492453&w=750', '2026-04-08 08:51:23', '2026-04-08 08:51:23', 4, 2),
(21, 'Pista de carerras bucle con 2 vehículos', 'Deja que tus hijos disfruten de las carreras más apasionantes con la variedad de pistas para autos. En ellas podrás competir contra otros carros, dar giros de 360°, correr por óvalos y circuitos, y más.\r\n', 99900.00, 5, 'https://panamericana.vtexassets.com/arquivos/ids/627635-1200-auto?v=639003769973670000&width=1200&height=auto&aspect=true', '2026-04-08 09:25:20', '2026-04-08 13:17:38', 5, 6),
(22, 'Set de estacionamiento de avi贸n con accesorios', 'Deja que tus hijos disfruten con la variedad de set y juguetes de Toys Store.\r\n', 279950.00, 8, 'https://panamericana.vtexassets.com/arquivos/ids/558984-800-auto?v=638646888000730000&width=800&height=auto&aspect=true', '2026-04-08 09:25:37', '2026-04-08 13:17:38', 5, 6),
(23, 'Dinosaurio triceratops con control, luz, sonido y vapor verde', 'Dinosaurio triceratops Características: -Color: verde/negro -Con luz, sonido y vapor -El dinosaurio lanza vapor por la boca, cuando su boca esta cerrada el vapor saldrá por la nariz -El dinosaurio requiere 1 batería de litio de 3.7V (incluida) -El control requiere 3 baterías AAA (no incluidas)\r\n', 209900.00, 8, 'https://panamericana.vtexassets.com/arquivos/ids/514909-800-auto?v=638325412132500000&width=800&height=auto&aspect=true', '2026-04-08 09:26:04', '2026-04-08 11:45:11', 5, 6),
(24, 'Lanzador Blazter con 20 dardos, silenciador y mira', 'Encuentradivertidos lanzadores de agua o de dardos para que niños y niñas disfruten compitiendo o lanzándose objetos. Características • Incluye 20 dardos • Con mira y silenciador • Requiere 4 baterías \"AA\" (no incluidas) • Dimensiones del producto: 35 x 76 x 6 cm\r\n', 309900.00, 8, 'https://panamericana.vtexassets.com/arquivos/ids/616993-800-auto?v=638957053034800000&width=800&height=auto&aspect=true', '2026-04-08 09:26:23', '2026-04-08 13:17:38', 5, 6),
(25, 'Lanzador Blazter con 40 dardos y silenciador', 'Encuentra divertidos lanzadores de agua o de dardos para que niños y niñas disfruten compitiendo o lanzándose objetos. Características • 40 unidades • Color: amarillo • Requiere 6 baterías \"AA\" (no incluidas)\r\n', 139950.00, 14, 'https://panamericana.vtexassets.com/arquivos/ids/620138-800-auto?v=638972678955500000&width=800&height=auto&aspect=true', '2026-04-08 09:26:39', '2026-04-08 13:17:38', 5, 6),
(26, 'Trompo beyblade x kits inciales cx (surtido)', '¡Vive la emoción de Beyblade X, la próxima generación de arenas, lanzadores y tops Beyblade! Los kits iniciales CX de Beyblade X incluyen 1 lanzador y 1 top (Requiere Beystadium, se vende por separado). Lánzate a la batalla o reconfigura el top intercambiando la hoja, el trinquete y el piñón del top con los de otros tops Beyblade X (se venden por separado) para crear tu propio e imbatible top. ¡Los tops CX están diseñados con una hoja que se separa en 3 piezas para aún más opciones de personalización! Beyblade X cuenta con el sistema Acelerador X: el engranaje de un top Beyblade X entra en contacto con el riel de la arena Beystadium, propulsando el top a velocidades extremas alrededor de la arena para generar impresionantes choques y épicas explosiones. Lanza tus tops a feroces batallas contra los tops de tus oponentes y anota puntos en cada confrontación. El primero en acumular 4 puntos será el ganador. Los juguetes Beyblade de Hasbro con auténticas partes de metal fundido son excelentes regalos para niños y niñas a partir de 8 años.\r\n', 149900.00, 3, 'https://panamericana.vtexassets.com/arquivos/ids/646861-800-auto?v=639088423635500000&width=800&height=auto&aspect=true', '2026-04-08 09:26:53', '2026-04-08 13:17:38', 5, 6),
(27, 'Lanzador de burbujas dino con luz y sonido (surtido)', 'Lanzador de burbujas dino con luz y sonido (surtido) Características: • Con luz y sonido • Requiere 3 baterías AA (no incluidas) • Incluye 2 botellas de liquido para hacer burbujas\r\n', 49900.00, 12, 'https://panamericana.vtexassets.com/arquivos/ids/568371-800-auto?v=638690945811200000&width=800&height=auto&aspect=true', '2026-04-08 09:27:11', '2026-04-08 09:27:11', 5, 6),
(28, 'Set para tinturar tela', 'Set para tinturar tela Características: \r\n• 5 colore de Pigmentos Tie-Dye \r\n• Bandas de goma \r\n• Bolsas y guantes plásticos\r\n', 89900.00, 6, 'https://panamericana.vtexassets.com/arquivos/ids/547400-800-auto?v=638576202043000000&width=800&height=auto&aspect=true', '2026-04-08 09:27:34', '2026-04-08 09:27:34', 5, 6),
(29, 'Perro con movimiento, sonido y accesorios x 3 piezas', '• Con collar y accesorios x 3 piezas\r\n', 59900.00, 2, 'https://panamericana.vtexassets.com/arquivos/ids/623598-800-800?v=638990696009770000&width=800&height=800&aspect=true', '2026-04-08 09:27:51', '2026-04-08 09:27:51', 5, 6),
(30, 'Tiranosaurio de 55 cm con control y sonido', 'Haz felices a tus hijos y permíteles disfrutar al máximo sus tiempos de entretenimiento con la variedad de juegos y juguetes disponibles: peluches, muñecas, figuras de acción, piscinas de pelotas, juegos de rol, Juegos didácticos, vehículos y más.\r\n', 139950.00, 8, 'https://panamericana.vtexassets.com/arquivos/ids/620275-800-auto?v=638972797856970000&width=800&height=auto&aspect=true', '2026-04-08 09:30:16', '2026-04-08 09:30:16', 5, 6),
(31, 'Grifería Lavaplatos Monocontrol Iris Negro Flexible Sensi Dacqua', 'Dale un toque moderno y funcional a tu cocina con la Grifería Lavaplatos Monocontrol Iris Negro Flexible Sensi Dacqua. Su diseño elegante en negro mate y su flexibilidad te brindarán comodidad y estilo en cada uso.\r\n', 149900.00, 5, 'https://media.falabella.com/sodimacCO/898557/w=1036,h=832,f=webp,fit=contain,q=85', '2026-04-08 09:45:47', '2026-04-08 09:45:47', 6, 7),
(32, 'Cocina Integral 1.80 Metros Lioni Plomo+Fresno/Europeo Incluye Meson sin Quemadores Just Home Collec', 'Cocina Integral 1.80 Metros Lioni Plomo+Fresno/Europeo Incluye Mesón sin Quemadores Just Home Collection\r\n', 5899900.00, 0, 'https://media.falabella.com/sodimacCO/796733/w=360,h=360,f=webp,fit=contain,q=85', '2026-04-08 09:46:12', '2026-04-08 13:17:38', 6, 7),
(33, 'Juego de Utensilios de Cocina 28 Piezas en Acero y Silicona con Soporte', '¡Dale un toque de elegancia y funcionalidad a tu cocina con el Juego de Utensilios de Cocina de 28 Piezas! Este set NCUE es perfecto para cualquier amante de la cocina, desde principiantes hasta expertos. Con este juego, prepararás, servirás y hornearás con estilo y comodidad, gracias a sus utensilios de silicona y acero inoxidable.\r\n', 249900.00, 5, 'https://media.falabella.com/sodimacCO/3023892/w=360,h=360,f=webp,fit=contain,q=85', '2026-04-08 09:46:28', '2026-04-08 13:17:38', 6, 7),
(34, 'Maquina para Hacer Pastas Ravioles Raf Manual Acero Inoxidable', 'Maquina para Hacer Pastas Ravioles Raf Manual Acero Inoxidable - 52 Bits - 3048667\r\n', 109900.00, 7, 'https://media.falabella.com/sodimacCO/3048667/w=360,h=360,f=webp,fit=contain,q=85', '2026-04-08 09:46:44', '2026-04-08 13:17:38', 6, 7),
(35, 'Set x 8 Ramekin Surtidos Red Rectovalado', '¡Dale un toque especial a tus creaciones culinarias con el Set x 8 Ramekin Surtidos Red Rectovalado! Este set de mini ramekines de cerámica, con su diseño clásico y colores surtidos, es perfecto para presentar tus platillos de manera elegante y original. Ideales para hornear porciones individuales, estos ramekines son el complemento perfecto para cualquier cocina\r\n', 139900.00, 7, 'https://media.falabella.com/sodimacCO/3028745_02/w=1160', '2026-04-08 09:47:07', '2026-04-08 13:17:38', 6, 7),
(36, 'Cuchillo/Cepillo Quita Escamas Pescados', 'Cuchillo/Cepillo Quita Escamas Pescados\r\n', 33900.00, 45, 'https://media.falabella.com/sodimacCO/636967/w=360,h=360,f=webp,fit=contain,q=85', '2026-04-08 09:47:23', '2026-04-08 09:47:23', 6, 7),
(37, 'Olla con Asas 20 cm 4.5 Litros Espesor 1.8 mm Paris Roja', 'Sin dudas, las comidas serán abundantes con la olla alta Tramontina Paris en aluminio con revestimiento interno y externo antiadherente Starflon Max rojo con tapa de vidrio 20 centímetros 4,2 litros. Está fabricada en aluminio de 1,8 milímetros de espesor y cuenta con revestimiento interno y externo con antiadherente Starflon Max. Gracias a estas características, proporciona una cocción rápida y uniforme de los alimentos, evita que se peguen en la superficie y también es muy fácil de limpiar. Sus asas son de baquelita antitérmica y el agarrador de su tapa de vidrio templado es de nylon, ambos materiales son antitérmicos y no se calientan. ¡La olla alta, además de presentar todas estas características, es apta para lavavajillas, lo que facilita su rutina diaria!\r\n', 174900.00, 15, 'https://media.falabella.com/sodimacCO/312260/w=360,h=360,f=webp,fit=contain,q=85', '2026-04-08 09:47:37', '2026-04-08 09:47:37', 6, 7),
(38, 'Olla Antiadherente con Tapa 20x8.0cm 2.3 Litros Acero Inoxidable Inducción Midnight Blue Libre de PF', 'Midnight blue es un atributo a la magia de la noche, a esos momentos en los que el cielo se tiñe de azul profundo y las estrellas comienzan a brillar. Es como invitar la serenidad de la noche a tu cocina, en donde la elegancia te envuelve y te conecta con la tranquilidad. Evoca la quietud de la noche y la dimensión del océano, se convierte en un símbolo de lujo discreto en una declaración de buen gusto. Con el disfrute consciente de cada momento transforma lo cotidiano en extraordinario.\r\n', 194900.00, 16, 'https://media.falabella.com/sodimacCO/768895/w=360,h=360,f=webp,fit=contain,q=85', '2026-04-08 09:48:05', '2026-04-08 09:48:05', 6, 7),
(39, 'Chocolatera Acero Inoxidable 13.5cm 1 Litro Home Elements', 'Chocolatera Acero Inoxidable 13.5cm 1 Litro Home Elements - Home Elements - 794178\r\n', 64900.00, 17, 'https://media.falabella.com/sodimacCO/794178/w=360,h=360,f=webp,fit=contain,q=85', '2026-04-08 09:48:21', '2026-04-08 13:17:38', 6, 7),
(40, 'Olla Honda 20Cm Tapa De Vidrio 3.10Lt Allegra', 'comida más sana, por ser de acero inoxidable, la cacerola tramontina no libera ningún tipo de residuo en sus recetas, fácil de usar, una cacerola práctica para todas sus recetas y que se luce en cualquier tipo de cocina, a gas, eléctrica, vitrocerámica y de inducción, tapa de vidrio con salida de vapor y encaje perfecto, más durable: el acero inoxidable tramontina es una materia prima noble, resistente y que se luce por mucho más tiempo en la cocina, ahorrar tiempo y energía: el secreto está en el fondo triple (acero inoxidable + aluminio + acero inoxidable)\r\n', 244900.00, 25, 'https://media.falabella.com/sodimacCO/476993/w=360,h=360,f=webp,fit=contain,q=85', '2026-04-08 09:48:37', '2026-04-08 13:17:38', 6, 7),
(41, 'https://media.falabella.com/sodimacCO/476993/w=360,h=360,f=webp,fit=contain,q=85', 'Disfruta de la eficiencia y el estilo con el Jarro Hervidor de 12 cm de Pedrini. Fabricado en material antiadherente, este hervidor es ideal para calentar líquidos rápidamente. Su diseño compacto y funcional es perfecto para cualquier cocina, proporcionando comodidad y facilidad de uso. Ideal para el hogar, garantiza durabilidad y rendimiento.\r\n', 74900.00, 165, 'https://media.falabella.com/sodimacCO/545124/w=360,h=360,f=webp,fit=contain,q=85', '2026-04-08 09:48:53', '2026-04-08 09:48:53', 6, 7),
(42, 'Maquina Corta Pelo Afeitar Patillera Recargable Cabello Gm6613', 'Maquina Corta Pelo Afeitar Patillera Recargable Cabello Gm6613\r\n', 119900.00, 15, 'https://media.falabella.com/sodimacCO/762577/w=1036,h=832,f=webp,fit=contain,q=85', '2026-04-08 11:08:44', '2026-04-08 11:08:44', 7, 1),
(43, 'Maquina de Afeitar Razurar Shaver Vgr Recargable Inalambrica', 'Esta máquina de afeitar cuenta con una potencia nominal de 5 W, asegurando un rendimiento óptimo. Su modelo V-352 está pensado para ofrecerte un afeitado preciso y confortable. Además, su diseño recargable te da la libertad de usarla sin cables, facilitando su manejo y transporte.\r\n', 184900.00, 25, 'https://media.falabella.com/sodimacCO/794040/w=1036,h=832,f=webp,fit=contain,q=85', '2026-04-08 11:08:59', '2026-04-08 13:17:38', 7, 1),
(44, 'Aspiradora Eléctrica 20L Inox. + Hidrolavadora 1200 Watts', 'Esta hidrolavadora de alta presión, con una potencia de 1200 W, es ideal para uso profesional. Su caudal máximo es de 372 l/h y su presión máxima alcanza los 1300 psi. Además, cuenta con un filtro integrado y un sistema de acoplamiento rápido modular para facilitar su uso. Incluye una aspiradora seco con una capacidad de 30 Litros.\r\n', 829900.00, 21, 'https://media.falabella.com/sodimacCO/3010812/w=1036,h=832,f=webp,fit=contain,q=85', '2026-04-08 11:09:16', '2026-04-08 13:03:39', 7, 1),
(45, 'Aspiradora Robot y Trapeador con Base de Autovaciado sin Bolsa', 'Este robot aspirador y trapeador cuenta con una potente succión de 8000 Pa y un cepillo en V antienredos, ideal para hogares con mascotas. Su navegación LiDAR con sensores duales y visión nocturna aseguran una limpieza precisa, incluso en condiciones de poca luz. Además, su autonomía de hasta 180 minutos y control a través de app, voz y botones te brindan la flexibilidad que necesitas.\r\n', 1409900.00, 0, 'https://media.falabella.com/sodimacCO/3017744/w=1036,h=832,f=webp,fit=contain,q=85', '2026-04-08 11:09:30', '2026-04-08 13:27:51', 7, 1),
(46, 'Aspiradora Inalámbrica T-Fal X-FORCE FLEX 9.60, 250 Watts, Batería 45min, Accesorio Mascota', 'Alta potencia de succión y su ajuste automático de la potencia según el tipo de superficie, Elimina con gran facilidad los pelos de tu mascota gracias a que cuenta con animal Kit, Duración de batería hasta 45 min, Cuenta con posibilidad de trapear superficies gracias a que se le puede instalar el accesorio aqua head, Cuenta con 3 niveles de potencia: ECO - AUTO- BOOST\r\n', 949900.00, 20, 'https://media.falabella.com/sodimacCO/730879/w=1036,h=832,f=webp,fit=contain,q=85', '2026-04-08 11:09:51', '2026-04-08 13:03:39', 7, 1),
(47, 'Cortapicos 130V 1 Salida 10Amp Electrodoméstico Nicoma', 'Cortapicos 130V 1 Salida 10Amp Electrodomestico Nicoma | Halux | Electricidad\r\n', 49900.00, 684, 'https://media.falabella.com/sodimacCO/209667/w=1036,h=832,f=webp,fit=contain,q=85', '2026-04-08 11:10:07', '2026-04-08 13:24:00', 7, 1),
(48, 'Kit Protector Voltaje Homepro (Regulador) + Multitoma Multipro 120Vac/15A (1800W) Powest', 'Protege tus equipos electrónicos con el Kit Protector de Voltaje Homepro, que incluye un regulador de 1000VA/600W y una multitoma Multipro. Este kit es ideal para proteger tus equipos de cómputo y periféricos, así como tu centro de entretenimiento. ¡No esperes más y asegura la vida útil de tus dispositivos!\r\n', 114900.00, 54, 'https://media.falabella.com/sodimacCO/344273/w=1036,h=832,f=webp,fit=contain,q=85', '2026-04-08 11:10:26', '2026-04-08 13:24:00', 7, 1),
(49, 'Cable UTP Aps-UTP6al-100ext Assis', 'Cable UTP Aps-UTP6al-100ext Assis\r\n', 102900.00, 9, 'https://media.falabella.com/sodimacCO/732993/w=1036,h=832,f=webp,fit=contain,q=85', '2026-04-08 11:10:41', '2026-04-08 13:24:00', 7, 1),
(50, 'Linterna Recargable Alcance 150m Iluminacion Lateral', 'Ilumina tus noches de aventura con la Linterna Recargable de SODIMAC. Con un alcance de hasta 150 metros y una potente luz LED, esta linterna es perfecta para cualquier situación. Su diseño compacto y cuerpo resistente la hacen ideal para seguridad, camping o uso profesional. ¡Prepárate para la oscuridad!\r\n', 59900.00, 20, 'https://media.falabella.com/sodimacCO/3030431/w=1036,h=832,f=webp,fit=contain,q=85', '2026-04-08 11:10:56', '2026-04-08 11:10:56', 7, 1),
(51, 'Linterna De Trabajo Con Panel Solar Alcance 200 M', 'Linterna de trabajo con panel solar alcance 200 m\r\n', 169900.00, 14, 'https://media.falabella.com/sodimacCO/728967/w=1036,h=832,f=webp,fit=contain,q=85', '2026-04-08 11:11:12', '2026-04-08 13:17:38', 7, 1),
(52, 'Colgante 3 Luces Jaula Octagonal Luz & Ambiente', 'Ilumina tus espacios con la Lámpara Colgante 3 Luces Jaula Octagonal Luz & Ambiente, un elemento decorativo que fusiona el estilo Boho Chic con la funcionalidad. Con un diseño que evoca la calidez y el encanto, esta lámpara es perfecta para crear ambientes acogedores y llenos de personalidad.\r\n', 329900.00, 26, 'https://media.falabella.com/sodimacCO/637319/w=1036,h=832,f=webp,fit=contain,q=85', '2026-04-08 11:24:57', '2026-04-08 11:24:57', 8, 3),
(53, 'Lámpara Colgante Cubos Rat 3 Luces E27 Just Home Collection', 'Ilumina tus espacios con la Lámpara Colgante Cubos Rat 3 Luces E27 Just Home Collection. Con su diseño Urbano Industrial y su color café/marrón, esta lámpara colgante es perfecta para darle un toque moderno y acogedor a cualquier ambiente. Sus tres luces y su rosca E27 te permitirán crear la atmósfera ideal para tus momentos especiales.\r\n', 399900.00, 10, 'https://media.falabella.com/sodimacCO/881781_03/w=1036,h=832,f=webp,fit=contain,q=85', '2026-04-08 11:25:14', '2026-04-08 11:25:14', 8, 3),
(54, 'Espejo Vestidor 120x30 cm Color Surtido', '¡Dale un toque de elegancia a tu hogar con el Espejo Vestidor 120x30 cm Color Surtido! Este espejo rectangular, con un diseño industrial y moderno, es perfecto para cualquier espacio. Imagina combinar tus espacios con un diseño vanguardista, simple y moderno. ¡No esperes más para transformar tus espacios!\r\n', 24900.00, 15, 'https://media.falabella.com/sodimacCO/252013_05/w=1036,h=832,f=webp,fit=contain,q=85', '2026-04-08 11:25:28', '2026-04-08 11:25:28', 8, 3),
(55, 'Lámpara Pie Sophie 1 Luz E27 Blanco Casa Bonita', 'Esta lámpara de pie cuenta con un tipo de encendido por cable interruptor y un voltaje de 110 V. Su diseño incluye un diámetro de 23 cm y un largo de cable de 160 cm, lo que facilita su ubicación y uso. Fabricada en acero, ofrece durabilidad y un toque contemporáneo a tu decoración. Es de tipo piso y requiere uso exclusivo en interiores.\r\n', 69900.00, 10, 'https://media.falabella.com/sodimacCO/872587_02/w=1160', '2026-04-08 11:25:42', '2026-04-08 11:25:42', 8, 3),
(56, 'Sofá Cama 3 Puestos Bonnie 182x84x84 cm Negro', '¡Descubre el Sofá Cama Bonnie, el aliado perfecto para tu hogar! Con sus 182 cm de ancho, este sofá ofrece comodidad y estilo en un solo mueble. Su diseño nórdico y color negro lo convierten en una pieza versátil que se adapta a cualquier espacio. ¡Transforma tu sala en un oasis de confort con el Sofá Cama Bonnie!\r\n', 619900.00, 11, 'https://media.falabella.com/sodimacCO/885683/w=1036,h=832,f=webp,fit=contain,q=85', '2026-04-08 11:26:02', '2026-04-08 13:17:38', 8, 3),
(57, 'Combo Colchon Romance relax Navidad 100 + Almohada + Aromaterapia', '¡Descansa como nunca con el Combo Colchón Romance Relax Navidad! Este colchón, con su Pillow Top y 35 cm de altura, te brindará noches de sueño profundo. Incluye una almohada y un spray de linos para una experiencia de descanso completa. ¡Prepárate para despertar renovado!\r\n', 1579900.00, 20, 'https://media.falabella.com/sodimacCO/3042309/w=1036,h=832,f=webp,fit=contain,q=85', '2026-04-08 11:26:17', '2026-04-08 11:26:17', 8, 3),
(58, 'Escritorio 120 Vilna Rovere+Blanco 120x120x45cm', 'El Escritorio 120 Vilna Rovere+Blanco es la solución perfecta para tu espacio de trabajo. Con su diseño moderno y combinación de colores, este escritorio no solo es funcional, sino también estéticamente atractivo. Sus dimensiones de 120 x 120 x 45 cm lo hacen ideal para cualquier ambiente, ofreciendo una amplia superficie para trabajar y estudiar.\r\n', 249900.00, 2, 'https://media.falabella.com/sodimacCO/437380/w=1036,h=832,f=webp,fit=contain,q=85', '2026-04-08 11:26:31', '2026-04-08 11:26:31', 8, 3),
(59, 'Silla de Escritorio Matrix Gamer Giratoria Masajeadora Reposapiés 53,5x129x64 cm Azul/Negro Just Hom', 'Dale a tu espacio de juego un toque de comodidad y estilo con la Silla Gamer Masajeadora Matrix en color negro. Disfruta de horas de juego sin sacrificar la comodidad gracias a su diseño ergonómico y materiales de alta calidad. Relájate con la tranquilidad de una garantía de 12 meses y experimenta la diferencia de una silla gamer que se adapta a tus necesidades.\r\n', 699900.00, 25, 'https://media.falabella.com/sodimacCO/905765/w=1036,h=832,f=webp,fit=contain,q=85', '2026-04-08 11:26:45', '2026-04-08 11:26:45', 8, 3),
(60, 'Silla Reclinable 1 Puesto Atlanta 91x101x94 cm Negro', 'Relajate y disfruta de la comodidad que te ofrece el Sillón Reclinable 1 Cuerpo Calentador Masajeador Atlanta. Su diseño ejecutivo urbano en color negro te brindará un toque de elegancia a tu hogar. Con su función de masaje y calor, podrás aliviar el estrés del día a día y disfrutar de momentos únicos de descanso. ¡No esperes más para consentirte!\r\n', 189900.00, 5, 'https://media.falabella.com/sodimacCO/899330/w=1036,h=832,f=webp,fit=contain,q=85', '2026-04-08 11:26:58', '2026-04-08 13:17:38', 8, 3),
(61, 'Juego de Comedor Brasilia 4 Puestos Wengue', 'El Juego de comedor tubo de la marca Just Home Collection, es perfecto para situar en ambientes de espacio reducido, también puede ser de gran uso como comedor de diario en tu cocina. Este Juego cuenta con 4 sillas, su estructura es de metal lo cual hacen de este comedor muy firme y resistente, y la base de las sillas son de madera color chocolate. Sus dimensiones son de 76 cm de ancho por 70 cm de alto y 110 cm de largo.\r\n', 369900.00, 8, 'https://media.falabella.com/sodimacCO/281065/w=1036,h=832,f=webp,fit=contain,q=85', '2026-04-08 11:27:13', '2026-04-08 11:27:13', 8, 3),
(62, 'PATIN BELLONI PLUS GW', 'Descubre la emoción del patinaje con el Patín Recreativo Belloni Plus de GW, diseñado para ofrecerte una experiencia de deslizamiento inigualable. Perfecto para patinadores de todos los niveles, este patín combina tecnología avanzada, comodidad y estilo para que puedas disfrutar de cada movimiento con confianza y facilidad. Nuestros patines son de horma ajustada.\r\n', 299900.00, 15, 'https://atlanta-deportes.com.co/wp-content/uploads/2025/09/0129666-PATIN-BELLONI-PLUS-GW.jpg', '2026-04-08 11:36:29', '2026-04-08 11:36:29', 9, 4),
(63, 'TABLA DE SKATE COUGAR', 'La Tabla B01 de Cougar viene con un madero con 9 capas de fibra de pino, chasis en aluminio de 5″ y ruedas de 53×32/53x35mm PU.\r\n', 189900.00, 6, 'https://atlanta-deportes.com.co/wp-content/uploads/2025/06/0114616-TABLA-DE-SKATE-COUGAR.jpg', '2026-04-08 11:36:43', '2026-04-08 11:36:43', 9, 4),
(64, 'KIT DE PROTECCION DE PATINAJE GW', 'El kit de protección de patinaje te protege tus aventuras sobre ruedas con nuestro kit de protección de patinaje, diseñado para garantizar tu seguridad . El kit es la elección perfecta para patinadores de todos los niveles.\r\n', 69900.00, 6, 'https://atlanta-deportes.com.co/wp-content/uploads/2025/06/0112495-KIT-DE-PROTECCION-DE-PATINAJE-GW.jpg', '2026-04-08 11:36:56', '2026-04-08 13:17:38', 9, 4),
(65, 'BALON VOLEIBOL LAMINADO SCORE', 'El balon de voleybol laminado Score es MICROPERFORADO, tiene una superficie con textura que absorbe significativamente la energía del impacto\r\n', 69900.00, 22, 'https://atlanta-deportes.com.co/wp-content/uploads/2025/08/0121095-BALON-VOLEIBOL-LAMINADO-SCORE.jpg', '2026-04-08 11:37:16', '2026-04-08 12:47:50', 9, 4),
(66, 'CODERA MULTIUSOS BLISTER MIYAGI', 'La codera Multiusos de Miyagi es preformada, muy cómoda y viene en diferentes tallas. Ref. M7302\r\n', 44900.00, 48, 'https://atlanta-deportes.com.co/wp-content/uploads/2025/06/0110913-CODERA-MULTIUSOS-BLISTER-MIYAGI.jpg', '2026-04-08 11:37:32', '2026-04-08 11:37:32', 9, 4),
(67, 'ELIPTICA NORWICH K8722H SPORTFITNESS', 'La elípticas Norwich K8722H de Sportfitness es ideal para tu entrenamiento cardiovascular. Algunos de los beneficios de las maquinas elípticas es la ausencia de impacto en las articulaciones, fortalecimiento de músculos, quema de calorías y prevención de enfermedades. La Elíptica Norwich Sportfitness tiene la ventaja de tener 15 niveles de resistencia para una gran variedad de entrenamientos.\r\n', 1989950.00, 7, 'https://atlanta-deportes.com.co/wp-content/uploads/2025/06/0126387-ELIPTICA-NORWICH-K8722H-SPORTFITNESS.jpg', '2026-04-08 11:37:45', '2026-04-08 13:17:38', 9, 4),
(68, 'GRIP PARA MANOS AJUSTABLE SPORTFITNESS', 'El grip para mano ajustable de SportFitness esta diseñado para fortalecer los músculos de la mano y antebrazo.\r\n', 45900.00, 74, 'https://atlanta-deportes.com.co/wp-content/uploads/2025/06/0111436-GRIP-PARA-MANOS-AJUSTABLE-SPORTFITNESS.jpg', '2026-04-08 11:38:02', '2026-04-08 11:38:02', 9, 4),
(69, 'CINTURON LUMBAR 5,5″ SARED', 'El cinturón de levantamiento de pesas Sared esta diseñado con el mejor cuero 100% Colombiano de la más alta calidad. En la parte interna contamos con un forro en Eva microporoso para una mayor comodidad.\r\n', 129900.00, 8, 'https://atlanta-deportes.com.co/wp-content/uploads/2025/06/0118315-CINTURON-LUMBAR-SARED.jpg', '2026-04-08 11:38:19', '2026-04-08 13:17:38', 9, 4),
(70, 'BARRA EN Z 120CM SPORTFITNESS', 'La barra en Z 120cm de Sportfitness es ideal para ejercicios de fuerza, tonificar y ganar masa muscular.\r\n', 94900.00, 48, 'https://atlanta-deportes.com.co/wp-content/uploads/2025/06/0109039-BARRA-EN-Z-120CM-SPORTFITNESS.jpg', '2026-04-08 11:38:32', '2026-04-08 11:38:32', 9, 4),
(71, 'CONO CON HUECOS SPORTFITNESS', 'Con el Cono con Huecos Sportfitness mejora tus entrenamientos, ideal para marcar rutas, ejercicios de agilidad y delimitación de áreas. Su color vibrante y material resistente lo hacen visible y duradero, incluso en exteriores.\r\n', 15900.00, 10, 'https://atlanta-deportes.com.co/wp-content/uploads/2026/02/0129874-CONO-CON-HUECOS-SPORTFITNESS.webp', '2026-04-08 11:38:45', '2026-04-08 11:38:45', 9, 4);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `email` varchar(120) NOT NULL,
  `password_hash` varchar(128) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `role` enum('cliente','emprendedor','admin') NOT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `users`
--

INSERT INTO `users` (`id`, `email`, `password_hash`, `first_name`, `last_name`, `role`, `is_active`, `created_at`) VALUES
(1, 'cliente@cliente.com', 'pbkdf2:sha256:600000$NOPruFAkWACBSre4$789c81ed5a20e1898a1f540dca6f0b50c81314ecd85b7acc0fb13184b183a53f', 'anderson', 'Seren', 'cliente', 1, '2026-04-07 07:09:30'),
(2, 'emprendedor@emprendedor.com', 'pbkdf2:sha256:600000$Nqg6MLD0Flp82a7U$597d8349314643e44d489f79b495779281a726675131e324a23cd7ea9a7b096d', 'Anderson', 'Seren', 'emprendedor', 1, '2026-04-07 07:10:46'),
(3, 'admin@localmarket.com', 'pbkdf2:sha256:600000$VbJFhOL3MPk6tnVi$96cb780adf79373e3e95691d315365a5736451baf6445fd1df26628016df05bc', 'Admin', 'Local', 'admin', 1, '2026-04-07 07:42:31'),
(4, 'ropa@emprendedor.com', 'pbkdf2:sha256:600000$WrILEPRb0WzAeYsj$0ceabe2e62806ff13a17ad18dd4a60378ef1b16cb1d88f5770c3bb864d851b1c', 'Store', 'Close', 'emprendedor', 1, '2026-04-08 08:35:36'),
(5, 'Toys@emprendedor.com', 'pbkdf2:sha256:600000$lL8VhFB5PtilLiom$86c6fdb931031f9a4bad3115583e7bb0732e6451e706bd7df4cfe1c38c367635', 'Toys', 'Store', 'emprendedor', 1, '2026-04-08 08:53:37'),
(6, 'CocinaStore@emprendedor.com', 'pbkdf2:sha256:600000$Fe6MTcwsayjal8tQ$6e24db32217c7d40fba00dfed32f05885193638b8948097dd66dd4b0ad45cf7c', 'Cocina Store', 'Store', 'emprendedor', 1, '2026-04-08 09:31:35'),
(7, 'ElectronicStore@emprendedor.com', 'pbkdf2:sha256:600000$M8gB5SaSllDGtxzU$0a90f3ade16268b8bd054a9cc8c9d7972f3d661dfd10f3d589b034ee3245dfd9', 'ElectronicStore', 'Store', 'emprendedor', 1, '2026-04-08 09:50:14'),
(8, 'HomeStore@emprendedor.com', 'pbkdf2:sha256:600000$OCRqLYsrMGVNVmsn$05dff4a02bcbf7155b81a82b25be9f978133d2a8483013ae00800452e8261282', 'HomeStore', 'Store', 'emprendedor', 1, '2026-04-08 11:13:19'),
(9, 'SportStore@emprendedor.com', 'pbkdf2:sha256:600000$6ARrCqUeec7IBwxQ$d4966e57e115ad122da591dafae5c8dbe9c03327169f18976ed2b153f8c841b3', 'SportStore', 'Store', 'emprendedor', 1, '2026-04-08 11:28:15');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `alembic_version`
--
ALTER TABLE `alembic_version`
  ADD PRIMARY KEY (`version_num`);

--
-- Indices de la tabla `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indices de la tabla `invoices`
--
ALTER TABLE `invoices`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `invoice_number` (`invoice_number`),
  ADD UNIQUE KEY `order_id` (`order_id`);

--
-- Indices de la tabla `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indices de la tabla `order_details`
--
ALTER TABLE `order_details`
  ADD PRIMARY KEY (`id`),
  ADD KEY `order_id` (`order_id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indices de la tabla `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `category_id` (`category_id`);

--
-- Indices de la tabla `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `categories`
--
ALTER TABLE `categories`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `invoices`
--
ALTER TABLE `invoices`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `orders`
--
ALTER TABLE `orders`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `order_details`
--
ALTER TABLE `order_details`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=46;

--
-- AUTO_INCREMENT de la tabla `products`
--
ALTER TABLE `products`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=72;

--
-- AUTO_INCREMENT de la tabla `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `invoices`
--
ALTER TABLE `invoices`
  ADD CONSTRAINT `invoices_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`);

--
-- Filtros para la tabla `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Filtros para la tabla `order_details`
--
ALTER TABLE `order_details`
  ADD CONSTRAINT `order_details_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`),
  ADD CONSTRAINT `order_details_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`);

--
-- Filtros para la tabla `products`
--
ALTER TABLE `products`
  ADD CONSTRAINT `products_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `products_ibfk_2` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
