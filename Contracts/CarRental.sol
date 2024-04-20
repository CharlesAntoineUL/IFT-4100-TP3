// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 < 0.9.0;

contract CarRental {
    address private owner;
    uint private carCount = 0;

    struct Car {
        uint id;
        address owner;
        string brand;
        string model;
        string yearOfConstruction;
        uint rentalPricePerDay;
        bool isRented;
    }

    mapping(uint => Car) public cars;
    mapping(uint => address) public carRenters;
    mapping(address => uint) public deposits;

    event CarAdded(uint carId, string brand, string model, string yearOfConstruction);
    event CarRented(uint carId, address indexed renter, uint numDays);
    event CarReturned(uint carId, address indexed renter);
    event CarRemoved(uint carId);

    modifier onlyOwner() {
        require(msg.sender == owner, unicode"Cette personne n'est pas le propriétaire de l'auto");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function addCar(string memory _brand, string memory _model, string memory _yearOfConstruction, uint _rentalPricePerDay) public {
        uint carId = carCount++;
        cars[carId] = Car(carId, msg.sender, _brand, _model, _yearOfConstruction, _rentalPricePerDay, false);
        emit CarAdded(carId, _brand, _model, _yearOfConstruction);
    }

    function rentCar(uint _carId, uint _numDays) public payable {
        Car storage car = cars[_carId];

        carRenters[_carId] = msg.sender;
        deposits[msg.sender] = msg.value;
        car.isRented = true;
        emit CarRented(_carId, msg.sender, _numDays);
    }

    function returnCar(uint _carId) public {
        require(carRenters[_carId] == msg.sender, unicode"Vous n'êtes pas le locataire de cet auto");
        Car storage car = cars[_carId];

        uint deposit = deposits[msg.sender];
        uint refundAmount = deposit - car.rentalPricePerDay * 2;
        deposits[msg.sender] = 0;

        payable(msg.sender).transfer(refundAmount);
        car.isRented = false;
        emit CarReturned(_carId, msg.sender);
    }

    function getCar(uint _carId) public view returns (Car memory) {
        return cars[_carId];
    }

    function removeCar(uint _carId) public onlyOwner {
        require(!cars[_carId].isRented, unicode"L'auto est présentement déjà loué");
        delete cars[_carId];
        emit CarRemoved(_carId);
    }
}