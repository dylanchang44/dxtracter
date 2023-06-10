import requests, json, aiohttp

class Source():
    def __init__(self):
        self.data = {}

class DataMap:
    def __init__(self):
        self.value = {}
        self.result = {}
        self.normalized_result = {}

class Drater:
    def __init__(self):
        self.source = Source()
        self.company_data = DataMap()

    def parse_target(self, yaml):
        # Process the data
        for key, values in yaml.items():
            # Create a list to store the values
            value_list = []
            # Iterate over the values and append them to the list
            for value in values:
                value_list.append(value)
            # Add the key-value pair to the dictionary
            self.source.data[key] = value_list

    async def fetch_data(self, api_key, symbol):
        for category in self.source.data.keys():
            endpoint = f"https://www.alphavantage.co/query?function={category}&symbol={symbol}&apikey={api_key}"
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(endpoint) as response:
                        response.raise_for_status()
                        fetch_result = await response.text()
                        self.parse_fetched_data(category, fetch_result)
            except aiohttp.ClientError as err:
                return f"Failed to fetch values. Error: {err}"
        
        self.convert_company_data()   #debug till here
        self.normalize_company_data()
    
    def parse_fetched_data(self, keyword, json_string): 
        # Parse the JSON data
        try:
            #turn json string to dict
            json_text = json.loads(json_string)
        except Exception as err:
            return f"Failed to parse JSON: {err}"
        
        if len(json_text) < 1:
            raise ValueError("Empty or invalid JSON data, check if stock symbol is correct")
            
        # Extract data vector
        target_vec = json_text if keyword == "OVERVIEW" else json_text["quarterlyReports"][0]
        for item in self.source.data[keyword]:
            try:
                self.company_data.value[item] = float(target_vec.get(item))
            except ValueError:
                self.company_data.value[item] = 0.0

    def convert_company_data(self):
        source_map = self.company_data.value
        result = self.company_data.result
        
        result["gross_margin"] = 100.0 * (source_map["grossProfit"] / abs(source_map["totalRevenue"]))
        result["net_margin"] = 100.0 * (source_map["netIncome"] / abs(source_map["totalRevenue"]))
        result["retained_earning"] = 100.0 * (source_map["retainedEarnings"] / abs(source_map["totalShareholderEquity"]))
        result["total_equity"] = 100.0 * (source_map["totalShareholderEquity"] / abs(source_map["netIncome"]))
        result["capital_expenditure"] = 100.0 * (source_map["capitalExpenditures"] / abs(source_map["netIncome"]))
        result["dividend_paid"] = 100.0 * (source_map["dividendPayout"] / abs(source_map["operatingCashflow"]))
        result["cash_finance"] = 100.0 * (source_map["cashflowFromFinancing"] / abs(source_map["operatingCashflow"]))
        result["PERatio"] = source_map["PERatio"] if source_map["PERatio"]>=0.0 else 120.0
        result["PEGRatio"] = source_map["PEGRatio"] if source_map["PEGRatio"]>=0.0 else 3.0
        #print(self.company_data.result)
    
    def normalize_company_data(self):
        source_map = self.company_data.result
        result = self.company_data.normalized_result

        result["gross_margin"] = source_map["gross_margin"]  # 0~100
        result["net_margin"] = 5.0 * source_map["net_margin"]  # 0~20
        result["retained_earning"] = (source_map["retained_earning"] + 200.0) / 10.0  # -200~800
        result["total_equity"] = source_map["total_equity"] / 50.0  # 0~5000
        result["capital_expenditure"] = source_map["capital_expenditure"]  # 0~100
        result["dividend_paid"] = 2.0 * source_map["dividend_paid"]  # 0~50
        result["cash_finance"] = (source_map["cash_finance"] + 200.0) / 4.0  # -200~200
        result["PERatio"] = (150.0 - source_map["PERatio"]) * 2.0/3.0        # 0~150 
        result["PEGRatio"] = 100.0 - source_map["PEGRatio"] * 100.0 / 4.0    # 0~4 
        #clear negative score
        for key, value in result.items():
            if isinstance(value, float) and value < 0.0:
                result[key] = 0.0
            elif isinstance(value, float) and value > 100.0:
                result[key] = 100.0
        #print(self.company_data.normalized_result)

    def rating_calc(self) -> float:
        n_map = [
            self.company_data.normalized_result["gross_margin"],
            self.company_data.normalized_result["net_margin"],
            self.company_data.normalized_result["retained_earning"],
            self.company_data.normalized_result["total_equity"],
            self.company_data.normalized_result["capital_expenditure"],
            self.company_data.normalized_result["dividend_paid"],
            self.company_data.normalized_result["cash_finance"],
            self.company_data.normalized_result["PERatio"],
            self.company_data.normalized_result["PEGRatio"]
            ]
    
        weight_vec = [0.15, 0.1, 0.1, 0.15, 0.1, 0.05, 0.1, 0.2, 0.05]
        rating = 0.0
        for it in range(9):
            rating += n_map[it] * weight_vec[it]
        
        rating = 5.0 - rating / 25.0
        return rating