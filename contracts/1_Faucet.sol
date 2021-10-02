// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.5.0 <0.9.0;

/**
 * @title Ownable
 * @dev The Ownable contract has an owner address, and provides basic authorization control
 * functions, this simplifies the implementation of "user permissions".
 */
contract Ownable {
  address public owner;

  event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);

  /**
   * @dev The Ownable constructor sets the original `owner` of the contract to the sender
   * account.
   */
  constructor() {
    owner = msg.sender;
  }


  /**
   * @dev Throws if called by any account other than the owner.
   */
  modifier onlyOwner() {
    require(msg.sender == owner);
    _;
  }


  /**
   * @dev Allows the current owner to transfer control of the contract to a newOwner.
   * @param newOwner The address to transfer ownership to.
   */
  function transferOwnership(address newOwner) public onlyOwner {
    require(newOwner != address(0));
    emit OwnershipTransferred(owner, newOwner);
    owner = newOwner;
  }

}

/**
 * 
 * @title Rinkeby Faucet EscuelaCryptoES
 * 
 * @author @EscuelaCryptoES & @Ivanovish10
 * 
 * @dev This is the official EscuelaCryptoES Rinkeby Faucet
 * to all the Telegram members
 * 
 */
contract RinkebyECESFaucet is Ownable {
    
    /**
     * @dev cooldownTime put to 1 days. One user cannot take more than 1 ETH daily
     */
    uint private cooldown = 1 days;
    
    /**
     * @dev reward in wei
     */
     uint private _reward = 1000000000000000000;
    
    /**
     * 
     * @dev Struct to store all the user info
     * 
     */
    struct User{
        string telegram;
        address last_Address;
        bool Stored;
        uint64 ready;
    }
    
    /**
     * 
     * @dev Mapping to store all the users with their Telegram users
     * 
     */
    mapping (string => User) users;
    
    /**
     * 
     * @dev Updates cooldownTime state variable ;; for 1 day 86400
     * 
     * @param __days is the new time to set cooldownTime
     * 
     */
    function setCooldownTime(uint __days) public onlyOwner {
        cooldown = __days;
    }
    
    /**
     * 
     * @dev Returns the actual cooldownTime
     * 
     * @return the cooldownTime in uint256
     * 
     */
    function getCooldownTime() external view onlyOwner returns(uint) {
        return cooldown;
    }
    
    /**
     * 
     * @dev Updates reward state variable ;; 1000000000000000000 for 1 ether
     * 
     * @param __wei is the new reward
     * 
     */
    function setReward(uint __wei) public onlyOwner {
        _reward = __wei;
    }
    
    /**
     * 
     * @dev Returns the actual reward value
     * 
     * @return the reward in uint256
     * 
     */
    function getReward() external view onlyOwner returns(uint) {
        return _reward;
    }

    /**
     * 
     * @notice Function to pay a user with the set reward
     * 
     * @param __user is the Telegram user name
     * @param __to is the user's Ethereum address 
     * 
     */
    function payUser(string memory __user, address __to) external payable onlyOwner {
        User storage u = users[__user];
        
        if(!u.Stored){
            // Not stored yet
            u.last_Address = __to;
            u.telegram = __user;
            u.Stored = true;
        }
        
        if(u.last_Address != __to){
            u.last_Address = __to;
        }
        
        require(_ethDeployed1Day(__user), "Solo puedes conseguir ETH cada 24 horas");
        
        // Pay
        u.ready = uint64(block.timestamp + cooldown);
        address payable chosenOne = payable(__to); 
        chosenOne.transfer(_reward);
    }
    
    /**
     * 
     * @notice This function lets you know if you are ready to 
     * receive the set reward again
     *
     * @param __user is the Telegram user name
     * 
     */
    function _ethDeployed1Day(string memory __user) internal view returns (bool) {
        User storage u = users[__user];
        return u.ready <= block.timestamp;
    }
    
    /**
     * 
     * @notice This function returns your info stored
     * 
     * @dev Later, in frontend we transform the waiting time
     * into an understandable language.
     * 
     * @param __user is the Telegram user name
     *
     * @return User info in tuple format
     * 
     */
    function seeMyInfo(string memory __user) external view returns(User memory){
        User storage u = users[__user];
        return u;
    }
    
    /**
     * 
     * @notice Smart Contract feeding function
     * 
     */
    receive() external payable {}
    
}