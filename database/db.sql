-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Tempo de geração: 06-Fev-2023 às 20:12
-- Versão do servidor: 10.4.27-MariaDB
-- versão do PHP: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `db`
--

CREATE SCHEMA IF NOT EXISTS `db` DEFAULT CHARACTER SET utf8 ;
USE `db` ;

--
-- Estrutura da tabela `cliente`
--

CREATE TABLE `cliente` (
  `id` int(5) NOT NULL,
  `cpf` varchar(15) NOT NULL,
  `nome` varchar(100) NOT NULL,
  `rua` varchar(100) NOT NULL,
  `bairro` varchar(100) NOT NULL,
  `numero` varchar(10) NOT NULL,
  `cep` varchar(11) NOT NULL,
  `telefone` varchar(13) DEFAULT NULL,
  `email` varchar(30) DEFAULT NULL,
  `sexo` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Extraindo dados da tabela `cliente`
--

INSERT INTO `cliente` (`id`, `cpf`, `nome`, `rua`, `bairro`, `numero`, `cep`, `telefone`, `email`, `sexo`) VALUES
(0, '0', '0', '0', '0', '0', '0', '0', '0', '0');

-- --------------------------------------------------------

--
-- Estrutura da tabela `comissao`
--

CREATE TABLE `comissao` (
  `id` int(5) NOT NULL,
  `valor` int(10) NOT NULL,
  `funcionario_id` int(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Extraindo dados da tabela `comissao`
--

INSERT INTO `comissao` (`id`, `valor`, `funcionario_id`) VALUES
(0, 0, 1);

-- --------------------------------------------------------

--
-- Estrutura da tabela `compra`
--

CREATE TABLE `compra` (
  `id` int(5) NOT NULL,
  `data` varchar(50) NOT NULL,
  `quantidade` int(11) NOT NULL,
  `valor` int(11) NOT NULL,
  `comissao_id` int(5) NOT NULL,
  `cliente_id` int(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Extraindo dados da tabela `compra`
--

INSERT INTO `compra` (`id`, `data`, `quantidade`, `valor`, `comissao_id`, `cliente_id`) VALUES
(0, '0', 0, 0, 0, 0);

-- --------------------------------------------------------

--
-- Estrutura da tabela `compraproduto`
--

CREATE TABLE `compraproduto` (
  `id` int(5) NOT NULL,
  `nome` varchar(50) NOT NULL,
  `qt_estoque` int(11) NOT NULL,
  `preco` int(11) NOT NULL,
  `fabricante` varchar(100) NOT NULL,
  `estado` varchar(50) NOT NULL,
  `tempo_de_uso` varchar(50) DEFAULT NULL,
  `compra_id` int(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura da tabela `funcionario`
--

CREATE TABLE `funcionario` (
  `id` int(5) NOT NULL,
  `nome` varchar(50) NOT NULL,
  `senha` varchar(20) NOT NULL,
  `salario` varchar(10) NOT NULL,
  `dt_nascimento` varchar(10) NOT NULL,
  `telefone` varchar(15) DEFAULT NULL,
  `tipo` int(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Extraindo dados da tabela `funcionario`
--

INSERT INTO `funcionario` (`id`, `nome`, `senha`, `salario`, `dt_nascimento`, `telefone`, `tipo`) VALUES
(1, 'admin', 'admin', '0', '00-00-0000', '0', 0);

-- --------------------------------------------------------

--
-- Estrutura da tabela `ponto`
--

CREATE TABLE `ponto` (
  `id` int(5) NOT NULL,
  `hora` varchar(10) NOT NULL,
  `data` varchar(15) NOT NULL,
  `nome` varchar(50) NOT NULL,
  `funcionario_id` int(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura da tabela `pontos`
--

CREATE TABLE `pontos` (
  `id` int(5) NOT NULL,
  `hora` varchar(50) NOT NULL,
  `data` varchar(50) NOT NULL,
  `nome` varchar(50) NOT NULL,
  `funcionario_id` int(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura da tabela `produto`
--

CREATE TABLE `produto` (
  `id` int(5) NOT NULL,
  `nome` varchar(50) NOT NULL,
  `qt_estoque` int(11) NOT NULL,
  `preco` int(11) NOT NULL,
  `fabricante` varchar(100) NOT NULL,
  `estado` varchar(50) NOT NULL,
  `tempo_de_uso` varchar(50) DEFAULT NULL,
  `compra_id` int(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Índices para tabelas despejadas
--

--
-- Índices para tabela `cliente`
--
ALTER TABLE `cliente`
  ADD PRIMARY KEY (`id`);

--
-- Índices para tabela `comissao`
--
ALTER TABLE `comissao`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_comissao_funcionario` (`funcionario_id`);

--
-- Índices para tabela `compra`
--
ALTER TABLE `compra`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_compra_comissao` (`comissao_id`),
  ADD KEY `fk_compra_cliente` (`cliente_id`);

--
-- Índices para tabela `compraproduto`
--
ALTER TABLE `compraproduto`
  ADD PRIMARY KEY (`id`);

--
-- Índices para tabela `funcionario`
--
ALTER TABLE `funcionario`
  ADD PRIMARY KEY (`id`);

--
-- Índices para tabela `ponto`
--
ALTER TABLE `ponto`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_ponto_funcionario` (`funcionario_id`);

--
-- Índices para tabela `pontos`
--
ALTER TABLE `pontos`
  ADD PRIMARY KEY (`id`);

--
-- Índices para tabela `produto`
--
ALTER TABLE `produto`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_produto_compra` (`compra_id`);

--
-- AUTO_INCREMENT de tabelas despejadas
--

--
-- AUTO_INCREMENT de tabela `cliente`
--
ALTER TABLE `cliente`
  MODIFY `id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de tabela `comissao`
--
ALTER TABLE `comissao`
  MODIFY `id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de tabela `compra`
--
ALTER TABLE `compra`
  MODIFY `id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de tabela `compraproduto`
--
ALTER TABLE `compraproduto`
  MODIFY `id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de tabela `funcionario`
--
ALTER TABLE `funcionario`
  MODIFY `id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de tabela `ponto`
--
ALTER TABLE `ponto`
  MODIFY `id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de tabela `pontos`
--
ALTER TABLE `pontos`
  MODIFY `id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de tabela `produto`
--
ALTER TABLE `produto`
  MODIFY `id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- Restrições para despejos de tabelas
--

--
-- Limitadores para a tabela `comissao`
--
ALTER TABLE `comissao`
  ADD CONSTRAINT `fk_comissao_funcionario` FOREIGN KEY (`funcionario_id`) REFERENCES `funcionario` (`id`);

--
-- Limitadores para a tabela `compra`
--
ALTER TABLE `compra`
  ADD CONSTRAINT `fk_compra_cliente` FOREIGN KEY (`cliente_id`) REFERENCES `cliente` (`id`),
  ADD CONSTRAINT `fk_compra_comissao` FOREIGN KEY (`comissao_id`) REFERENCES `comissao` (`id`);

--
-- Limitadores para a tabela `ponto`
--
ALTER TABLE `ponto`
  ADD CONSTRAINT `fk_ponto_funcionario` FOREIGN KEY (`funcionario_id`) REFERENCES `funcionario` (`id`);

--
-- Limitadores para a tabela `produto`
--
ALTER TABLE `produto`
  ADD CONSTRAINT `fk_produto_compra` FOREIGN KEY (`compra_id`) REFERENCES `compra` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
