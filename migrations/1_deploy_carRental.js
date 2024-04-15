const carRental = artifacts.require("CarRental")

module.exports = function(deployer) {
    deployer.deploy(carRental)
}