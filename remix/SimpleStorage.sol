// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.8.7;

contract SimpleStorage {

    // uint256 favoriteNumber = 5;
    // bool favoriteBool = true;
    // string favoriteString = "String";
    // int256 favoriteInt = -5;
    // address favoriteAddress = 0x18e24B27B6152595B9545C1757280EDc46545545;   
    // bytes32 favoriteBytes = "bytes";

    uint256 public favoriteNumber;

    struct Person {
        string name;
        uint256 favoriteNumber;
    }

    Person[] public people;
    mapping(string => uint256) public nameToFavoriteNumber;

    function store(uint256 _favoriteNumber) public {
        favoriteNumber = _favoriteNumber;
    }

    function retrieve() public view returns(uint256) {
        return favoriteNumber;
    }

    function addPerson(string memory _name, uint256 number) public {
        people.push(Person({name: _name, favoriteNumber: number}));
        nameToFavoriteNumber[_name] = number;
    }
}

