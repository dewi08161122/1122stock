

class FormatHelper:
    @staticmethod
    def change_tw_date(tw_date_str: str):
        y, m, d = tw_date_str.split('/')
        western_year = int(y) + 1911
        return f"{western_year}-{m.zfill(2)}-{d.zfill(2)}"
    
    @staticmethod
    def clean_value_to_float(value: str):
        if not value or value in ['X', '--', ' ']:
            return 0.0
        try:
            clean_value = value.replace(',', '').replace('+', '')
            return float(clean_value)
        except ValueError:
            return 0.0
    
    @staticmethod
    def clean_value_to_int(value: str):
        if not value or value in ['X', '--', ' ']:
            return 0
        try:
            return int(value.replace(',', ''))
        except ValueError:
            return 0
    