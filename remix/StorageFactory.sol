// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.8.7;

import "./SimpleStorage.sol";

contract StorageFactory is SimpleStorage {

    SimpleStorage[] public simpleStorageArray;

    function createSimpleStorageContract() public {
        SimpleStorage simpleStorage = new SimpleStorage();
        simpleStorageArray.push(simpleStorage);
    }

    function sfStore(uint256 index, uint256 number) public {
        SimpleStorage simpleStorage = SimpleStorage(address(simpleStorageArray[index]));
        simpleStorage.store(number);
    }

    function sfRetrieve(uint256 index) public view returns (uint256) {
        SimpleStorage simpleStorage = SimpleStorage(address(simpleStorageArray[index]));
        return simpleStorage.retrieve();
    }

}

