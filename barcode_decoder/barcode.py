from abc import abstractmethod

class BarCode:
    # Init to initialize the Bar Code as a list of integer
    def __init__(self, code: list[bytes]) -> None:
        self.code: list[bytes] = code

    # Return the current code
    def get_code(self, without_check=True, raw=True) -> list[bytes]:
        return self.code

    # Set a new code value
    def set_code(self, code: list[bytes]) -> None:
        self.code = code

    # Check if the code is valid, depends on the barcode type.
    @abstractmethod
    def is_valid() -> bool:
        pass
    
    # Show the code transform the list[bytes] -> str
    @abstractmethod
    def __str__(self) -> str:
        return ""

class BarCode11(BarCode):
    code_to_str_map: dict[str, str] = {
        bytes([1,0,1,0,1,1]): "0",
        bytes([1,1,0,1,0,1,1]): "1",
        bytes([1,0,0,1,0,1,1]): "2",
        bytes([1,1,0,0,1,0,1]): "3",
        bytes([1,0,1,1,0,1,1]): "4",
        bytes([1,1,0,1,1,0,1]): "5",
        bytes([1,0,0,1,1,0,1]): "6",
        bytes([1,0,1,0,0,1,1]): "7",
        bytes([1,1,0,1,0,0,1]): "8",
        bytes([1,1,0,1,0,1]): "9",
        bytes([1,0,1,1,0,1]): "-",
        bytes([1,0,1,1,0,0,1]): "S/S"
    }

    str_to_code_map: dict[str, bytes] = {
        "0": bytes([1,0,1,0,1,1]),
        "1": bytes([1,1,0,1,0,1,1]),
        "2": bytes([1,0,0,1,0,1,1]),
        "3": bytes([1,1,0,0,1,0,1]),
        "4": bytes([1,0,1,1,0,1,1]),
        "5": bytes([1,1,0,1,1,0,1]),
        "6": bytes([1,0,0,1,1,0,1]),
        "7": bytes([1,0,1,0,0,1,1]),
        "8": bytes([1,1,0,1,0,0,1]),
        "9": bytes([1,1,0,1,0,1]),
        "-": bytes([1,0,1,1,0,1]),
        "S/S": bytes([1,0,1,1,0,0,1])
    }
    
    code_to_int_map: dict[bytes, int] = {
        bytes([1,0,1,0,1,1]): 0,
        bytes([1,1,0,1,0,1,1]): 1,
        bytes([1,0,0,1,0,1,1]): 2,
        bytes([1,1,0,0,1,0,1]): 3,
        bytes([1,0,1,1,0,1,1]): 4,
        bytes([1,1,0,1,1,0,1]): 5,
        bytes([1,0,0,1,1,0,1]): 6,
        bytes([1,0,1,0,0,1,1]): 7,
        bytes([1,1,0,1,0,0,1]): 8,
        bytes([1,1,0,1,0,1]): 9,
        bytes([1,0,1,1,0,1]): 10
    }

    def __init__(self, code: list[bytes], use_check: bool=False, min_number_of_digits: int=1) -> None:
        super().__init__(code)
        self.use_check: bool = use_check
        if self.use_check:
            if len(self.code) < 4: # 1 Start + 1 Digit (at least) + 1 CheckSum + 1 Stop = 4
                self.valid: bool = False
                return
            
            if [self.code[0], self.code[-1]] != 2 * [BarCode11.str_to_code_map["S/S"]]:
                self.valid: bool = False
                return

            self.check_digit: str = BarCode11.code_to_str(code[-2])
            
            if self.check_digit in ["-", "S/S"]:
                self.valid: bool = False
            else:
                self.valid: bool = None
        else:
            self.valid = len(self.code) == (min_number_of_digits + 2) # 1 Start + N Digit + 1 Stop = N + 2
            self.valid = self.valid and [self.code[0], self.code[-1]] == 2 * [BarCode11.str_to_code_map["S/S"]]
            self.check_digit = None

    @staticmethod
    def code_to_str(code: bytes) -> str:
        return BarCode11.code_to_str_map[code]
    
    @staticmethod
    def code_to_int(code: bytes) -> int:
        return BarCode11.code_to_int_map[code]
    
    @staticmethod
    def checksum(code) -> tuple[bool, int | None]:
        sum: int = 0
        index: int = len(code)

        for byte in code:
            if byte == BarCode11.str_to_code_map["S/S"]:
                valid = False
                return (valid, None)
            
            sum += BarCode11.code_to_int(byte) * (index)
            index -= 1
        
        return (True, sum)
    
    @staticmethod
    def get_expect_digit(sum: int) -> int:
        return 11 - int(sum / 11) % 11
        
    def is_valid(self) -> bool:
        if self.valid is not None:
            return self.valid
        
        valid, sum = BarCode11.checksum(self.code[1:-2])
        if not valid:
            self.valid = False
            return self.valid

        expected_digit: int = BarCode11.get_expect_digit(sum)
        self.valid: bool = expected_digit == int(self.check_digit)

        return self.valid

    def __str__(self) -> str:
        return ", ".join([BarCode11.code_to_str_map[byte] for byte in self.code])

def create_barcode11_from_str(code: list[str], use_check: bool=False, min_number_of_digits: int=1) -> BarCode11:
    list_bytes: list[bytes] = []
    for digit in code:
        list_bytes.append(BarCode11.str_to_code_map[digit])
    return BarCode11(code=list_bytes, use_check=use_check, min_number_of_digits=min_number_of_digits)
