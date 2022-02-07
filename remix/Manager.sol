// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.8.7;

// import "./Donation.sol";

contract Donation {

    address payable public owner;
    event Status(string, uint256);

    constructor() {
        owner = payable(msg.sender);
    }

    modifier onlyOwner {
        require(owner == msg.sender, "Allowed only for owner!");
        _;
    }

    function donate() payable public {
        emit Status("new donation", balance());
        require(msg.value >= 10 ** 9, "1 gwei minimum donation.");
    }

    function withdraw() onlyOwner public {
        emit Status("pre withdrawal", balance());
        owner.transfer(address(this).balance);
        emit Status("post withdrawal", balance());
    }

    function balance() public view returns(uint256) {
        return address(this).balance;
    }
}

contract Manager {

    Donation immutable public myDonation;
    Donation public otherDonation;

    event Status(string, uint256);

    constructor() {
        myDonation = new Donation();
    }

    receive() external payable {
        emit Status("received", balance());
    }

    function setOtherDonation(Donation _otherDonation) public {
        otherDonation = _otherDonation;
    }

    function balance() public view returns(uint256) {
        return address(this).balance;
    }

    function withdraw() public {
        emit Status("pre withdrawal", balance());
        myDonation.withdraw();
        emit Status("post withdrawal", balance());
    }

    function forwardDonation() public {
        require(address(otherDonation) != address(0));

        emit Status("pre forward", balance());
        myDonation.withdraw();
        otherDonation.donate{value: balance()}();
        emit Status("post forward", balance());
    }
}

