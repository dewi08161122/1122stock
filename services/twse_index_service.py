from utils.data_utils import FormatHelper

class TwseIndex:
    @staticmethod
    def get_TWindex_url(date):
        date_str = date.strftime("%Y%m%d")
        url_TW_k = f"https://www.twse.com.tw/rwd/zh/TAIEX/MI_5MINS_HIST?date={date_str}&response=json"
        url_TW_v = f"https://www.twse.com.tw/rwd/zh/afterTrading/FMTQIK?date={date_str}&response=json"
        return url_TW_k, url_TW_v

    @staticmethod
    def clean_index_data(jsondata_TW_k, jsondata_TW_v):
        combined_dict = {}
        TW_k_data = jsondata_TW_k.get('data', [])
        for i in TW_k_data:
            date_key = i[0]
            combined_dict[date_key] = {
                "trade_date": FormatHelper.change_tw_date(i[0]),
                "open": FormatHelper.clean_value_to_float(i[1]),
                "close": FormatHelper.clean_value_to_float(i[4]),
                "high": FormatHelper.clean_value_to_float(i[2]),
                "low": FormatHelper.clean_value_to_float(i[3]),
                "change": 0.0,
                "value": 0     
            }
        TW_v_data = jsondata_TW_v.get('data', [])
        for i in TW_v_data:
            date_key = i[0]
            if date_key in combined_dict:
                combined_dict[date_key]["value"] = FormatHelper.clean_value_to_int(i[2])
                combined_dict[date_key]["change"] = FormatHelper.clean_value_to_float(i[5])
        records = []
        for i in combined_dict.values():
            record = (
                i["trade_date"],
                i["open"],
                i["close"],
                i["high"],
                i["low"],
                i["change"],
                i["value"]
            )
            records.append(record)
        
        return records
