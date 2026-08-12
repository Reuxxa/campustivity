-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 12, 2025 at 07:40 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `sistemkegiatan`
--

-- --------------------------------------------------------

--
-- Table structure for table `absensi`
--

CREATE TABLE `absensi` (
  `id_absensi` int(11) NOT NULL,
  `id_pendaftaran` int(11) NOT NULL,
  `tgl_kehadiran` date NOT NULL,
  `status_kehadiran` enum('belum absen','alfa','hadir','izin','sakit') DEFAULT 'belum absen',
  `id_pengelola` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `absensi`
--

INSERT INTO `absensi` (`id_absensi`, `id_pendaftaran`, `tgl_kehadiran`, `status_kehadiran`, `id_pengelola`) VALUES
(1, 8, '2025-06-12', 'hadir', 2),
(2, 10, '2025-06-12', 'izin', 2),
(3, 12, '2025-06-12', 'hadir', 2),
(4, 16, '2025-06-13', 'hadir', 2),
(5, 17, '2025-06-13', 'izin', 3),
(6, 18, '2025-06-13', 'alfa', 4),
(7, 19, '2025-06-13', 'sakit', 5),
(8, 20, '2025-06-13', 'hadir', 6);

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id_admin` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(100) NOT NULL,
  `nim` varchar(15) DEFAULT NULL,
  `id_pengelola` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id_admin`, `username`, `password`, `nim`, `id_pengelola`) VALUES
