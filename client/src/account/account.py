import json
import os
from typing import List

from ..utils.logging import log
from ..models.peer import Peer
from ..config import ACCOUNT_FILE

class Account(Peer):
    """
    Represents a user account that extends Peer functionality with persistence.
    
    Inherits from Peer and adds file-based storage, account management,
    and GUI authentication capabilities.
    
    Attributes:
        username: Unique identifier/username of the account
        host: IP address or hostname where the account is registered
        port: Network port number for the account (1024-65535)
    
    Class Methods:
        create: Create and persist a new account
        load: Load account(s) from storage
        auth: GUI authentication dialog for account selection
    
    Examples:
        >>> # Create a new account
        >>> account = Account.create("alice", "192.168.1.10", 8080)
        
        >>> # Load specific account
        >>> account = Account.load("alice")
        
        >>> # Interactive authentication (async)
        >>> account = await Account.auth()
    """
    
    @staticmethod
    def __read_file() -> List["Account"]:
        """
        Read accounts data from JSON file.  
        If the file does not exist, it will be created with an empty list.

        Returns:
            list: List of Accounts made from account dicts from file,  
                or an empty list if the file doesn't exist, is corrupted,  
                or cannot be read/written.

        Notes:
            - If the file is missing, it will be created automatically.
            - If the file exists but contains invalid JSON, an empty list is returned.
            - If the file is not a list, an empty list is returned.
        """

        # if ACCOUNT_FILE exists then read and return dictionary list
        if os.path.exists(ACCOUNT_FILE):
            try:
                with open(ACCOUNT_FILE, "r") as f:
                    data = json.load(f) # get info in dicts 
                    data = [Account.from_dict(acc_data) for acc_data in data] # remake into the Peers
                    log.info("Account file read.")
                    return data if isinstance(data, list) else []
            except (json.JSONDecodeError, TypeError, OSError) as ex:
                log.error(f"Error in account file reading:\n{ex}")
                return []
            
        # if ACCOUNT_FILE does not exists then create it and return empty list
        log.info("Creating ACCOUNT_FILE . . .")
        try:
            with open(ACCOUNT_FILE, "w") as f:
                json.dump([], f, ensure_ascii=False, indent=4)
        except OSError as ex:
            log.error(f"Error in ACCOUNT_FILE creating:\n{ex}")
            return []
        log.info("ACCOUNT_FILE created.")
        return []

    @staticmethod
    def __write_file(accounts_list):
        """
        Write accounts list to JSON file.
        
        Args:
            accounts_list: List of account dictionaries to persist
        """
        with open(ACCOUNT_FILE, "w") as f:
            json.dump(accounts_list, f, indent=4)

    @classmethod
    def create(cls, username: str, host: str, port: int):
        """
        Create and persist a new account.
        
        Args:
            username: Unique username for the account
            host: IP address or hostname
            port: Port number (1024-65535)
            
        Returns:
            Account: Newly created account instance
        """
        acc = cls(username=username, host=host, port=port)
        accounts = Account.__read_file()
        if not any(a["username"] == username for a in accounts):
            accounts.append(acc.to_json())
            Account.__write_file(accounts)
            log.info(f"Account '{username}' created")
        else:
            log.info(f"Account '{username}' already exists")
        return acc

    @classmethod
    def load(cls, username=None):
        """
        Load account(s) from persistent storage.
        
        Args:
            username: Specific username to load. If None, loads first account.
            
        Returns:
            Account: Loaded account instance, or None if not found
        """
        accounts = Account.__read_file()
        if not accounts:
            return None
        if username:
            acc_data = next((a for a in accounts if a["username"] == username), None)
            return cls(**acc_data) if acc_data else None
        return cls(**accounts[0]) # default first
    
    @staticmethod
    def get_accounts_from_file():
        return Account.__read_file()
