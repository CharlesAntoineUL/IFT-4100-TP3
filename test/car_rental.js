const CarRental = artifacts.require("CarRental");

/*
 * uncomment accounts to access the test accounts made available by the
 * Ethereum client
 * See docs: https://www.trufflesuite.com/docs/truffle/testing/writing-tests-in-javascript
 */
contract("CarRental", function (accounts) {
  it("should assert true", async function () {
    console.log(await web3.eth.getBalance(accounts[0]));
    console.log(await web3.eth.getBalance(accounts[1]));
    await CarRental.deployed();
    return assert.isTrue(true);
  });
});
