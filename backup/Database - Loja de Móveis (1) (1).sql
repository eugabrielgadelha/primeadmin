-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=1;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`Cliente`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Cliente` (
  `cpf` VARCHAR(15) NOT NULL,
  `nome` VARCHAR(200) NOT NULL,
  `rua` VARCHAR(100) NOT NULL,
  `bairro` VARCHAR(100) NOT NULL,
  `cep` VARCHAR(9) NOT NULL,
  `numero` VARCHAR(10) NOT NULL,
  `telefone` VARCHAR(11) NULL,
  `email` VARCHAR(100) NULL,
  PRIMARY KEY (`cpf`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Compra`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Compra` (
  `codigo` INT NOT NULL,
  `data_aqui` VARCHAR(50) NOT NULL,
  `quantidade` INT NOT NULL,
  `Cliente_cpf` VARCHAR(15) NOT NULL,
  `Funcionarios_codigo` INT NOT NULL,
  `codigo_produto` VARCHAR(50) NOT NULL,
  `valor` INT NOT NULL,
  PRIMARY KEY (`codigo`),
  INDEX `fk_Compra_Cliente_idx` (`Cliente_cpf` ASC),
  CONSTRAINT `fk_Compra_Cliente`
    FOREIGN KEY (`Cliente_cpf`)
    REFERENCES `mydb`.`Cliente` (`cpf`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Produto`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Produto` (
  `id` INT NOT NULL,
  `qt_estoque` INT NOT NULL,
  `preço` INT NOT NULL,
  `fabricante` VARCHAR(100) NOT NULL,
  `estado` VARCHAR(45) NOT NULL,
  `nome` VARCHAR(45) NOT NULL,
  `tempo_de_uso` VARCHAR(45) NULL,
  `Compra_codigo` INT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_Produto_Compra1_idx` (`Compra_codigo` ASC),
  CONSTRAINT `fk_Produto_Compra1`
    FOREIGN KEY (`Compra_codigo`)
    REFERENCES `mydb`.`Compra` (`codigo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Funcionarios`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Funcionarios` (
  `codigo` INT NOT NULL,
  `nome` VARCHAR(100) NOT NULL,
  `salario` INT NOT NULL,
  `dt_nascimento` VARCHAR(50) NOT NULL,
  `telefone` VARCHAR(45) NULL,
  `Ponto_id` INT NOT NULL,
  PRIMARY KEY (`codigo`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Ponto`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Ponto` (
  `id` INT NOT NULL,
  `data_ponto` VARCHAR(50) NOT NULL,
  `hora` VARCHAR(45) NOT NULL,
  `nome_funcionario` VARCHAR(200) NOT NULL,
  `Funcionarios_codigo` INT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_Ponto_Funcionarios1_idx` (`Funcionarios_codigo` ASC),
  CONSTRAINT `fk_Ponto_Funcionarios1`
    FOREIGN KEY (`Funcionarios_codigo`)
    REFERENCES `mydb`.`Funcionarios` (`codigo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Comissao`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Comissao` (
  `codigo` INT NOT NULL,
  `valor` INT NOT NULL,
  `Funcionarios_codigo` INT NOT NULL,
  `Compra_codigo` INT NOT NULL,
  PRIMARY KEY (`codigo`, `Funcionarios_codigo`, `Compra_codigo`),
  INDEX `fk_Comissao_Funcionarios1_idx` (`Funcionarios_codigo` ASC),
  INDEX `fk_Comissao_Compra1_idx` (`Compra_codigo` ASC),
  CONSTRAINT `fk_Comissao_Funcionarios1`
    FOREIGN KEY (`Funcionarios_codigo`)
    REFERENCES `mydb`.`Funcionarios` (`codigo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Comissao_Compra1`
    FOREIGN KEY (`Compra_codigo`)
    REFERENCES `mydb`.`Compra` (`codigo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
