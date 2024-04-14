pragma solidity 0.8.24;

contract contrat {
    struct Item {
        uint id;
        address payable owner;
        string description;
        bool isRented;
    }
}