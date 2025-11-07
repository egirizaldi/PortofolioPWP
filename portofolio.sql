-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 07 Nov 2025 pada 07.38
-- Versi server: 10.4.32-MariaDB
-- Versi PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `portofolio`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `projects`
--

CREATE TABLE `projects` (
  `id` int(11) NOT NULL,
  `title` varchar(150) NOT NULL,
  `description` text DEFAULT NULL,
  `image` varchar(255) DEFAULT NULL,
  `link` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `projects`
--

INSERT INTO `projects` (`id`, `title`, `description`, `image`, `link`) VALUES
(1, 'website', 'Ini adalah website terbaik ', 'Dashboard_-_Social_Media_Analytics.jpg', 'https://chatgpt.com/c/690b4c42-81a0-8320-9d14-7fc9aea8eb66');

-- --------------------------------------------------------

--
-- Struktur dari tabel `skills`
--

CREATE TABLE `skills` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `level` varchar(50) DEFAULT NULL,
  `icon` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `skills`
--

INSERT INTO `skills` (`id`, `name`, `level`, `icon`) VALUES
(2, 'Wordpress', 'Intermediate', 'wordpress.png'),
(3, 'Python', 'Beginner', 'download.png');

-- --------------------------------------------------------

--
-- Struktur dari tabel `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `name` varchar(150) DEFAULT NULL,
  `bio` text DEFAULT NULL,
  `photo` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `name`, `bio`, `photo`) VALUES
(1, 'egirizaldi112', '112233', 'Egi Rizaldi123', 'Web Developer dan Digital Creator yang berfokus pada pembuatan website modern, responsif, dan berorientasi konversi. Saya berpengalaman membangun landing page, website bisnis, serta dashboard berbasis web menggunakan teknologi seperti WordPress, Bootstrap, dan Flask.\r\nSaya juga aktif sebagai konten kreator faceless di TikTok dengan niche bisnis dan marketing digital, termasuk penjualan produk digital.\r\nBagi saya, teknologi bukan hanya tentang tampilan, tetapi bagaimana menciptakan pengalaman digital yang efektif, cepat, dan menghasilkan dampak nyata.', 'WhatsApp_Image_2025-10-27_at_19.54.01_100666f1.jpg');

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `projects`
--
ALTER TABLE `projects`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `skills`
--
ALTER TABLE `skills`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `projects`
--
ALTER TABLE `projects`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT untuk tabel `skills`
--
ALTER TABLE `skills`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT untuk tabel `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