(2, 'isa', '$2b$12$1W0GPvVH.MXbKuFv/0t3DudjchY0jopCSfG8iIADcdY4h4k016SJa', NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `kegiatan`
--

CREATE TABLE `kegiatan` (
  `id_kegiatan` int(11) NOT NULL,
  `judul_kegiatan` varchar(100) NOT NULL,
  `waktu` datetime NOT NULL,
  `tempat` varchar(100) NOT NULL,
  `deskripsi` text DEFAULT NULL,
  `id_pengelola` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `kegiatan`
--

INSERT INTO `kegiatan` (`id_kegiatan`, `judul_kegiatan`, `waktu`, `tempat`, `deskripsi`, `id_pengelola`) VALUES
(2, 'Badminton', '2025-06-16 00:00:00', 'Lapangan UTY', 'Lomba antar prodi.', 2),
(3, 'Tenis Meja', '2025-06-12 00:00:00', 'UTY', 'Lomba antar prodi.', 2),
(4, 'Latihan Hadroh', '2025-06-13 00:00:00', 'Masjid UTY', 'Shalawat bersama mahasiswa UTY.', 6),
(5, 'Mini Futsal Cup', '2025-06-13 00:00:00', 'Lapangan', 'Mini Futsal Cup yang diadakan oleh bagian Olahraga', 2),
(6, 'Pameran Lukisan', '2025-06-13 00:00:00', 'Aula', 'Pameran Lukisan yang diadakan oleh bagian Seni', 3),
(7, 'Try Out UTBK', '2025-06-13 00:00:00', 'Online', 'Try Out UTBK yang diadakan oleh bagian Akademik', 4),
(8, 'Pelatihan UI/UX', '2025-06-13 00:00:00', 'Lab', 'Pelatihan UI/UX yang diadakan oleh bagian Teknologi', 5),
(9, 'Doa Bersama', '2025-06-13 00:00:00', 'Masjid', 'Doa Bersama yang diadakan oleh bagian Kerohanian', 6);

-- --------------------------------------------------------

--
-- Table structure for table `mahasiswa`
--

CREATE TABLE `mahasiswa` (
  `nim` varchar(15) NOT NULL,
  `nama_mahasiswa` varchar(100) NOT NULL,
  `prodi` varchar(50) NOT NULL,
  `angkatan` year(4) NOT NULL,
  `password` varchar(100) NOT NULL,
  `id_admin` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `mahasiswa`
--

INSERT INTO `mahasiswa` (`nim`, `nama_mahasiswa`, `prodi`, `angkatan`, `password`, `id_admin`) VALUES
('123', 'Aretha', 'informatika', '2022', '$2b$12$xVRTRHqFPFNc9dz66UfZNO3vka5Is/XTw.xyZAXGZQkx9SD6y3Qk2', NULL),
('124', 'Intan Liana', 'Informatika', '2023', '$2b$12$C9DPSyXKVUn8RfvlzSmxCOFgGyLBK1kYxLOHYw.pUz0SBEInbWZra', NULL),
('125', 'Dina Oktavia', 'Informatika', '2023', '$2b$12$Fs2Q2tRkxakX32U.6q3cKupaQU4F39pda7CkUwJXPnCZSdMQrTKsS', NULL),
('126', 'Juha Jushy', 'Informatika', '2022', '$2b$12$2a26Civpm8jtIq3Pc0KnBei5oU3x9d8EoZOyBIhJSaoLj9OG5RqVO', NULL),
('234', 'Karen Tresha', 'Manajemen', '2024', '$2b$12$ez48gQvpjX/BkoOiuMceg.aJ6rfOpPiHto3wOlpSfKhubzi3pS7Bq', NULL),
('235', 'Cintya', 'Manajemen', '2024', '$2b$12$snhHTm73PJh45c4sxbPWB.sPfpgSrV41AiGydoC6CCBE9h1IgHtHa', NULL),
('236', 'Elisa Amelia', 'Manajemen', '2022', '$2b$12$rV0Sju1p9dT.nnmXBxhFOOj3cfyPXoJrdWjd44G9x6g7LDcXubS72', NULL),
('311', 'Tariq Hidayat', 'Informatika', '2023', '$2b$12$fa435678a60f7b1dd3f3646dc1c9e6aa8f2a8ab9cbe2149277a9a', NULL),
('312', 'Gilang', 'Teknik Elektro', '2022', '$2b$12$cd7a97b1e89d5031b2df9db4a9c7fbbf824f73034f7cc6abff322', NULL),
('313', 'Rosa Meilani', 'Manajemen', '2021', '$2b$12$fd9ba8a1ac237c8cc4762c9cf7ee02819ad1d46d8c875e9ff3921', NULL),
('314', 'Bayu', 'Sistem Informasi', '2024', '$2b$12$aa03123e30de4453ac7d223cba2c3db7c4df2c7d43b28f522ec5c', NULL),
('315', 'Nabila Zahra', 'Informatika', '2023', '$2b$12$b8245f7d0cbd2b8e879c9e58251d2347ce9c33e3fa28d3a3a0ecf', NULL),
('345', 'Satria Ridho', 'Sistem Informasi', '2021', '$2b$12$SOSBd0yr0lC6oWi3Vv2Zies1KdrYlP7DLkbQkXw9Gg2VU73Cy0ET2', NULL),
('346', 'Rafli Ramdan', 'Sistem Informasi', '2021', '$2b$12$eqm3jiTrqdVIRXUJNZsuSuoxAWMh.l4fNk3aWiks6ISS6lySTTOXi', NULL),
('347', 'Sri Suci', 'Sistem Informasi', '2021', '$2b$12$Xwi0LtLUuUyonMIT9YcsJOteAtLWBIYMNdzgzrbx9s0RZptEKcbAi', NULL),
('348', 'Nia Kurnia Sari', 'Sistem Informasi', '2021', '$2b$12$slI4mDOgbEuYR4py7rMIWuTUd3yxqflFOW4KdV5tgnKv3AN0G6/Ni', NULL),
('349', 'Aldy Putra', 'Sistem Informasi', '2024', '$2b$12$RW.9OKhO0RkPhFfL4/qKr.lpdgmPhFOWIh9pGr7AL99oMlZhoZvB2', NULL),
('452', 'Firgo FI', 'Teknik Elektro', '2021', '$2b$12$1flw0PsBMuzG2uotZFmPBuZazSl33PuChASCLOOQXjQx6jG4wL2Xe', NULL),
('453', 'Rendi Firman', 'Teknik Elektro', '2021', '$2b$12$XdB1N/gxrTXI5WLF11Yr9Ob2qmZetprqKse3nn97wnQAMI2CDE2AO', NULL),
('454', 'Alisya Rahma', 'Teknik Elektro', '2024', '$2b$12$GdVtPICc04uf/WoyuuBx7.5yeEZ0ggim3ybfN7iLpcEED46qk5Ytm', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `notifikasi`
--

CREATE TABLE `notifikasi` (
  `id_notifikasi` int(11) NOT NULL,
  `nim` varchar(15) NOT NULL,
  `judul` varchar(100) NOT NULL,
  `pesan` text NOT NULL,
  `tanggal` date NOT NULL,
  `id_pengelola` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `notifikasi`
--

INSERT INTO `notifikasi` (`id_notifikasi`, `nim`, `judul`, `pesan`, `tanggal`, `id_pengelola`) VALUES
(2, '123', 'Kegiatan Baru', 'Ada kegiatan baru: Badminton. Yuk cek dan daftar sekarang!', '2025-06-11', NULL),
(3, '123', 'Kegiatan Baru', 'Ada kegiatan baru: Tenis Meja. Yuk cek dan daftar sekarang!', '2025-06-11', NULL),
(4, '123', 'Kegiatan Baru', 'Ada kegiatan baru: Latihan Hadroh. Yuk cek dan daftar sekarang!', '2025-06-12', NULL),
(5, '124', 'Kegiatan Baru', 'Ada kegiatan baru: Latihan Hadroh. Yuk cek dan daftar sekarang!', '2025-06-12', NULL),
(6, '125', 'Kegiatan Baru', 'Ada kegiatan baru: Latihan Hadroh. Yuk cek dan daftar sekarang!', '2025-06-12', NULL),
(7, '126', 'Kegiatan Baru', 'Ada kegiatan baru: Latihan Hadroh. Yuk cek dan daftar sekarang!', '2025-06-12', NULL),
(8, '234', 'Kegiatan Baru', 'Ada kegiatan baru: Latihan Hadroh. Yuk cek dan daftar sekarang!', '2025-06-12', NULL),
(9, '235', 'Kegiatan Baru', 'Ada kegiatan baru: Latihan Hadroh. Yuk cek dan daftar sekarang!', '2025-06-12', NULL),
(10, '236', 'Kegiatan Baru', 'Ada kegiatan baru: Latihan Hadroh. Yuk cek dan daftar sekarang!', '2025-06-12', NULL),
(11, '345', 'Kegiatan Baru', 'Ada kegiatan baru: Latihan Hadroh. Yuk cek dan daftar sekarang!', '2025-06-12', NULL),
(12, '346', 'Kegiatan Baru', 'Ada kegiatan baru: Latihan Hadroh. Yuk cek dan daftar sekarang!', '2025-06-12', NULL),
(13, '347', 'Kegiatan Baru', 'Ada kegiatan baru: Latihan Hadroh. Yuk cek dan daftar sekarang!', '2025-06-12', NULL),
(14, '348', 'Kegiatan Baru', 'Ada kegiatan baru: Latihan Hadroh. Yuk cek dan daftar sekarang!', '2025-06-12', NULL),
(15, '349', 'Kegiatan Baru', 'Ada kegiatan baru: Latihan Hadroh. Yuk cek dan daftar sekarang!', '2025-06-12', NULL),
(16, '452', 'Kegiatan Baru', 'Ada kegiatan baru: Latihan Hadroh. Yuk cek dan daftar sekarang!', '2025-06-12', NULL),
(17, '453', 'Kegiatan Baru', 'Ada kegiatan baru: Latihan Hadroh. Yuk cek dan daftar sekarang!', '2025-06-12', NULL),
(18, '454', 'Kegiatan Baru', 'Ada kegiatan baru: Latihan Hadroh. Yuk cek dan daftar sekarang!', '2025-06-12', NULL),
(19, '123', 'Kegiatan Baru', 'Ada kegiatan baru: Mini Futsal Cup. Yuk cek dan daftar sekarang!', '2025-06-13', 2),
(20, '124', 'Kegiatan Baru', 'Ada kegiatan baru: Mini Futsal Cup. Yuk cek dan daftar sekarang!', '2025-06-13', 2),
(21, '125', 'Kegiatan Baru', 'Ada kegiatan baru: Mini Futsal Cup. Yuk cek dan daftar sekarang!', '2025-06-13', 2),
(22, '126', 'Kegiatan Baru', 'Ada kegiatan baru: Mini Futsal Cup. Yuk cek dan daftar sekarang!', '2025-06-13', 2),
(23, '234', 'Kegiatan Baru', 'Ada kegiatan baru: Mini Futsal Cup. Yuk cek dan daftar sekarang!', '2025-06-13', 2),
(24, '235', 'Kegiatan Baru', 'Ada kegiatan baru: Mini Futsal Cup. Yuk cek dan daftar sekarang!', '2025-06-13', 2),
(25, '236', 'Kegiatan Baru', 'Ada kegiatan baru: Mini Futsal Cup. Yuk cek dan daftar sekarang!', '2025-06-13', 2),
(26, '345', 'Kegiatan Baru', 'Ada kegiatan baru: Mini Futsal Cup. Yuk cek dan daftar sekarang!', '2025-06-13', 2),
(27, '346', 'Kegiatan Baru', 'Ada kegiatan baru: Mini Futsal Cup. Yuk cek dan daftar sekarang!', '2025-06-13', 2),
(28, '347', 'Kegiatan Baru', 'Ada kegiatan baru: Mini Futsal Cup. Yuk cek dan daftar sekarang!', '2025-06-13', 2),
(29, '348', 'Kegiatan Baru', 'Ada kegiatan baru: Mini Futsal Cup. Yuk cek dan daftar sekarang!', '2025-06-13', 2),
(30, '349', 'Kegiatan Baru', 'Ada kegiatan baru: Mini Futsal Cup. Yuk cek dan daftar sekarang!', '2025-06-13', 2),
(31, '452', 'Kegiatan Baru', 'Ada kegiatan baru: Mini Futsal Cup. Yuk cek dan daftar sekarang!', '2025-06-13', 2),
(32, '453', 'Kegiatan Baru', 'Ada kegiatan baru: Mini Futsal Cup. Yuk cek dan daftar sekarang!', '2025-06-13', 2),
(33, '454', 'Kegiatan Baru', 'Ada kegiatan baru: Mini Futsal Cup. Yuk cek dan daftar sekarang!', '2025-06-13', 2),
(34, '311', 'Kegiatan Baru', 'Ada kegiatan baru: Mini Futsal Cup. Yuk cek dan daftar sekarang!', '2025-06-13', 2),
(35, '312', 'Kegiatan Baru', 'Ada kegiatan baru: Mini Futsal Cup. Yuk cek dan daftar sekarang!', '2025-06-13', 2),
(36, '313', 'Kegiatan Baru', 'Ada kegiatan baru: Mini Futsal Cup. Yuk cek dan daftar sekarang!', '2025-06-13', 2),
(37, '314', 'Kegiatan Baru', 'Ada kegiatan baru: Mini Futsal Cup. Yuk cek dan daftar sekarang!', '2025-06-13', 2),
(38, '315', 'Kegiatan Baru', 'Ada kegiatan baru: Mini Futsal Cup. Yuk cek dan daftar sekarang!', '2025-06-13', 2),
(39, '123', 'Kegiatan Baru', 'Ada kegiatan baru: Pameran Lukisan. Yuk cek dan daftar sekarang!', '2025-06-13', 3),
(40, '124', 'Kegiatan Baru', 'Ada kegiatan baru: Pameran Lukisan. Yuk cek dan daftar sekarang!', '2025-06-13', 3),
(41, '125', 'Kegiatan Baru', 'Ada kegiatan baru: Pameran Lukisan. Yuk cek dan daftar sekarang!', '2025-06-13', 3),
(42, '126', 'Kegiatan Baru', 'Ada kegiatan baru: Pameran Lukisan. Yuk cek dan daftar sekarang!', '2025-06-13', 3),
(43, '234', 'Kegiatan Baru', 'Ada kegiatan baru: Pameran Lukisan. Yuk cek dan daftar sekarang!', '2025-06-13', 3),
(44, '235', 'Kegiatan Baru', 'Ada kegiatan baru: Pameran Lukisan. Yuk cek dan daftar sekarang!', '2025-06-13', 3),
(45, '236', 'Kegiatan Baru', 'Ada kegiatan baru: Pameran Lukisan. Yuk cek dan daftar sekarang!', '2025-06-13', 3),
(46, '345', 'Kegiatan Baru', 'Ada kegiatan baru: Pameran Lukisan. Yuk cek dan daftar sekarang!', '2025-06-13', 3),
(47, '346', 'Kegiatan Baru', 'Ada kegiatan baru: Pameran Lukisan. Yuk cek dan daftar sekarang!', '2025-06-13', 3),
(48, '347', 'Kegiatan Baru', 'Ada kegiatan baru: Pameran Lukisan. Yuk cek dan daftar sekarang!', '2025-06-13', 3),
(49, '348', 'Kegiatan Baru', 'Ada kegiatan baru: Pameran Lukisan. Yuk cek dan daftar sekarang!', '2025-06-13', 3),
(50, '349', 'Kegiatan Baru', 'Ada kegiatan baru: Pameran Lukisan. Yuk cek dan daftar sekarang!', '2025-06-13', 3),
(51, '452', 'Kegiatan Baru', 'Ada kegiatan baru: Pameran Lukisan. Yuk cek dan daftar sekarang!', '2025-06-13', 3),
(52, '453', 'Kegiatan Baru', 'Ada kegiatan baru: Pameran Lukisan. Yuk cek dan daftar sekarang!', '2025-06-13', 3),
(53, '454', 'Kegiatan Baru', 'Ada kegiatan baru: Pameran Lukisan. Yuk cek dan daftar sekarang!', '2025-06-13', 3),
(54, '311', 'Kegiatan Baru', 'Ada kegiatan baru: Pameran Lukisan. Yuk cek dan daftar sekarang!', '2025-06-13', 3),
(55, '312', 'Kegiatan Baru', 'Ada kegiatan baru: Pameran Lukisan. Yuk cek dan daftar sekarang!', '2025-06-13', 3),
(56, '313', 'Kegiatan Baru', 'Ada kegiatan baru: Pameran Lukisan. Yuk cek dan daftar sekarang!', '2025-06-13', 3),
(57, '314', 'Kegiatan Baru', 'Ada kegiatan baru: Pameran Lukisan. Yuk cek dan daftar sekarang!', '2025-06-13', 3),
(58, '315', 'Kegiatan Baru', 'Ada kegiatan baru: Pameran Lukisan. Yuk cek dan daftar sekarang!', '2025-06-13', 3),
(59, '123', 'Kegiatan Baru', 'Ada kegiatan baru: Try Out UTBK. Yuk cek dan daftar sekarang!', '2025-06-13', 4),
(60, '124', 'Kegiatan Baru', 'Ada kegiatan baru: Try Out UTBK. Yuk cek dan daftar sekarang!', '2025-06-13', 4),
(61, '125', 'Kegiatan Baru', 'Ada kegiatan baru: Try Out UTBK. Yuk cek dan daftar sekarang!', '2025-06-13', 4),
(62, '126', 'Kegiatan Baru', 'Ada kegiatan baru: Try Out UTBK. Yuk cek dan daftar sekarang!', '2025-06-13', 4),
(63, '234', 'Kegiatan Baru', 'Ada kegiatan baru: Try Out UTBK. Yuk cek dan daftar sekarang!', '2025-06-13', 4),
(64, '235', 'Kegiatan Baru', 'Ada kegiatan baru: Try Out UTBK. Yuk cek dan daftar sekarang!', '2025-06-13', 4),
(65, '236', 'Kegiatan Baru', 'Ada kegiatan baru: Try Out UTBK. Yuk cek dan daftar sekarang!', '2025-06-13', 4),
(66, '345', 'Kegiatan Baru', 'Ada kegiatan baru: Try Out UTBK. Yuk cek dan daftar sekarang!', '2025-06-13', 4),
(67, '346', 'Kegiatan Baru', 'Ada kegiatan baru: Try Out UTBK. Yuk cek dan daftar sekarang!', '2025-06-13', 4),
(68, '347', 'Kegiatan Baru', 'Ada kegiatan baru: Try Out UTBK. Yuk cek dan daftar sekarang!', '2025-06-13', 4),
(69, '348', 'Kegiatan Baru', 'Ada kegiatan baru: Try Out UTBK. Yuk cek dan daftar sekarang!', '2025-06-13', 4),
(70, '349', 'Kegiatan Baru', 'Ada kegiatan baru: Try Out UTBK. Yuk cek dan daftar sekarang!', '2025-06-13', 4),
(71, '452', 'Kegiatan Baru', 'Ada kegiatan baru: Try Out UTBK. Yuk cek dan daftar sekarang!', '2025-06-13', 4),
(72, '453', 'Kegiatan Baru', 'Ada kegiatan baru: Try Out UTBK. Yuk cek dan daftar sekarang!', '2025-06-13', 4),
(73, '454', 'Kegiatan Baru', 'Ada kegiatan baru: Try Out UTBK. Yuk cek dan daftar sekarang!', '2025-06-13', 4),
(74, '311', 'Kegiatan Baru', 'Ada kegiatan baru: Try Out UTBK. Yuk cek dan daftar sekarang!', '2025-06-13', 4),
(75, '312', 'Kegiatan Baru', 'Ada kegiatan baru: Try Out UTBK. Yuk cek dan daftar sekarang!', '2025-06-13', 4),
(76, '313', 'Kegiatan Baru', 'Ada kegiatan baru: Try Out UTBK. Yuk cek dan daftar sekarang!', '2025-06-13', 4),
(77, '314', 'Kegiatan Baru', 'Ada kegiatan baru: Try Out UTBK. Yuk cek dan daftar sekarang!', '2025-06-13', 4),
(78, '315', 'Kegiatan Baru', 'Ada kegiatan baru: Try Out UTBK. Yuk cek dan daftar sekarang!', '2025-06-13', 4),
(79, '123', 'Kegiatan Baru', 'Ada kegiatan baru: Pelatihan UI/UX. Yuk cek dan daftar sekarang!', '2025-06-13', 5),
(80, '124', 'Kegiatan Baru', 'Ada kegiatan baru: Pelatihan UI/UX. Yuk cek dan daftar sekarang!', '2025-06-13', 5),
(81, '125', 'Kegiatan Baru', 'Ada kegiatan baru: Pelatihan UI/UX. Yuk cek dan daftar sekarang!', '2025-06-13', 5),
(82, '126', 'Kegiatan Baru', 'Ada kegiatan baru: Pelatihan UI/UX. Yuk cek dan daftar sekarang!', '2025-06-13', 5),
(83, '234', 'Kegiatan Baru', 'Ada kegiatan baru: Pelatihan UI/UX. Yuk cek dan daftar sekarang!', '2025-06-13', 5),
(84, '235', 'Kegiatan Baru', 'Ada kegiatan baru: Pelatihan UI/UX. Yuk cek dan daftar sekarang!', '2025-06-13', 5),
(85, '236', 'Kegiatan Baru', 'Ada kegiatan baru: Pelatihan UI/UX. Yuk cek dan daftar sekarang!', '2025-06-13', 5),
(86, '345', 'Kegiatan Baru', 'Ada kegiatan baru: Pelatihan UI/UX. Yuk cek dan daftar sekarang!', '2025-06-13', 5),
(87, '346', 'Kegiatan Baru', 'Ada kegiatan baru: Pelatihan UI/UX. Yuk cek dan daftar sekarang!', '2025-06-13', 5),
(88, '347', 'Kegiatan Baru', 'Ada kegiatan baru: Pelatihan UI/UX. Yuk cek dan daftar sekarang!', '2025-06-13', 5),
(89, '348', 'Kegiatan Baru', 'Ada kegiatan baru: Pelatihan UI/UX. Yuk cek dan daftar sekarang!', '2025-06-13', 5),
(90, '349', 'Kegiatan Baru', 'Ada kegiatan baru: Pelatihan UI/UX. Yuk cek dan daftar sekarang!', '2025-06-13', 5),
(91, '452', 'Kegiatan Baru', 'Ada kegiatan baru: Pelatihan UI/UX. Yuk cek dan daftar sekarang!', '2025-06-13', 5),
(92, '453', 'Kegiatan Baru', 'Ada kegiatan baru: Pelatihan UI/UX. Yuk cek dan daftar sekarang!', '2025-06-13', 5),
(93, '454', 'Kegiatan Baru', 'Ada kegiatan baru: Pelatihan UI/UX. Yuk cek dan daftar sekarang!', '2025-06-13', 5),
(94, '311', 'Kegiatan Baru', 'Ada kegiatan baru: Pelatihan UI/UX. Yuk cek dan daftar sekarang!', '2025-06-13', 5),
(95, '312', 'Kegiatan Baru', 'Ada kegiatan baru: Pelatihan UI/UX. Yuk cek dan daftar sekarang!', '2025-06-13', 5),
(96, '313', 'Kegiatan Baru', 'Ada kegiatan baru: Pelatihan UI/UX. Yuk cek dan daftar sekarang!', '2025-06-13', 5),
(97, '314', 'Kegiatan Baru', 'Ada kegiatan baru: Pelatihan UI/UX. Yuk cek dan daftar sekarang!', '2025-06-13', 5),
(98, '315', 'Kegiatan Baru', 'Ada kegiatan baru: Pelatihan UI/UX. Yuk cek dan daftar sekarang!', '2025-06-13', 5),
(99, '123', 'Kegiatan Baru', 'Ada kegiatan baru: Doa Bersama. Yuk cek dan daftar sekarang!', '2025-06-13', 6),
(100, '124', 'Kegiatan Baru', 'Ada kegiatan baru: Doa Bersama. Yuk cek dan daftar sekarang!', '2025-06-13', 6),
(101, '125', 'Kegiatan Baru', 'Ada kegiatan baru: Doa Bersama. Yuk cek dan daftar sekarang!', '2025-06-13', 6),
(102, '126', 'Kegiatan Baru', 'Ada kegiatan baru: Doa Bersama. Yuk cek dan daftar sekarang!', '2025-06-13', 6),
(103, '234', 'Kegiatan Baru', 'Ada kegiatan baru: Doa Bersama. Yuk cek dan daftar sekarang!', '2025-06-13', 6),
(104, '235', 'Kegiatan Baru', 'Ada kegiatan baru: Doa Bersama. Yuk cek dan daftar sekarang!', '2025-06-13', 6),
(105, '236', 'Kegiatan Baru', 'Ada kegiatan baru: Doa Bersama. Yuk cek dan daftar sekarang!', '2025-06-13', 6),
(106, '345', 'Kegiatan Baru', 'Ada kegiatan baru: Doa Bersama. Yuk cek dan daftar sekarang!', '2025-06-13', 6),
(107, '346', 'Kegiatan Baru', 'Ada kegiatan baru: Doa Bersama. Yuk cek dan daftar sekarang!', '2025-06-13', 6),
(108, '347', 'Kegiatan Baru', 'Ada kegiatan baru: Doa Bersama. Yuk cek dan daftar sekarang!', '2025-06-13', 6),
(109, '348', 'Kegiatan Baru', 'Ada kegiatan baru: Doa Bersama. Yuk cek dan daftar sekarang!', '2025-06-13', 6),
(110, '349', 'Kegiatan Baru', 'Ada kegiatan baru: Doa Bersama. Yuk cek dan daftar sekarang!', '2025-06-13', 6),
(111, '452', 'Kegiatan Baru', 'Ada kegiatan baru: Doa Bersama. Yuk cek dan daftar sekarang!', '2025-06-13', 6),
(112, '453', 'Kegiatan Baru', 'Ada kegiatan baru: Doa Bersama. Yuk cek dan daftar sekarang!', '2025-06-13', 6),
(113, '454', 'Kegiatan Baru', 'Ada kegiatan baru: Doa Bersama. Yuk cek dan daftar sekarang!', '2025-06-13', 6),
(114, '311', 'Kegiatan Baru', 'Ada kegiatan baru: Doa Bersama. Yuk cek dan daftar sekarang!', '2025-06-13', 6),
(115, '312', 'Kegiatan Baru', 'Ada kegiatan baru: Doa Bersama. Yuk cek dan daftar sekarang!', '2025-06-13', 6),
(116, '313', 'Kegiatan Baru', 'Ada kegiatan baru: Doa Bersama. Yuk cek dan daftar sekarang!', '2025-06-13', 6),
(117, '314', 'Kegiatan Baru', 'Ada kegiatan baru: Doa Bersama. Yuk cek dan daftar sekarang!', '2025-06-13', 6),
(118, '315', 'Kegiatan Baru', 'Ada kegiatan baru: Doa Bersama. Yuk cek dan daftar sekarang!', '2025-06-13', 6);

-- --------------------------------------------------------

--
-- Table structure for table `pendaftaran`
--

CREATE TABLE `pendaftaran` (
  `id_pendaftaran` int(11) NOT NULL,
  `nim` varchar(15) NOT NULL,
  `id_kegiatan` int(11) NOT NULL,
  `tgl_pendaftaran` date NOT NULL,
  `status` enum('pending','terdaftar','diterima','ditolak') DEFAULT 'pending'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `pendaftaran`
--

INSERT INTO `pendaftaran` (`id_pendaftaran`, `nim`, `id_kegiatan`, `tgl_pendaftaran`, `status`) VALUES
(8, '123', 3, '2025-06-12', 'diterima'),
(9, '454', 2, '2025-06-12', 'terdaftar'),
(10, '452', 3, '2025-06-12', 'diterima'),
(11, '453', 2, '2025-06-12', 'terdaftar'),
(12, '453', 3, '2025-06-12', 'diterima'),
(13, '126', 4, '2025-06-12', 'terdaftar'),
(14, '235', 4, '2025-06-12', 'terdaftar'),
(15, '454', 4, '2025-06-12', 'terdaftar'),
(16, '311', 5, '2025-06-13', 'diterima'),
(17, '312', 6, '2025-06-13', 'terdaftar'),
(18, '313', 7, '2025-06-13', 'pending'),
(19, '314', 8, '2025-06-13', 'ditolak'),
(20, '315', 9, '2025-06-13', 'diterima');

-- --------------------------------------------------------

--
-- Table structure for table `pengelola`
--

CREATE TABLE `pengelola` (
  `id_pengelola` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `id_admin` int(11) DEFAULT NULL,
  `bagian` enum('Olahraga','Seni','Akademik','Teknologi','Kerohanian') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `pengelola`
--

INSERT INTO `pengelola` (`id_pengelola`, `username`, `password`, `id_admin`, `bagian`) VALUES
(2, 'laila', '$2b$12$aKXPhYYZSB9l27mpPIvpgu3Ogqp4M7G9x.TDul.oxJqzNP4C/c7t2', NULL, 'Olahraga'),
(3, 'clara', '$2b$12$thyjrMbBB9O1Ri15D3PZ0e2VXLi8GGxZONso/4UUR.Vk7aSbJFkm6', NULL, 'Seni'),
(4, 'zahra', '$2b$12$bynM3taOSkb.5F7qI1silu8JKvJ1jHbvCCV8N1CckZx.aZyHVPiHK', NULL, 'Akademik'),
(5, 'kevin', '$2b$12$UAi1v9iIkq6RyufDODcGee/G1B/LtKK3l176X1AcAs/j8C5njiCzu', NULL, 'Teknologi'),
(6, 'adnan', '$2b$12$MuQlW7uaDq1vkLmNeOkKRe3SJlFlGnh6YWjVYUtacRWZWTde3dcK6', NULL, 'Kerohanian');

-- --------------------------------------------------------

--
-- Table structure for table `sertifikat`
--

CREATE TABLE `sertifikat` (
  `id_sertifikat` int(11) NOT NULL,
  `id_pendaftaran` int(11) NOT NULL,
  `tgl_terbit` date NOT NULL,
  `status` varchar(20) DEFAULT 'pending'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `sertifikat`
--

INSERT INTO `sertifikat` (`id_sertifikat`, `id_pendaftaran`, `tgl_terbit`, `status`) VALUES
(1, 8, '2025-06-12', 'Terbit'),
(2, 12, '2025-06-12', 'Terbit'),
(3, 16, '2025-06-13', 'Terbit'),
(4, 20, '2025-06-13', 'Terbit');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `absensi`
--
ALTER TABLE `absensi`
  ADD PRIMARY KEY (`id_absensi`),
  ADD KEY `idx_absensi_pendaftaran` (`id_pendaftaran`),
  ADD KEY `idx_absensi_pengelola` (`id_pengelola`);

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id_admin`),
  ADD KEY `fk_admin_mahasiswa` (`nim`),
  ADD KEY `fk_admin_pengelola` (`id_pengelola`);

--
-- Indexes for table `kegiatan`
--
ALTER TABLE `kegiatan`
  ADD PRIMARY KEY (`id_kegiatan`),
  ADD KEY `idx_kegiatan_pengelola` (`id_pengelola`);

--
-- Indexes for table `mahasiswa`
--
ALTER TABLE `mahasiswa`
  ADD PRIMARY KEY (`nim`),
  ADD KEY `idx_mahasiswa_nim` (`nim`),
  ADD KEY `fk_mahasiswa_admin` (`id_admin`);

--
-- Indexes for table `notifikasi`
--
ALTER TABLE `notifikasi`
  ADD PRIMARY KEY (`id_notifikasi`),
  ADD KEY `idx_notifikasi_nim` (`nim`),
  ADD KEY `fk_pengelola_notif` (`id_pengelola`);

--
-- Indexes for table `pendaftaran`
--
ALTER TABLE `pendaftaran`
  ADD PRIMARY KEY (`id_pendaftaran`),
  ADD KEY `idx_pendaftaran_nim` (`nim`),
  ADD KEY `idx_pendaftaran_kegiatan` (`id_kegiatan`);

--
-- Indexes for table `pengelola`
--
ALTER TABLE `pengelola`
  ADD PRIMARY KEY (`id_pengelola`),
  ADD KEY `fk_pengelola_admin` (`id_admin`);

--
-- Indexes for table `sertifikat`
--
ALTER TABLE `sertifikat`
  ADD PRIMARY KEY (`id_sertifikat`),
  ADD KEY `idx_sertifikat_pendaftaran` (`id_pendaftaran`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `absensi`
--
ALTER TABLE `absensi`
  MODIFY `id_absensi` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `id_admin` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `kegiatan`
--
ALTER TABLE `kegiatan`
  MODIFY `id_kegiatan` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `notifikasi`
--
ALTER TABLE `notifikasi`
  MODIFY `id_notifikasi` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=119;

--
-- AUTO_INCREMENT for table `pendaftaran`
--
ALTER TABLE `pendaftaran`
  MODIFY `id_pendaftaran` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `pengelola`
--
ALTER TABLE `pengelola`
  MODIFY `id_pengelola` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `sertifikat`
--
ALTER TABLE `sertifikat`
  MODIFY `id_sertifikat` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `absensi`
--
ALTER TABLE `absensi`
  ADD CONSTRAINT `absensi_ibfk_1` FOREIGN KEY (`id_pendaftaran`) REFERENCES `pendaftaran` (`id_pendaftaran`) ON DELETE CASCADE,
  ADD CONSTRAINT `absensi_ibfk_2` FOREIGN KEY (`id_pengelola`) REFERENCES `pengelola` (`id_pengelola`);

--
-- Constraints for table `admin`
--
ALTER TABLE `admin`
  ADD CONSTRAINT `fk_admin_mahasiswa` FOREIGN KEY (`nim`) REFERENCES `mahasiswa` (`nim`) ON DELETE SET NULL,
  ADD CONSTRAINT `fk_admin_pengelola` FOREIGN KEY (`id_pengelola`) REFERENCES `pengelola` (`id_pengelola`) ON DELETE SET NULL;

--
-- Constraints for table `kegiatan`
--
ALTER TABLE `kegiatan`
  ADD CONSTRAINT `kegiatan_ibfk_1` FOREIGN KEY (`id_pengelola`) REFERENCES `pengelola` (`id_pengelola`);

--
-- Constraints for table `mahasiswa`
--
ALTER TABLE `mahasiswa`
  ADD CONSTRAINT `fk_mahasiswa_admin` FOREIGN KEY (`id_admin`) REFERENCES `admin` (`id_admin`) ON DELETE SET NULL;

--
-- Constraints for table `notifikasi`
--
ALTER TABLE `notifikasi`
  ADD CONSTRAINT `fk_pengelola_notif` FOREIGN KEY (`id_pengelola`) REFERENCES `pengelola` (`id_pengelola`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `notifikasi_ibfk_1` FOREIGN KEY (`nim`) REFERENCES `mahasiswa` (`nim`) ON DELETE CASCADE;

--
-- Constraints for table `pendaftaran`
--
ALTER TABLE `pendaftaran`
  ADD CONSTRAINT `pendaftaran_ibfk_1` FOREIGN KEY (`nim`) REFERENCES `mahasiswa` (`nim`) ON DELETE CASCADE,
  ADD CONSTRAINT `pendaftaran_ibfk_2` FOREIGN KEY (`id_kegiatan`) REFERENCES `kegiatan` (`id_kegiatan`) ON DELETE CASCADE;

--
-- Constraints for table `pengelola`
--
ALTER TABLE `pengelola`
  ADD CONSTRAINT `fk_pengelola_admin` FOREIGN KEY (`id_admin`) REFERENCES `admin` (`id_admin`) ON DELETE SET NULL;

--
-- Constraints for table `sertifikat`
--
ALTER TABLE `sertifikat`
  ADD CONSTRAINT `sertifikat_ibfk_1` FOREIGN KEY (`id_pendaftaran`) REFERENCES `pendaftaran` (`id_pendaftaran`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
