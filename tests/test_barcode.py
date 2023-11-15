from barcode_decoder.barcode import BarCode, BarCode11, create_barcode11_from_str

class TestBarCode11:
    def test_initialization(self):
        bytes_list = [bytes([1, 2, 3])]
        barcode = BarCode11(bytes_list)
        assert barcode.get_code() == bytes_list

    def test_without_check_digit(self):
        bytes_list: list[bytes] = [
                    BarCode11.str_to_code_map["S/S"],
                        *[BarCode11.str_to_code_map[str(code)] for code in [1, 2, 3, 4, "-", 5, 6, 7, 8]],
                        BarCode11.str_to_code_map["6"],
                        BarCode11.str_to_code_map["S/S"]
                    ]
        
        barcode = BarCode11(bytes_list)
        assert barcode.check_digit == None
        assert not barcode.is_valid()

    def test_check_digit(self):
        bytes_list: list[bytes] = [
                    BarCode11.str_to_code_map["S/S"],
                        *[BarCode11.str_to_code_map[str(code)] for code in [1, 2, 3, 4, "-", 5, 6, 7, 8]],
                        BarCode11.str_to_code_map["6"],
                        BarCode11.str_to_code_map["S/S"]
                    ]
        
        barcode = BarCode11(bytes_list, use_check=True)
        assert barcode.check_digit == "6"
        
    def test_valid(self):
        bytes_list: list[bytes] = [
                    BarCode11.str_to_code_map["S/S"],
                        *[BarCode11.str_to_code_map[str(code)] for code in [1, 2, 3, 4, "-", 5, 6, 7, 8]],
                        BarCode11.str_to_code_map["6"],
                        BarCode11.str_to_code_map["S/S"]
                    ]
        
        barcode = BarCode11(bytes_list)
        is_valid: bool = barcode.is_valid()
        assert not is_valid
        
        barcode = BarCode11(bytes_list, min_number_of_digits=10)
        is_valid: bool = barcode.is_valid()
        assert is_valid
        
        barcode = BarCode11(bytes_list, min_number_of_digits=9)
        is_valid: bool = barcode.is_valid()
        assert not is_valid
        
        barcode = BarCode11(bytes_list, use_check=True)
        is_valid: bool = barcode.is_valid()
        assert is_valid
        
        bytes_list: list[bytes] = [
            BarCode11.str_to_code_map["S/S"],
                *[BarCode11.str_to_code_map[str(code)] for code in [1, 2, 3, 4, "-", 5, 6, 7, 8]],
                BarCode11.str_to_code_map["5"], # Wrong Checksum
                BarCode11.str_to_code_map["S/S"]
            ]
        
        barcode = BarCode11(bytes_list)
        is_valid: bool = barcode.is_valid()
        assert not is_valid
        
        barcode = BarCode11(bytes_list, min_number_of_digits=10)
        is_valid: bool = barcode.is_valid()
        assert is_valid
        
        barcode = BarCode11(bytes_list, min_number_of_digits=9)
        is_valid: bool = barcode.is_valid()
        assert not is_valid
        
        barcode = BarCode11(bytes_list, use_check=True)
        is_valid: bool = barcode.is_valid()
        assert not is_valid
        
        bytes_list: list[bytes] = [
                *[BarCode11.str_to_code_map[str(code)] for code in [1, 2, 3, 4, "-", 5, 6, 7, 8]],
                BarCode11.str_to_code_map["5"], # Wrong Checksum
                BarCode11.str_to_code_map["S/S"]
            ]
        
        barcode = BarCode11(bytes_list, min_number_of_digits=10)
        is_valid: bool = barcode.is_valid()
        assert not is_valid
        
        bytes_list: list[bytes] = [
                *[BarCode11.str_to_code_map[str(code)] for code in [1, 2, 3, 4, "-", 5, 6, 7, 8]],
                BarCode11.str_to_code_map["5"], # Wrong Checksum
            ]
        
        barcode = BarCode11(bytes_list, min_number_of_digits=10)
        is_valid: bool = barcode.is_valid()
        assert not is_valid
        
        bytes_list: list[bytes] = [
                BarCode11.str_to_code_map["1"],
                *[BarCode11.str_to_code_map[str(code)] for code in [1, 2, 3, 4, "-", 5, 6, 7, 8]],
                BarCode11.str_to_code_map["5"] # Wrong Checksum
            ]
        
        barcode = BarCode11(bytes_list, min_number_of_digits=10)
        is_valid: bool = barcode.is_valid()
        assert not is_valid
        
        bytes_list: list[bytes] = [
                BarCode11.str_to_code_map["1"],
                *[BarCode11.str_to_code_map[str(code)] for code in [1, 2, 3, 4, "-", 5, 6, 7, 8]],
                BarCode11.str_to_code_map["5"], # Wrong Checksum
                BarCode11.str_to_code_map["-"]
            ]
        
        barcode = BarCode11(bytes_list, min_number_of_digits=10)
        is_valid: bool = barcode.is_valid()
        assert not is_valid
        
    def test_barcode_creator(self):
        bytes_list: list[bytes] = [
                    BarCode11.str_to_code_map["S/S"],
                        *[BarCode11.str_to_code_map[str(code)] for code in [1, 2, 3, 4, "-", 5, 6, 7, 8]],
                        BarCode11.str_to_code_map["6"],
                        BarCode11.str_to_code_map["S/S"]
                    ]
        bytes_list_str = ["S/S", "1", "2", "3", "4", "-", "5", "6", "7", "8", "6", "S/S"]
        
        barcode = create_barcode11_from_str(bytes_list_str)
        assert barcode.get_code() == bytes_list